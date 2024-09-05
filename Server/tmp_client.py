import socket
import struct
import time


def main():
    sock = socket.socket()
    sock.connect(('192.168.0.191', 12345))
    print("Connected", end='\n\n')

    tmp_tuple = struct.unpack('!I', sock.recv(4))
    client_number = tmp_tuple[0]
    print(f"Client number {client_number}")

    name = 'Eugene'
    name_b = name.encode('utf-8')
    tmp = len(name_b)
    name_length = struct.pack('!I', tmp)
    sock.send(name_length)
    data = struct.pack(f'!{tmp}s', name_b)
    sock.send(data)

    time.sleep(5)

main()