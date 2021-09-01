def load_account_details(keys_file_name="keys.json"):
    fname = "../%s", keys_file_name
    ks = __load_keys(fname)
    acc = []
    for k in ks:
        acc.append((k['addr'], k['type'], k['keys']))
    return acc


def __load_keys(fname):
    from json import load
    with open(fname) as f:
        x = load(f)
    return x
