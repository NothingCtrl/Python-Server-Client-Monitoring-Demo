import time
import socket
import logging

remote_server = socket.gethostname()
remote_port = 9999
# time to send update data
loop_time = 5
# encode / decode key
key = 'awesomepassword'
# client_id
client_id = socket.gethostname()


class Client(object):

    def __init__(self, cid, server, port, de_key):
        """
        :param cid: client_id
        :param server: remote server address
        :param port: remote server port
        :param de_key: encode / decode key
        """
        self.remote_server = server
        self.remote_port = port
        self.key = de_key
        self.client_id = cid

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

    def get_server_info(self):
        return "Some data... ID-%s" % self.client_id

    def send_encode_data(self, data):
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((self.remote_server, self.remote_port))
            c.send(self.xor_crypt_string(data, encode=True))
            print "Data sended, time: ", time.time()
            c.close()
        except Exception as e:
            print "Error connect to server!"
            logging.exception(e)

    def run(self):
        print "Client start, remote server: %s, remote port: %d " % (remote_server, remote_port)
        while True:
            try:
                begin = time.time()
                self.send_encode_data(self.get_server_info())
                sleep = loop_time - (time.time() - begin)
                if sleep > 0:
                    time.sleep(sleep)
            except Exception as e:
                logging.exception(e)
                time.sleep(1)
                pass

Client(client_id, remote_server, remote_port, key).run()
