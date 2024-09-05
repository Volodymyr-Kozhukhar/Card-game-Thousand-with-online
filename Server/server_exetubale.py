from time import sleep
from threading import Thread
import class_server


def main():

    new_server = class_server.Server()
    new_server.start()
    listen_thread = Thread(target=new_server.listen())
    listen_thread.start()
    listen_thread.join()

main()