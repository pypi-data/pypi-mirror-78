import json
import math
import os
import pickle
import shutil
import traceback
from pprint import pformat
from typing import Iterable

import pandas as pd
import pendulum
import ray
import certifi

from loguru import logger
from tqdm import tqdm
from elasticsearch import Elasticsearch
from pulse.downloader.flatten import flatten
from pulse.downloader.utils import Reservoir, uid_filter, elapsed_hms
from dotenv import load_dotenv

load_dotenv()


def extract(
    index,
    query,
    filepath,
    es_hosts=None,
    sample_size=20000,
    fields=(),
    flatten_doc=True,
    delimiter=".",
    include_meta_attribs=False,
    no_flatten: Iterable[str] = (),
    query_slice_size=10000,
    query_concurrency=8,
    auto_mkdir=False,
    env_path=None,
):

    """
    Extracts documents from Pulse

    Performs a multi-process sliced query for documents in a Pulse Elasticsearch index.
    Saves the result to format specified by filename extension. Optional flattening of
    documents is available (use with caution).

    :param index: Elasticsearch index
    :param query: Elasticsearch query
    :param filepath: Output filepath. File extension should match the desired output
        format. Supported formats include:

            - .jsonl    Fastest to download, suited for large datasets. Lowest
                        memory overhead in downstream processes.
            - .json     Standard, faster to load than .jsonl, but not suitable
                        for datasets that must be loaded into memory at once
            - .pkl      Fastest to load if using result in Python script
            - .csv      When consuming data with Excel or Pandas. Fields are
                        automatically flattened. Recommended to create a
                        separate post-processing script if some fields contain
                        data that can't be flattened automatically.

    :param es_hosts: Optional. A list of Elasticsearch hosts. Each item should
        be a fully-qualified URL with authentication if applicable. This overrides
        values that may exist in configuration.
            Example:
                es_hosts = [
                    "https://elastic:password@node1.host.com:9200",
                    "https://elastic:password@node2.host.com:9200",
                ]
    :param sample_size: Maximum number of results to return.
    :param fields: A list of fields to return from Elasticsearch. Limiting the
        amount of fields reduces download time.
    :param flatten_doc: Flatten documents. Useful when working with data frames,
        but has nuances. Use with caution.
    :param delimiter: Delimiter to use when flattening fields
    :param include_meta_attribs: Only applicable when flattening. When false,
        all meta.*.attribs fields are discarded.
    :param no_flatten: A list of fields that should not be flattened
    :param query_slice_size: Maximum number of documents per slice (worker)
    :param query_concurrency: Maximum number of queries to run concurrently
    :param auto_mkdir: Automatically create output directory if it doesn't exist
    :param env_path: Path to environment file
    :return: None
    """
    load_dotenv(env_path)
    if es_hosts is None:
        es_hosts = [h.strip() for h in os.environ.get('ES_URL', '').split(',')]
        if len(es_hosts) == 1 and len(es_hosts[0]) == 0:
            raise RuntimeError(
                "No Elasticsearch hosts defined. Provide es_hosts parameter or set the "
                "ES_URL environment variable (comma-separated if using multiple hosts)"
            )
    start_ts = pendulum.now()
    es = Elasticsearch(hosts=es_hosts,
                       use_ssl=True,
                       verify_certs=True,
                       ca_certs=certifi.where(),
                       )

    # ==================================================================================
    # File management
    # ==================================================================================
    output_format = filepath.split(".")[-1]
    if output_format == "csv":
        flatten_doc = True
    elif output_format in ("json", "jsonl", "pickle", "pkl"):
        pass
    else:
        raise ValueError(f"Unsupported output file type: {filepath}")

    if not "/" in filepath:
        filepath = os.path.join(os.getcwd(), filepath)

    if output_format == 'csv':
        include_meta_attribs = False

    if not os.path.exists(os.path.dirname(filepath)):
        if auto_mkdir:
            os.makedirs(os.path.dirname(filepath))
        raise NotADirectoryError(
            f"Output directory does not exist: {os.path.dirname(filepath)}"
        )
    temp_jsonl_path = filepath + ".tmp"

    # ==================================================================================
    # UID Sampling
    # ==================================================================================

    # Get an idea of how large our result pool is
    count = es.count(index=index, body=query)["count"]
    if count == 0:
        logger.warning("Query returned no results")
        return
    logger.info(f"Document query ({count} results)", extra=query)

    # Add 5 percent buffer to ensure
    # that UID sampling doesn't filter
    # too many documents
    ratio = float(sample_size) / count
    ratio *= 1.05
    if ratio < 1:
        # The query indicates that we're going to be scrolling through a bunch
        # of documents that we won't be using, potentially using up a lot of CPU
        # time. To address this, we add another random sampling method that
        # looks for specific 'uid' field prefixes
        if "bool" not in query["query"]:
            query["query"]["bool"] = {}
        if "filter" not in query["query"]["bool"]:
            query["query"]["bool"]["filter"] = []
        query["query"]["bool"]["filter"].append(
            {
                "bool": {
                    "should": [
                        {"wildcard": {"uid": uid}}
                        # Generate a random list of
                        # UIDs to get within 1/256
                        # above or below the sample
                        # size provided
                        for uid in uid_filter(ratio)
                    ]
                }
            }
        )
        logger.info("Added UID filter to query to reduce document count", query)
        count = es.count(index=index, body=query)["count"]
        logger.info(f"Post-filter document count: {count}")

    logger.info(f"Query: (index={index}):\n{pformat(query)}")

    # ==================================================================================
    # Slice Optimization
    # ==================================================================================
    shard_info = es.cat.shards(index)
    shard_data = [s.strip() for s in shard_info.split("\n") if len(s.strip()) > 0]
    num_shards = len([s for s in shard_data if "STARTED" in s])
    num_slices, m = num_shards, 1
    docs_per_slice = math.ceil(count / num_slices)
    shard_ratio = num_shards / len(shard_data)
    logger.info(f"Available shards: {num_shards}/{len(shard_data)} ({shard_ratio:.2f})")
    logger.debug(f"Shard information: \n{shard_info}")
    while docs_per_slice > query_slice_size:
        logger.debug(f"m={m} slice_size={docs_per_slice} slice_max={query_slice_size}")
        m += 1
        num_slices = m * num_shards
        docs_per_slice = math.ceil(count / num_slices)
    logger.debug(f"m={m} slice_size={docs_per_slice} slice_max={query_slice_size}")

    # ==================================================================================
    # Ray Initialization
    # ==================================================================================
    if not ray.is_initialized():
        # Initialize ray, the task broker.
        # This allows us to run partial
        # queries in parallel.
        logger.info("Initializing Ray")
        # Force Ray to use loopback address to fix issues when
        # a VPN is in use (github.com/ray-project/ray/issues/6573)
        ray.services.get_node_ip_address = lambda: "127.0.0.1"
        try:
            ray.init()
        except:
            traceback.print_exc()
            logger.error("Failed to initialize Ray")
            exit(1)
        logger.info("Ray initialized successfully")

    with open(temp_jsonl_path, "w"):
        pass  # Create/truncate temp path

    # Create tasks for child processes. Each slice gets a unique query containing
    # a distinct portion of the original query. The amount of queries that can be
    # run in parallel is dependent on machine specs, up to a maximum specified by
    # query concurrency. Query concurrency should respect ES cluster capabilities
    # to prevent service outages. A good rule of thumb is to limit concurrent
    # requests to the number of available shards.
    tasks = []
    for i in range(num_slices):
        tasks.append(
            {
                "hosts": es_hosts,
                "query": {**query, "slice": {"id": i, "max": num_slices}},
                "index": index,
                "filepath": temp_jsonl_path,
                "sample_size": math.ceil(sample_size / num_slices),
                "fields": fields,
            }
        )

    # ==================================================================================
    # Query Execution
    # ==================================================================================

    query_ts = pendulum.now()
    results, in_flight_tasks, tq = [], set(), tqdm(total=num_slices)

    while len(tasks) > 0:
        task = tasks.pop(0)
        logger.info(
            f"De-queueing slice ({len(tasks)} pending, {len(in_flight_tasks)} active)"
        )
        while len(in_flight_tasks) >= query_concurrency:
            ready, not_ready = ray.wait(list(in_flight_tasks))
            result_id = ready.pop(0)
            in_flight_tasks.remove(result_id)
            results.append(ray.get(result_id))
            logger.info(
                f"Task completed ({len(tasks)} pending, {len(in_flight_tasks)} active)"
            )
            tq.update(1)
            break
        in_flight_tasks.add(_run_query.remote(**task))
    while len(results) < num_slices:
        ready, not_ready = ray.wait(list(in_flight_tasks))
        result_id = ready.pop(0)
        in_flight_tasks.remove(result_id)
        results.append(ray.get(result_id))
        logger.info(
            f"Task completed ({len(tasks)} pending, {len(in_flight_tasks)} active)"
        )
        tq.update(1)
    tq.close()
    logger.info(f"Getting line count...")
    num_documents = _get_line_count(temp_jsonl_path)
    logger.success(f"Downloaded {num_documents} documents in {elapsed_hms(query_ts)}")

    # ==================================================================================
    # Post-processing / Export
    # ==================================================================================

    if output_format == "jsonl" and not flatten_doc:
        # Big shortcut if you can work with un-flattened JSONL data
        shutil.move(temp_jsonl_path, filepath)
    else:
        logger.info("Loading documents into memory...")
        documents = []
        load_ts = pendulum.now()
        with open(temp_jsonl_path, "r") as f:
            for line in tqdm(f.readlines()):
                line = line.strip()
                if len(line) > 0:
                    documents.append(json.loads(line))
        logger.success(f"Loaded {len(documents)} documents in {elapsed_hms(load_ts)}")

        # ==============================================================================
        # Flatten
        # ==============================================================================

        if flatten_doc:
            logger.info("Flattening documents")
            flatten_ts = pendulum.now()
            documents = [
                flatten(
                    doc,
                    delimiter=delimiter,
                    include_meta_attribs=include_meta_attribs,
                    no_auto_unpack=no_flatten,
                )
                for doc in documents
            ]
            logger.success(f"Flattened documents in {elapsed_hms(flatten_ts)}")

        # ==============================================================================
        # Export
        # ==============================================================================

        logger.info(f"Saving documents to {filepath}...")
        if output_format == "json":
            with open(filepath, "w") as f:
                json.dump(documents, f, indent=4, ensure_ascii=False, sort_keys=False)
        elif output_format == "jsonl":
            with open(filepath, "w") as f:
                for doc in documents:
                    line = json.dumps(
                        doc, indent=4, ensure_ascii=False, sort_keys=False
                    )
                    f.write(f"{line}\n")
        elif output_format in ("pkl", "pickle"):


            with open(filepath, "w") as f:
                pickle.dump(documents, f, protocol=pickle.HIGHEST_PROTOCOL)
        elif output_format == "csv":
            mapping = {}
            logger.info("Checking field types...")
            for doc in documents:
                for field in doc:
                    field_type = type(doc[field]).__name__
                    if field not in mapping:
                        mapping[field] = set()
                    mapping[field].add(field_type)

            for field in mapping:
                mapping[field].discard(type(None).__name__)
                if len(mapping[field]) > 1:
                    logger.warning(
                        f'Field "{field}" contains multiple types: {mapping[field]}'
                    )
            for doc in documents:
                for field, types in mapping.items():

                    # Add field if missing
                    if field not in doc:
                        doc[field] = None

                    # If a field contains a mix of list and non-list results,
                    # make all items in the field list instances for uniformity.
                    if list in types and not isinstance(doc[field], list):
                        doc[field] = [doc[field]]

            for field, types in mapping.items():
                if len(types) > 1 and 'list' in types:
                    logger.info(f'Converted all \"{field}\" results to \'list\'')


            df = pd.DataFrame(documents, columns=sorted(mapping.keys()))
            df.to_csv(filepath)
    if os.path.exists(temp_jsonl_path):
        os.remove(temp_jsonl_path)
    logger.success(f"Pipeline completed in {elapsed_hms(start_ts)}")



