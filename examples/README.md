# Examples

For all of these examples, you'll need to...
* Install Pygame Zero
* Put nethelper.py in the same directory as the example game
* Start a message relay server with the group "net_demo" (ie. run ```python3 nethelper.py -g net_demo```).
* Change the SERVER name in the example game to point to the address of your message relay server.

## basic.py
A simple tank game demonstrating the use of nethelper. To keep it simple, only movement is implemented. No shooting.

The player with the name "host" will host the game, while the other players will be clients and can use any names as long as they are unique.

How it works:
1. Clients send their keyboard commands to the host
2. Host reads the keyboard commands from the client and itself, then update position of all players
3. Host send back the players position to all clients
4. Client receives players position from host
5. Host and clients both displays the tanks in draw()

## server_assigned_names.py
Letting the players choose their names can lead to name clashes, and if a player tries to use a name that's already in use, the server will reject the connection. One solution is to let the server assign names to the players, instead of letting them choose their own.

This example demonstrates how to request for a random name, and how to read this random name. It also demonstrate how to assign the first connected player as the host, without requiring a hardcoded name. Besides that, this example is the same as basic.py

## remember_commands.py
In basic.py, the host will only move the client's tank if they receive a control command. If no control commands were received, the client's tank will not move for that frame. This can be a problem, as the client may be slightly delayed in sending out their control command (eg. slow network, high CPU load). This will cause the client's tank to pause once every few frames, resulting in slower movements.

To solve this, the host should remember the last command from the client. If no new commands were received, the host should just continue with the last command. In this example game, we use a new global dictionary **controls** to keep track of the commands from each player.

In this example, we also change the format of the command; instead of sending the change in x/y, we now send a string representing the key press. This prevents the client from cheating by sending a large change in x/y.