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
        BSIZE = 1024
        HOST = '127.0.0.1'
        PORT = 65432  # arbritrary - we're using telnet atm so security not a concern yet
        END = '.'  # phrase that ends server

        s = self.__s
        finished = False

        while not finished:
            content = ''
            fst = True
            s.listen()
            conn, addr = s.accept()
            

        s.close()