def _get_line_count(filename):
    with open(filename, "r") as f:
        return sum(1 for _ in f.readlines())


@ray.remote
def _run_query(
    hosts, query, index, filepath, sample_size, scroll_timeout=3, scroll_size=150, fields=()
):
    """
    Query worker process
    :param query: Elasticsearch query containing slice information, if applicable
    :param index: Elasticsearch index
    :param filepath: Output filepath (JSONL)
    :param sample_size: Max number of documents to retrieve
    :param scroll_timeout: Number of minutes to keep scroll window open
    :param scroll_size: Number of documents to retrieve per scroll
    :param fields: Fields to fetch from Elasticsearch
    :return: None
    """
    es = Elasticsearch(hosts=hosts,
                       use_ssl=True,
                       verify_certs=True,
                       ca_certs=certifi.where(),
                       )
    reservoir = Reservoir(size=sample_size)
    start_ts = pendulum.now()
    sidx = 1  # scroll index
    # Perform the initial scroll
    scroll_time = "{}m".format(int(scroll_timeout))
    kwargs = {}

    if len(fields) > 0:
        kwargs["_source_includes"] = list(fields)

    scroll_ids = set()
    data = es.search(
        index=index,
        scroll=scroll_time,
        size=scroll_size,
        body=query,
        request_timeout=60 * 5,
        ignore_unavailable=True,
        **kwargs,
    )
    sid = data["_scroll_id"]  # Save the resulting scroll id
    scroll_ids.add(sid)
    results = data["hits"]["hits"]  # Extract the documents
    reservoir.bulk_insert(results)  # Insert results into reservoir

    while len(results) > 0:  # Continue to scroll while we have documents

        data = es.scroll(scroll_id=sid, scroll=scroll_time, request_timeout=60 * 5)
        results = data["hits"]["hits"]
        results = [r for r in results]
        reservoir.bulk_insert(results)
        sid = data["_scroll_id"]
        scroll_ids.add(sid)
        sidx += 1

    logger.info(
        f"Scroll completed in {elapsed_hms(start_ts)} "
        f"with {len(reservoir.items)} documents"
    )

    if len(scroll_ids) > 0:
        es.clear_scroll(scroll_id=",".join(scroll_ids))
    logger.info(f"{reservoir.index} documents retrieved by scroll")
    logger.info(f"{len(reservoir.items)} resulting documents in reservoir")
    with open(filepath, "a") as f:
        for document in reservoir.items:
            line = json.dumps(document, ensure_ascii=False)
            f.write(f"{line}\n")

