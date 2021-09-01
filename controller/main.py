"""
controller for the email server
mainly used to supply keys to the senders and receivers
uses a dependency injection pattern
"""

from load_keys import load_account_details
from receiveemails import EmailReceiver
from userinput import SenderServer

def run_server():
    default_fname = "keys.json"
    print('leave blank for default file')
    fname = input('Please input file with keys (should be under root dir of project)\n')
    if fname == '':
        ks = load_account_details()
    else:
        ks = load_account_details(fname)
    f = lambda: ks
    recv = EmailReceiver(f)
    send = SenderServer()
    # TODO - put the system in parallel

