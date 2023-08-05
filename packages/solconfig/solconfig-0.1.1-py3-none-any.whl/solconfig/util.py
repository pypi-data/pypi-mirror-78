
def dict_safe_get(dct:dict, *keys):
    """safe method to get value of nested dictionary"""

    for key in keys:
        dct = dct.get(key)
        if dct == None: break

    return dct