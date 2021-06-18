# nethelper
Python module providing simple game networking

This module was originally created to facilitate a class on creating multiplayer games in Pygame Zero. It designed to be simple for beginner programmers to use, and will not be as full featured or efficient as other networking libraries.

## Features
* Work over the internet or LAN
* Designed specifically for game networking (...send and receive never blocks, messages are batched)
* Very simple to use
* No dependencies or installation. Just download and import one file.

## How it Works


## Starting the Server
For this module to work, you will require a message relay server. To start the server, simply run the module as a script.

```
python3 nethelper.py -g net_demo
```

This will start the server and configure it to recognize the "net_demo" group. Your game can use any string as a group name, as long as it is recognized by the server.

**IMPORTANT : Your server must be accessible on its listening port (default to 65042).**
**Read the section on "Server Access" for some tips on how to set this up.**

You can also configure the server to recognize multiple groups.

```
python3 nethelper.py -g demo1 demo2 demo3
```

This will configure the server to recognize 3 groups; "demo1", "demo2", and "demo3". Games can only talk to others in the same group, so a game that's on "demo1" will not be able to talk to a game on "demo2".

You can also write your group names into a file and provide the filename on the command line.

```
python3 nethelper.py -f file_containing_groups.txt
```

Each group name must be on it's own line, and lines starting with # are ignored.

To see more options, run...

```
python3 nethelper.py -h
```

## Game Setup

First, import the **NetNode** class.

```
from nethelper import NetNode
```

Next, create a NetNode object and connect to the message relay server (...make sure to start it first).

```
net = NetNode()
net.connect('localhost', 'foo', 'net_demo')
```

Now your game should be connected to the server as a node. Every node in the same group can talk to each other via the message relay server.

**localhost** is what I'm using here as the server address, but that will only work if the game is running on the same computer as the server. If the game is not running on the same computer as the server, you'll want to replace **localhost** with the IP address or domain name of the server.

**foo** is the name that this node is identifying itself as. You can use any string as a name, as long as every node in the same group has a unique name.

**net_demo** is the group that I am are connecting to. The server must be configured to recognize this group, and nodes can only communicate with other computers in the same group.

In your **update()** function, you should start with a...

```
net.process_recv()
```

This will receive all the incoming messages server, making them available to read.

To send a message to other nodes, use...

```
net.send_msg('bar', 'pp', players_pos)
```

This will send a message with the title **pp** to the node named **bar**. The content of the message will be the value of the variable **players_pos**.

To send to all nodes in the group, use **ALL** as the destination name.

```
net.send_msg('ALL', 'pp', players_pos)
```

To read incoming messages, use...

```
msg = net.get_msg('bar', 'controls')
```

This will get the content of the message titled **controls** from **bar**, and put it in the **msg** variable. If no messages are available, **get_msg** will return **None**.

Finally, you should end your **update()** function with a...

```
net.process_send()
```

This will push all the sent messages to the server. If you do not run **process_send()**, your messages will never get sent out.

One last useful function is **net.get_peers()**. This function will return a list containing the names of all nodes in your group.

## More Documentations

See Wiki page on Github for detailed documentations.

The Wiki docs are generated from the docstrings in the nethelper.py source, so you can also read that.

## Examples

As nethelper is designed for use with games, both of these examples uses Pygame Zero. However, nothing in nethelper requires Pygame Zero and it can also be used on its own without any other modules. A message relay server must be running and configured for group "net_demo" for the example to work.

Message sender:

```
import pgzrun
from nethelper import NetNode

net = NetNode()
net.connect('localhost', 'Tom', 'net_demo')

def update():
    if keyboard.up:
        net.send_msg('Jerry', 'controls', 'up')
    elif keyboard.down:
        net.send_msg('Jerry', 'controls', 'down')

    net.process_send()

pgzrun.go()
```

Message receiver:

```
import pgzrun
from nethelper import NetNode

net = NetNode()
net.connect('localhost', 'Jerry', 'net_demo')

msg = None
def update():
    global msg
    
    net.process_recv()
    msg = net.get_msg('Tom', 'controls')    

def draw():
    if msg:
        screen.clear()
        screen.draw.text(msg, (100,100), color="white")

pgzrun.go()
```

See the examples folder for more complete examples of games using nethelper.

## Server Access

You can run the message relay server on either a computer within your own LAN, or on an internet server (...typically through a cloud service).

### Computer within LAN

Running it on a computer within your own LAN can be faster and uses no internet bandwidth, but this may be blocked by your firewall or router. To open up access through the firewall, you need to allow incoming connections on **TCP port 65042**.

#### On Linux (Including Raspberry Pi)

On the command line, run...

```
sudo ufw allow 65042
```

### On Windows

Visit this link for instructions https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html

#### On Mac

Visit this link for instructions https://www.macworld.co.uk/how-to/how-open-specific-ports-in-os-x-1010-firewall-3616405/

#### Router Blocking Access

If the connection is being blocked by your router, you'll likely need to disable an option typically named "Wireless Isolation", "Client Isolation", or "Wireless client separation". There are many ways to configure a router to block client-to-client communications, so if that doesn't work, you'll need to consult your router manual or your network administrator for help. Alternatively, use an internet server instead.

### Internet Server

Running the message relay server on the internet may be slower (ie. laggy), but will allow players on different networks to play together (eg. for an online class where every student is at their own home). It can also have less issues with network configurations. You will need to pay for a cloud hosting service, but these are not expensive (...typically 1 cent per hour).

Most cloud services including Amazon AWS, DigitalOcean, and Linode, will do just fine. The following instructions are based on DigitalOcean.

1. Register for an account on [DigitalOcean](https://www.digitalocean.com)
2. Create a new **Droplet**:
    * Choose **Ubuntu** as your distribution.
    * The cheapest plan should be sufficient for dozens of students.
    * Choose a datacenter region that is close to you.
    * For Authentication, a password will be sufficient (...no sensitive data will be stored on the server)
3. Wait for your droplet to be ready (...this may take a few minutes), then login using an SSH client and your password.
4. Download nethelper.py using the command:
```
wget https://raw.githubusercontent.com/QuirkyCort/nethelper/main/nethelper.py
```
5. Open the port on the firewall using:
```
sudo ufw allow 65042
```
6. Run nethelper.py (...see **Starting the Server** for details)