import socket
import threading
import logging
import time

host = socket.gethostname()
port = 9999


class Server(object):
    def __init__(self, listen_port):
        self.host = socket.gethostname()
        self.port = listen_port
        self.count_thread = 0

    @staticmethod
    def client_hande(client, timeout=2, thread_time=5):
        # timeout: set time close of connection if no data receive from client
        # timeout reset (recouting) everytime have data from client
        client.settimeout(timeout)
        # thread_time: maximum run time of thread, note that if timeout > thread_time,
        # data = client.recv(102400) still waiting in first loop
        end_time = time.time() + thread_time
        while time.time() < end_time:
            # every timeout on 'client.recv(102400)' while will loop,
            # so this will loop 2 times if no data send / no connection from client side, with default value 2,5
            data = client.recv(102400)
            if data:
                print "Data from client: ", data
            # break
        client.close()
        print "End connection..."

    def run(self):
        print "Server start, listen port: ", self.port
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        serversocket.listen(120)
        while True:
            try:
                client, address = serversocket.accept()
                self.count_thread += 1
                threading.Thread(target=self.client_hande, args=(client,)).start()
            except Exception as e:
                logging.exception(e)

# start server
Server(9999).run()
