"""
at the moment, we are only supporting gmail addresses
"""
import smtplib, ssl


class Emailer:
    """
    A quick explanation of how Emailer is implemented
    We load our keys from an external json file
    This json file contains addresses, passwords and domain names for the addresses we use with the server
    These keys are stored in ks and used when required
    To refresh these keys, the Emailer object can be dropped and recreated - there is no other state stored

    See receiveemails/receiveemail.py for another copied implementation
    """
    __ks: [dict] = None

    def __init__(self):
        KEYS_NAME = '../keys.json'
        ks = self.__load_keys(KEYS_NAME)
        accs = []
        for k in ks:
            accs.append((k['addr'], k['type'], k['keys']))
        self.__ks = accs

    @staticmethod
    def __load_keys(keys_file_name):
        from json import load
        f = open(keys_file_name)
        x = load(f)
        f.close()
        return x

    """
    Sends an email with the specified message from a specified address
    """
    def send_email(self, addr, msg):
        ks = filter(lambda x: x['addr'] == addr, self.__ks)
        try:
            self.__email(ks.__next__(), addr, msg)
        except StopIteration:
            raise KeyError('no email found')

    @staticmethod
    def __email(ks, sender, msg):
        recv = ks['addr']
        port = 465
        pwd = ks['keys']

        ctxt = ssl.create_default_context()

        with smtplib.SMTP_SSL(ks['type'], port, context=ctxt) as s:
            s.login(sender, pwd)
            s.sendmail(sender, recv, msg)
