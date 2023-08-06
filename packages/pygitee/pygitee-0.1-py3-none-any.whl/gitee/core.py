# core.params(locals());
def params(kwargs: dict):
    result = {}
    for (k, v) in kwargs.items():
        if isinstance(v, str) or isinstance(v, int):
            result[k] = v
        elif isinstance(v, dict):
            for (kv, vv) in v.items():
                if isinstance(vv, str) or isinstance(v, int):
                    result[kv] = vv

    return result
