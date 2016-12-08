import socket
import threading
import logging
import time

host = socket.gethostname()
# maximum thread allow run the same time
maximum_run_thread = 10
# listen port
port = 9999
# encode / decode key
key = 'awesomepassword'


class Server(object):
    def __init__(self, listen_port, pass_key):
        self.host = socket.gethostname()
        self.port = listen_port
        self.count_thread = 0
        self.total_thread = 0
        self.key = pass_key
        # Maximum time get data from each client
        self.client_timeout = 2

    def xor_crypt_string(self, data, encode=False, decode=False):
        """
        Encode / decode data between client and server
        :param data:
        :param encode:
        :param decode:
        :return:
        """
        from itertools import izip, cycle
        import base64

        if decode:
            data = base64.decodestring(data)
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in izip(data, cycle(self.key)))
        if encode:
            return base64.encodestring(xored).strip()
        return xored

    def recv_timeout(self, client):
        # timeout reset (recouting) everytime have data from client
        # client.settimeout(self.client_timeout)
        client.setblocking(0)
        begin = time.time()
        end_time = begin + self.client_timeout + 0.5
        total_data = []
        # sleep_count = 0
        while time.time() < end_time:
            if total_data and time.time() - begin > self.client_timeout:
                break
            try:
                data = client.recv(102400)
                if data:
                    total_data.append(data)
                else:
                    # sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
        # join all parts to make final string
        return ''.join(total_data)

    def client_hande(self, client, thread_count, thread_time=5):
        # thread_time: maximum run time of thread, note that if timeout > thread_time,
        # data = client.recv(102400) still waiting in first loop
        end_time = time.time() + thread_time
        while time.time() < end_time:
            # every timeout on 'client.recv(102400)' while will loop,
            # so this will loop 2 times if no data send / no connection from client side, with default value 2,5
            data = self.recv_timeout(client)
            # data = client.recv(102400)
            if data:
                deccoded_data = self.xor_crypt_string(data, decode=True)
                # save data to database
                print deccoded_data
                # no need wating more data
                client.close()
                break
        client.close()
        self.count_thread -= 1
        print "End connection... ", thread_count

    def run(self):
        print "Server start, listen port: ", self.port
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        serversocket.listen(120)
        while True:
            try:
                if self.count_thread < maximum_run_thread:
                    client, address = serversocket.accept()
                    self.count_thread += 1
                    self.total_thread += 1
                    threading.Thread(target=self.client_hande, args=(client, self.total_thread)).start()
                    print "Thread %d created, current running threads: %d, client address: %s" % \
                          (self.total_thread, self.count_thread, address[0])
                else:
                    print "Maximum threads reach!"
                    time.sleep(1)
            except Exception as e:
                logging.exception(e)
                time.sleep(1)

# start server
Server(9999, key).run()
