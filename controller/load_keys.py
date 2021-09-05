import os


def load_account_details(*args, keys_file_name="keys.json"):
    fname = "../%s" % keys_file_name
    ks = __load_keys(fname)
    acc = []
    if ks is not None:
        for k in ks:
            x = ks[k]
            acc.append((x['addr'], x['type'], x['keys']))
    return acc


def __load_keys(fname):
    from json import load
    if os.path.exists(fname) and os.stat(fname).st_size > 0:
        with open(fname) as f:
            x = load(f)
    else:
        x = None
    return x
