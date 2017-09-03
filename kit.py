#!/usr/bin/env python

import argparse
import time
import colorsys
import blinkt
import random

# Animation modes
anim_mode = ['ping-pong', 'ping', 'sparkle']
hue_mode = ['rainbow', 'random', 'single']

# Initial values
NUM_LEDS = 8
DIM_FACTOR = 0.65
HUE_SPEED = 0.02
SATURATION = 1.0
SPEED = 0.07
BRIGHTNESS = 0.2

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default=anim_mode[0], const=anim_mode[0], nargs='?', choices=anim_mode, help='Anim mode, defaults to %s' % anim_mode[0])
parser.add_argument('--hue_mode', default=hue_mode[0], const=hue_mode[0], nargs='?', choices=hue_mode, help='Hue mode, defaults to %s' % hue_mode[0])
parser.add_argument('--dim_factor', default=DIM_FACTOR, type=float, help='How fast to dim the LEDs')
parser.add_argument('--hue_speed', default=HUE_SPEED, type=float, help='How fast to change the hue')
parser.add_argument('--initial_hue', default=0, type=float, help='Initial hue')
parser.add_argument('--speed', default=SPEED, type=float, help='Animation speed')
parser.add_argument('--brightness', default=BRIGHTNESS, type=float, help='LED Brightness')
args = parser.parse_args()

# Init hsl colors in hls, hue, saturation, lightness
hsl = [(0.0, 0.0, 0.0)] * NUM_LEDS

# Init animation variables
dir = 1
pos = 0
hue = float(args.initial_hue)

# Init blinkt
blinkt.set_clear_on_exit(True)
blinkt.set_brightness(args.brightness)

# Forever loop
while True:
    # Apply dimming to all LEDs
    for i in range(NUM_LEDS):
        h, s, l = hsl[i]
        hsl[i] = (h, s * args.dim_factor, l)

    # Set the current LED to full brightness
    hsl[pos] = (hue, 0.5, 1.0)
    
    # Set LEDs
    blinkt.clear()
    for i in range(8):
        h, s, l = hsl[i]
        r, g, b = colorsys.hls_to_rgb(h, s, l)
        blinkt.set_pixel(i, int(r * 255), int(g * 255), int(b * 255))
    blinkt.show()
    
    if args.mode == 'ping-pong':
        # Get the next LED
        if pos == 0:
            dir = 1
        if pos == (NUM_LEDS - 1):
            dir = -1
        pos += dir

    if args.mode == 'ping':
        if pos == (NUM_LEDS - 1):
            pos = 0
        else:
            pos += dir

    if args.mode == 'sparkle':
        pos = random.randint(0, NUM_LEDS - 1)

    # Get next hue
    if args.hue_mode == 'rainbow':
        hue = hue + HUE_SPEED
    if args.hue_mode == 'random':
        hue = random.random()
    
    time.sleep(args.speed)
