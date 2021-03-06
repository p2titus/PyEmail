import socket
import sendemail
# we just use localhost for security: this is essentially opening a telnet port on our machine
import os


class SenderServer:
    __s = None

    def __init__(self):
        protocol = socket.AF_INET
        s = socket.socket(protocol, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__s = s

    def main_loop(self, get_keys):
        self.__loop(get_keys)
        """pid = os.fork()
        if pid == 0:  # if new process
            self.__loop()"""

    def __loop(self, gk):
        HOST = '127.0.0.1'
        PORT = 65432  # arbritrary - we're using telnet atm so security not a concern yet
        END = '.\n\r'  # phrase that ends server

        emailer = sendemail.Emailer(lambda: gk())

        s = self.__s
        hp = HOST, PORT
        s.bind(hp)
        finished = False

        s.listen()

        while not finished:
            f = lambda x: self.__listen(s, x)
            print('start')
            email = f('email address please')
            finished = email == END
            if not finished:
                msg = f('email message please')
                sendemail.send_email(email, msg)
        s.close()

    # TODO - rewrite to accept arbitrarily long strings
    @staticmethod
    def __listen(s: socket, init_msg: str) -> str:
        BSIZE = 2048

        con, addr = s.accept()

        if init_msg is not None:
            encoding = 'utf-8'
            con.send(bytes(init_msg+'\n', encoding))

        return str(con.recv(BSIZE))
