 #!/usr/bin/env python

"""
A simple server that broadcasts what one client sends to all other clients
"""

import socket
import threading

import config

clients = {}

def manageClient(clientSocket, address):
    assert address not in clients
    clients[address] = clientSocket
    print "client connected:", address

    message = clientSocket.recv(config.packetSize)
    while message.strip():
        print '{} \t --> {}'.format(address, repr(message))
        # clientSocket.send(message)
        for other in clients:
            if other != address:
                clients[other].send(message)
                print '{} \t <-- {}'.format(other, repr(message))
        message = clientSocket.recv(config.packetSize)

    clientSocket.send("you send an empty message. goodbye.")
    clientSocket.close()
    del clients[address]
    print "client disconnected:", address



serverBinding = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverBinding.bind(config.serverBinding)
serverBinding.listen(config.serverBacklog)
print 'waiting for client to connect'
while True:
    threading.Thread(target=manageClient, args=serverBinding.accept()).start()


