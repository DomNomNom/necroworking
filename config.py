
protocolVersion = '1.0'

# a map from the remote players key to the key of "player 2"
keyMap = {
    'Left': 'j',
    'Right': 'l',
    'Up': 'i',
    'Down': 'k',
    # 'Escape': 'Escape',
}
listenWindow = 'Crypt of the NecroDancer'
eventAttributeList = 'Key Time'.split()  # which attrs get sent over the network



port = 1597
packetSize = 2048



# things only relevant for the client
remoteAddress = ('localhost', port)

#  things only relevant for the server
serverBinding = ('0.0.0.0', port)
serverBacklog = 5
