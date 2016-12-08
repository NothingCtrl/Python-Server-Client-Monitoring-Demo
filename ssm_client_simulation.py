import socket
import time
import threading

server_address = socket.gethostname()
server_port = 9999


def xor_crypt_string(data, key='awesomepassword', encode=False, decode=False):
    from itertools import izip, cycle
    import base64

    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored


def client_service(count):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    print "Going connect..."
    c.connect((server_address, server_port))
    print "Connected"

    if count == 2:
        print "Client 2 make connection but not send any data..."

    if count != 5 and count != 2:
        encoded = xor_crypt_string("This is data 1 send from client: %d" % count, encode=True)
        packet_1 = encoded[:15]
        packet_2 = encoded[15:]
        time.sleep(1)
        c.send(packet_1)
        print "%d - Packet sended [1]: %s" % (count, packet_1)
        time.sleep(0.1)
        c.send(packet_2)
        print "%d - Packet sended [2]: %s" % (count, packet_2)
        time.sleep(1)
        c.send(xor_crypt_string("This data 2 send from client: %d" % count, encode=True))

    if count == 5:
        print "Count = 5, will send data after 45s"
        time.sleep(45)
        c.send(xor_crypt_string("Count 5 send data after 45s", encode=True))

    if count == 7:
        c.send(xor_crypt_string("Client going sleep to test if thread terminated time out", encode=True))
        time.sleep(30)
        c.send(xor_crypt_string("If this message reach sever, thread not terminated after time out", encode=True))

i = 1
while i <= 100:
    print i
    threading.Thread(target=client_service, args=(i,)).start()
    time.sleep(.2)
    i += 1

# client_service(5)
# threading.Thread(target=client_service, args=(5,))


