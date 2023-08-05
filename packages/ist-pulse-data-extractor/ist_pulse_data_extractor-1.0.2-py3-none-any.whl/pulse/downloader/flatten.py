from typing import Iterable


def flatten(
    doc,
    delimiter=".",
    exclude=("_source",),
    meta_flatten_mode="ignore",
    include_meta_attribs=False,
    no_auto_unpack: Iterable[str] = (),
):

    out = {}

    out["_id"] = doc["_id"]
    out["_index"] = doc["_index"]

    doc = auto_flatten(
        doc, delimiter=".", exclude=("_source",), meta_flatten_mode=meta_flatten_mode
    )

    if not include_meta_attribs:
        doc = {k: v for k, v in doc.items() if not ("meta" in k and "attribs" in k)}

    unpacked = {}
    for k, v in doc.items():
        if isinstance(v, list) or isinstance(v, dict):
            res = v
            if (
                isinstance(res, list)
                and len(res) == 1
                and (
                    k not in no_auto_unpack
                    or any((k.startswith(p) for p in no_auto_unpack))
                )
            ):
                res = v[0]
            if isinstance(res, dict):
                res = auto_flatten(res, keys=(k,), delimiter=delimiter, exclude=exclude)
                unpacked.update(res)
            else:
                unpacked[k] = res
        else:
            unpacked[k] = v

    return unpacked


def auto_flatten(
    doc, keys=(), delimiter=".", exclude=("_source",), meta_flatten_mode="ignore"
):

    flattened = {}
    for k in doc:
        v = doc[k]

        can_str_concat = isinstance(v, list) and all(
            (isinstance(i, str) and "\n" not in i for i in v)
        )

        if isinstance(v, dict):
            out_keys = keys
            if k not in exclude:
                out_keys = out_keys + (k,)
            f = auto_flatten(v, keys=out_keys, delimiter=delimiter, exclude=exclude)
            flattened.update(f)

        elif can_str_concat:
            out_key = delimiter.join(keys + (k,))
            v = "\n".join(v)
            flattened[out_key] = v

        elif isinstance(v, list) and len(keys) > 0 and keys[-1] == "meta":

            f = flatten_meta(v, key=k, mode=meta_flatten_mode)
            flattened.update(f)

        else:
            out_key = delimiter.join(keys + (k,))
            flattened[out_key] = v
    return flattened


def flatten_meta(meta, key, mode="ignore"):

    assert isinstance(meta, list), f"Expected list of meta results: {meta}"

    if len(meta) == 0:
        return {}

    elif len(meta) == 1:
        return auto_flatten(meta[0], keys=("meta", key))

    else:
        if mode == "ignore":
            return auto_flatten(meta[0], keys=("meta", key))
        elif mode == "keep":
            return list(auto_flatten(x, keys=("meta", key)) for x in meta)
        elif mode == "error":
            raise Exception("Multiple results for meta field")
        else:
            raise ValueError("Invalid mode: " + mode)
