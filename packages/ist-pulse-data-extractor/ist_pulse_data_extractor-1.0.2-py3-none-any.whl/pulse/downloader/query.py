import pendulum

def build_query(
        start_date=None,
        end_date=None,
        project_id=None,
        campaign_id=None,
        where_exists=(),
        where_not_exists=(),
        include_match: dict = None,
        exclude_match: dict = None,
        include_terms: dict = None,
        exclude_terms: dict = None,
        include_phrase: dict = None,
        exclude_phrase: dict = None,
        doc_type=None,
        timestamp_field="norm.timestamp",
        query_string=None,
        ):
    """
    Builds an Elasticsearch query
    :param start_date: Date range start (eg. 2020-06-14 or 2020-06-14T12:00:00.000Z)
    :param end_date: Date range end
    :param project_id: Project ID
    :param campaign_id: Campaign ID
    :param where_exists: A list or tuple containing fields that should exist in each document
    :param where_not_exists: A list or tuple containing fields that should not exist in each document
    :param include_match: A mapping of fields to lists of keywords or phrases to include as full text matches.
    :param exclude_match: A mapping of fields to lists of keywords or phrases to exclude as full text matches.
    :param include_terms: A mapping of fields to lists of keywords to include as partial text matches.
    :param exclude_terms: A mapping of fields to lists of keywords to exclude as partial text matches.
    :param include_phrase: A mapping of fields to lists of keywords or phrases to include as partial text matches.
    :param exclude_phrase: A mapping of fields to lists of keywords or phrases to exclude as partial text matches.
    :param doc_type: Pulse document type
    :param timestamp_field: Timestamp field to use for start_date and end_date
    :param query_string: A prepared query string
    :return:
    """
    query = []
    must_not = []

    if project_id is not None:
        query.append(
            {"terms": {"meta.rule_matcher.results.project_id": [project_id]}}
        )

    if campaign_id is not None:
        query.append(
            {"terms": {"meta.rule_matcher.results.campaign_id": [campaign_id]}}
        )

    if doc_type is not None:
        query.append({"match": {"type": doc_type}})

    if include_terms is not None:
        for field, value in include_terms.items():
            _value = value
            if isinstance(value, list):
                pass
            elif isinstance(value, tuple):
                _value = list(value)
            else:
                _value = [value]
            query.append({"terms": {field: _value}})



    if include_match is not None:
        for field, value in include_match.items():
            query.append({"match": {field: value}})

    if include_phrase is not None:
        for field, value in include_phrase.items():
            query.append({"match_phrase": {field: value}})


    if where_exists is not None:
        if isinstance(where_exists, list) or isinstance(
                where_exists, tuple
        ):
            for item in where_exists:
                query.append({"exists": {"field": item}})
        elif isinstance(where_exists, str):
            query.append({"exists": {"field": where_exists}})
        else:
            raise TypeError(
                f"Expected list or tuple, "
                f"but got {type(where_exists).__name__}"
            )

    if query_string is not None:
        query.append({"query_string": {"query": query_string}})

    if start_date is not None and end_date is not None:
        d0 = pendulum.parse(start_date)
        d1 = pendulum.parse(end_date)
        query.append(
            {
                "range": {
                    timestamp_field: {
                        "gte": d0.isoformat(),
                        "lte": d1.isoformat(),
                    }
                }
            }
        )

    if where_not_exists is not None:
        if isinstance(where_not_exists, list) or isinstance(
                where_not_exists, tuple
        ):
            for item in where_not_exists:
                must_not.append({"exists": {"field": item}})
        elif isinstance(where_not_exists, str):
            must_not.append({"exists": {"field": where_not_exists}})
        else:
            raise TypeError(
                f"Expected list or tuple, "
                f"but got {type(where_not_exists).__name__}"
            )

    if exclude_match is not None:
        for field, value in exclude_match.items():
            must_not.append({"match": {field: value}})

    if exclude_phrase is not None:
        for field, value in exclude_phrase.items():
            must_not.append({"match_phrase": {field: value}})

    if exclude_terms is not None:
        for field, value in exclude_terms.items():
            _value = value
            if isinstance(value, list):
                pass
            elif isinstance(value, tuple):
                _value = list(value)
            else:
                _value = [value]
            must_not.append({"terms": {field: _value}})

    if len(must_not) > 0:
        query.append({"bool": {"must_not": must_not}})

    query = {"query": {"bool": {"filter": query}}}

    return query
