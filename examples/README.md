# Examples

For all of these examples, you'll need to...
* Install Pygame Zero
* Put nethelper.py in the same directory as the example game
* Run nethelper.py. This will start a message relay server.
* Change the SERVER name in the example game to point to the address of your message relay server.

## basic.py
A simple tank game demonstrating the use of nethelper. To keep it simple, only movement is implemented. No shooting.

The player with the name "host" will host the game, while the other players will be clients and can use any names as long as they are unique.

How it works:
* Clients send their keyboard commands to the host
* Host reads the keyboard commands from the client, as well as from itself
* Host update position of all players
* Host send back the players position to all clients
* Client receives players position from host
* Host and clients both displays the tanks in draw()

## server_assigned_names.py
Letting the players choose their names can lead to name clashes, and if a player tries to use a name that's already in use, the server will reject the connection.
One solution is to let the server assign names to the players, instead of letting them choose their own.

This example demonstrates how to request for a random name, and how to read this random name.
It also demonstrate how to assign the first connected player as the host, without requiring a hardcoded name.
Besides that, this example is the same as basic.py