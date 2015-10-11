
protocolVersion = '1.1'

# a map from the remote players key to the key of "player 2"
keyMap = {
    'Left': 'j',
    'Right': 'l',
    'Up': 'i',
    'Down': 'k',
    'Enter': 'Enter',
}
listenWindow = 'Crypt of the NecroDancer'



port = 1597
packetSize = 256



# things only relevant for the client
remoteAddress = ('58.84.227.113', port)

#  things only relevant for the server
serverBinding = ('0.0.0.0', port)
serverBacklog = 5
