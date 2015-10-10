

import pyHook
import pythoncom
import sys
import json
import socket
import threading
import win32com.client
import datetime

import config


shell = win32com.client.Dispatch("WScript.Shell")  # emulate keyboard presses with this

# create connection to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(config.remoteAddress)


epoch = datetime.datetime.utcfromtimestamp(0)
def unixTimeMillis():
    return (datetime.datetime.now() - epoch).total_seconds() * 1000.0

def handleNetworkMessage(message):
    event = json.loads(message)
    assert "time" in event
    assert event['v'] == config.protocolVersion

    # print 'message received:', message

    mappedKey = config.keyMap[event['~key']]
    shell.SendKeys(mappedKey)
    lag = int(unixTimeMillis() - event['time'])
    print "{:>3}ms lag    pushing mapped key: {}".format(lag, mappedKey)

def listenToSocket(clientSocket):
    print 'Connected to server.'
    message = clientSocket.recv(config.packetSize)
    while message.strip():
        handleNetworkMessage(message)
        message = clientSocket.recv(config.packetSize)
    clientSocket.close()


def OnKeyboardEvent(event):

    if event.WindowName == config.listenWindow and event.Key in config.keyMap:
        message = {
            'time': unixTimeMillis(),
            'v': config.protocolVersion,
            '~key': event.Key,  # having the '~' here is a hack to get consistent ordering
        }
        message = json.dumps(message, sort_keys=True)
        print 'sending message:', message
        clientSocket.send(message)


    # return True to pass the event to other handlers
    # return False to stop the event from propagating
    return True



def listenToKeyboard():
    # set up keyboard listening
    hm = pyHook.HookManager()  # create the hook mananger
    hm.KeyDown = OnKeyboardEvent  # register callback
    hm.HookKeyboard()  # hook into the keyboard events

    print 'starting listening to keyboard events'
    pythoncom.PumpMessages() # loops forever

if __name__ == '__main__':

    if len(sys.argv) < 2 or sys.argv[1] != '--noKeyboardListen':
        # set up listening socket responses
        keyboardThread = threading.Thread(target=listenToKeyboard)
        keyboardThread.deamon = True  # stop when finishes
        keyboardThread.start()
    else:
        print 'not going to listen to keyboard'

    listenToSocket(clientSocket)
