#!/usr/bin/env python3

import pgzrun
from nethelper import NetNode
from pgzhelper import Collide
import random

WIDTH = 800
HEIGHT = 600
SERVER = 'localhost' # <== You may need to change this

# First player must be 'host'. Every one else must use a different value.
NAME = 'host'  # <== Change this!

# Alternatively, you can use input to ask for the player's name
# NAME = input('What is your name? (first player must be "host") : ')

tank = Actor('tank_blue')
rock = Actor('rock')

rocks = []
# Only the host will create rocks
if NAME == 'host':
    for _ in range(5):
        r = {
            'x': random.randint(100, 700),
            'y': random.randint(100, 450)
        }
        rocks.append(r)

players = {}

# Connect to the message relay server
net = NetNode()
net.connect('localhost', NAME, 'net_demo')

def add_player(name):
    players[name] = {
        'x': random.randint(100, 700),
        'y': 550,
        'angle': 0
    }

def get_controls():
    if keyboard.left:
        return [-3, 0, 180]
    elif keyboard.right:
        return [3, 0, 0]
    elif keyboard.up:
        return [0, -3, 90]
    elif keyboard.down:
        return [0, 3, 270]

def update_host():
    # Check if any of the clients are making requests
    for p in players:
        requests = net.get_msg(p, 'requests')
        # Send the rocks list if requested
        if requests == 'rocks':
            net.send_msg(p, 'rocks', rocks)

    for p in players:
        if p == 'host':
            controls = get_controls()
        else:
            # Get control info from the client
            controls = net.get_msg(p, 'control')
        if controls is not None:
            orig_x = players[p]['x']
            orig_y = players[p]['y']
            players[p]['x'] += controls[0]            
            players[p]['y'] += controls[1]            
            players[p]['angle'] = controls[2]

    # Send data to all other players
    net.send_msg('ALL', 'players', players)

def update_client():
    global players, rocks

    # Request for rocks if we don't have any
    if len(rocks) == 0:
        net.send_msg('host', 'requests', 'rocks')
    
    # When the server replies, update our rocks list
    msg = net.get_msg('host', 'rocks')
    if msg is not None:
        rocks = msg
    
    # Read and update players position
    msg = net.get_msg('host', 'players')
    if msg is not None:
        players = msg

    # Client controls
    net.send_msg('host', 'control', get_controls())

def update():
    # Run this to receive messages from the server
    net.process_recv()

    # Add player into game if not present
    for peer in net.get_peers():
        if peer not in players:
            add_player(peer)

    if NAME == 'host':
        update_host()
    else:
        update_client()

    # Run this to send all buffered messages to the server
    net.process_send()

def draw():
    screen.clear()
    for r in rocks:
        rock.x = r['x']
        rock.y = r['y']
        rock.draw()
    for p in players:
        tank.x = players[p]['x']
        tank.y = players[p]['y']
        tank.angle = players[p]['angle']
        tank.draw()
        screen.draw.text(p, (players[p]['x'], players[p]['y']))

pgzrun.go() # Must be last line
