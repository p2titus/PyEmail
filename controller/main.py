"""
controller for the email server
mainly used to supply keys to the senders and receivers
uses a dependency injection pattern
"""

from load_keys import load_account_details

def run_server():
    default_fname = "keys.json"
    print('leave blank for default file')
    fname = input('Please input file with keys (should be under root dir of project)\n')
    if fname == '':
        fname = default_fname


