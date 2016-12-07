import socket
import time
import threading

server_address = socket.gethostname()
server_port = 9999


def client_service(count):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    print "Going connect..."
    c.connect((server_address, server_port))
    print "Connected"

    if count != 5:
        time.sleep(1)
        c.send("This data 1 send from client: %d" % count)
        time.sleep(1)
        c.send("This data 2 send from client: %d" % count)

    if count == 5:
        print "Count = 5, will send data after 45s"
        time.sleep(45)
        c.send("Count 5 send data after 45s")

    if count == 7:
        c.send("Client going sleep to test if thread terminated time out")
        time.sleep(30)
        c.send("If this message reach sever, thread not terminated after time out")

i = 0
while i <= 100:
    print i
    threading.Thread(target=client_service, args=(i,)).start()
    time.sleep(.2)
    i += 1

# client_service(5)
# threading.Thread(target=client_service, args=(5,))


