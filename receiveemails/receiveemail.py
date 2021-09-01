import poplib
from containers import *

"""
Recall POP downloads email from a (remote) server and deletes them from the server once received
By contrast, IMAP caches emails, allows you to perform actions, uploads the actions then deletes the cache
As we store emails in this server, POP is the correct choice of protocol
HOWEVER, you may choose to use IMAP instead. If this is the case, you should only need to reconfigure the message 
receiving in this class
No other class should receive email except by calling methods from this class
"""


class EmailReceiver:
    __DEBUG_LVL = 0  # use 0 for prod
    __ks: [(str, str, str)] = None

    # for an explanation, see the almost identical code in userinput/sendemail.py
    def __init__(self, get_keys):
        self.__ks = get_keys()

    class Account:
        local: str
        pwd: str
        domain: str

    # as a postcondition, we assert that all emails on the server that we've downloaded are deleted
    def read_emails(self) -> [Email]:
        accounts = self.__ks
        acc = []

        for a in accounts:
            x = Account()
            x.local, x.domain, x.pwd = a

            es = self.__get_updates_account(x)
            acc.append(es)

        return acc

    @staticmethod
    def __get_updates_account(a: Account) -> [Email]:
        es = []
        port = 995
        mb = poplib.POP3_SSL(a.domain, port)
        mb.user(a.local)
        mb.pass_(a.pwd)

        for msg in mb.retr(0):
            es += EmailReceiver.__emailify(msg)

        mb.quit()
        return es

    # TODO - write method
    @staticmethod
    def __emailify(msg):
        pass
