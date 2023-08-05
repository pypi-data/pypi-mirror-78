# ========================================================
# RECURSIVE METHODS FOR DICTIONARY MANIPULATION
# ========================================================

def recursive_create_with_keys(keys, value):
    """
    Method to recursively create dictionary from keys and value

    """
    if len(keys) == 1:
        d0 = {keys[0]: value}

    else:
        d0 = {keys[0]: recursive_create_with_keys(keys[1:], value)}

    return d0

def recursive_set(d0, d1, append_lists=True, update_sets=True, existing_keys_only=False):
    """
    Method to recursively set values from d1 into d0

    Example:

      d0 = {'a': {'b': [1, 2]}}
      d1 = {'a': {'b': [3, 4]}}

      recursive_set_(d0, d1)

      d0 ==> {'a': {'b': [1, 2, 3, 4]}}

    :params

      (bool) append_lists       : if True, append any lists (rather than replace)
      (bool) existing_keys_only : if True, set only if key is present in d0 already

    """
    for k, v in d1.items():
        if k in d0:
            if type(v) is dict:
                recursive_set(d0[k], v, append_lists, existing_keys_only)
            else:
                if type(d0[k]) is list and append_lists:
                    d0[k].extend(v) if type(v) is list else d0[k].append(v)
                elif type(d0[k]) is set and update_sets:
                    d0[k].update(v) if type(v) is set else d0[k].add(v)
                else:
                    d0[k] = v
        elif not existing_keys_only:
            d0[k] = v

def recursive_set_with_keys(d0, keys, value, **kwargs):
    """
    Method to recursively set value into d0 via list of keys

    Example:

      d0 = {'a': {'b': [1, 2]}}

      recursive_set_with_keys(d0, keys=['a', 'b'], value=3)

      d0 ==> {'a': {'b': [1, 2, 3]}}

    """
    d1 = recursive_create_with_keys(keys, value)
    recursive_set(d0, d1, **kwargs)
