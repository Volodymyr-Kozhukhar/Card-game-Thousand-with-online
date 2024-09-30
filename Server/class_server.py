import socket
import struct

from threading import Thread

def listen_client(client_number, conn):
    try:
        # Waiting for number form the client
        while True:
            tmp_tuple = struct.unpack('!I', conn.recv(4))
            received_number = tmp_tuple[0]
        # If number is 0 → client disconnected by button
            if received_number == 0:
                print(f"Client {client_number} disconnected")
                break
        # if error occurred → client closed window
    except ConnectionResetError:
        print(f"Client {client_number} disconnected unexpectedly")
    finally:
        conn.close()

class Server:

    __connections = {}      # (connection number, connection)
    __i_connection = 1
    __ip = ''
    __port = 12345
    __sock = None
    __names = {}            # (connection number, name)

    def __init__(self):
        with open("ip.txt", "r") as file:
            self.__ip = file.read()

    def start(self):
        self.__sock = socket.socket()
        self.__sock.bind((self.__ip, self.__port))

    def listen(self):
        self.__sock.listen(20)

        while True:

            # Accept new connection with a client and write to the list.
            self.__connections[self.__i_connection], addr = self.__sock.accept()
            print(f"\nNew connection:\nSocket = {self.__connections[self.__i_connection]}, number = {self.__i_connection}")

            # Sending number of the connection to the client.
            data = struct.pack('!I', self.__i_connection)
            self.__connections[self.__i_connection].send(data)

            # Receiving length of next message.
            tmp_tuple = struct.unpack('!I', self.__connections[self.__i_connection].recv(4))
            length = tmp_tuple[0]

            # Receiving text message and unpacking.
            tmp_tuple = struct.unpack(f'!{length}s', self.__connections[self.__i_connection].recv(length))
            received_name = tmp_tuple[0].decode('utf-8')
            self.__names[self.__i_connection] = received_name
            print(f"New name: {self.__names[self.__i_connection]}")

            # Creating new thread for each client with listen_client() func.
            client_thread = Thread(target=listen_client, args=(self.__i_connection, self.__connections[self.__i_connection]))
            client_thread.start()

            self.__i_connection += 1