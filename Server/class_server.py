import socket
import struct
# import multiprocessing


class Server:

    __connections = {}      # (connection number, connection)
    __i_connection = 1
    __ip = ''
    __port = 12345
    __sock = None
    __names = {}

    def __init__(self):
        file = open("ip.txt", "r")
        self.__ip = file.read()

    def start(self):
        self.__sock = socket.socket()
        self.__sock.bind((self.__ip, self.__port))

    def listen(self):
        self.__sock.listen(20)

        while True:
            self.__connections[self.__i_connection], addr = self.__sock.accept()
            print(f"\nNew connection:\nSocket = {self.__connections[self.__i_connection]}, number = {self.__i_connection}")

            data = struct.pack('!I', self.__i_connection)
            self.__connections[self.__i_connection].send(data)

            tmp_tuple = struct.unpack('!I', self.__connections[self.__i_connection].recv(4))
            length = tmp_tuple[0]

            tmp_tuple = struct.unpack(f'!{length}s', self.__connections[self.__i_connection].recv(length))
            received_name = tmp_tuple[0].decode('utf-8')
            self.__names[self.__i_connection] = received_name
            print(f"New name: {self.__names[self.__i_connection]}")

            self.__i_connection += 1
        # new thread