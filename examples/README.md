# Examples

For all of these examples, you'll need to...
* Install Pygame Zero
* Put nethelper.py in the same directory as the example game
* Start a message relay server with the group "net_demo" (ie. run ```python3 nethelper.py -g net_demo```).
* Change the SERVER name in the example game to point to the address of your message relay server.

# Purpose
The purpose of these examples is to demonstrate the use of nethelper in games to beginner programmers. As such, I try to keep them as simple as possible, even if it means that the game itself is crude or flawed.

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

## static_objects.py
In basic.py, the position of the tanks are shared with the clients on every frame. That make senses, as the tanks are often moving. However, many games will have a lot of static objects such as trees, rocks, bushes, etc, which are randomly placed at the start of the game, but don't move after that. While you can send these to the clients on every frame, it is often more efficient to send them only once.

In this example, we introduce the concept of a **request**. There is nothing special about this; it's just a normal **send_msg** like what we have been using. If the client detects that its "rocks" list is empty, it will send a message with the title "request" and the string "rocks" in the content. When the server receives this message, it will send the "rocks" list back to the client.

Using this approach, we can share a world with a large number of static objects, without having to send a lot of data across the network on every frame.

## bullets_simple.py
This uses a simple approach of handling bullets. The server does all the work of moving the bullet, and send the result to the client on every frame. This is basically the same as how we handled the players. For many games, such an approach is perfectly adequate.

## bullets_delta.py
In the delta approach, we send only the changes to the bullets list. Since every bullet can only move straight at a fixed speed, the client can handle the movement of the bullets themselves as long as they are notified of every new bullet that's added and every old bullet that is removed. In games where there are a large number of bullets flying around, this can be more efficient than sending the position of all the bullets on every frame.

In the simple approach, the client always receive the position of all the bullets, so it doesn't matter if it miss one message as the next message will overwite it. But with the delta method, we cannot miss even a single message, so we need to set **queue** to **True** when sending the message, and the client will need to keep reading until there are no more messages in the queue. To identify which bullet to remove, we will also need to tag each bullet with a unique id. 

**Caution**: In an actual game, the host may not run at the same frame rate as the clients! This may cause the bullet to move faster for one player and slower for another. To prevent this, take the time step into account when moving the bullet (...see the Pygame Zero **update(dt)** documentations).

**Caution**: A newly joined player may not see the bullets that are already in the air. You can resolve this by having the client put in an initial request for "bullets" when they first join (...see static_objects.py). But depending on your game, this may not matter (eg. if game only start when all players are in).

**Tips**: Don't optimize unnecessarily. If the simple approach works fine, you may want to just use that.