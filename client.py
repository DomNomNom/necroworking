import pyHook
import pythoncom
import win32com.client

import sys
import json
import socket
import threading
import datetime
import ctypes
import traceback

import config


shell = win32com.client.Dispatch("WScript.Shell")  # emulate keyboard presses with this

# create connection to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(config.remoteAddress)



user32dll = ctypes.WinDLL("User32.dll")
def isToggledOn():
    VK_CAPITAL = 0x14
    VK_SCROLL = 0x91
    return user32dll.GetKeyState(VK_SCROLL)  # check whether scroll lock is on.
    return user32dll.GetKeyState(VK_CAPITAL)

epoch = datetime.datetime.utcfromtimestamp(0)
def unixTimeMillis():
    return (datetime.datetime.now() - epoch).total_seconds() * 1000.0

def handleNetworkMessage(message):

    if not isToggledOn():
        print 'mute (scroll lock) is on: ignoring network message'
        return

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
        try:
            for line in message.split('\n'):
                handleNetworkMessage(line)
        except:
            traceback.print_exc(file=sys.stdout)
        message = clientSocket.recv(config.packetSize)
    clientSocket.close()


def OnKeyboardEvent(event):

    if event.WindowName == config.listenWindow and event.Key in config.keyMap:
        if not isToggledOn():
            print 'mute (scroll lock) is on: not sending'
            return True

        message = {
            'time': unixTimeMillis(),
            'v': config.protocolVersion,
            '~key': event.Key,  # having the '~' here is a hack to get consistent ordering
        }
        message = json.dumps(message, sort_keys=True) + '\n'
        print 'sending message:', repr(message)
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
