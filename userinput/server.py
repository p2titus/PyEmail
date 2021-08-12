from socket import socket, AF_UNIX, SOCK_STREAM
# we just use localhost for security: this is essentially opening a telnet port on our machine
import os


class Server:
    __s = None

    def __init__(self):
        protocol = AF_UNIX
        self.__s = socket(family=protocol, type=SOCK_STREAM)

    def main_loop(self):
        pid = os.fork()
        if pid == 0:  # if new process
            self.__loop()

    def __loop(self):
        HOST = '127.0.0.1'
        PORT = 65432  # arbritrary - we're using telnet atm so security not a concern yet
        END = '.'  # phrase that ends server

        s = self.__s
        s.bind((HOST, PORT))
        finished = False

        while not finished:
            x = self.__listen(s, 'email address please')
            finished = x == END

        s.close()

    @staticmethod
    def __listen(s: socket, init_msg: str) -> str:
        BSIZE = 1024
        acc = ''

        s.listen()
        con, addr = s.accept()

        if init_msg is not None:
            con.send(init_msg)

        with con:
            fresh_data = True
            while fresh_data:
                data = con.recv(BSIZE)
                if not data:
                    fresh_data = False
                else:
                    acc += data

        return data
