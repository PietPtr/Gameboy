import memory as m
from memlocs import *

screen = [[0 for pixel in range(0, 160)] for line in range(0, 144)]

last_update = 0

def update(cycle):
    global last_update, screen
    if cycle - last_update > 456:
        m.write(LY, (m.read(LY) + 1) % 154)
        last_update = cycle - cycle % 456
