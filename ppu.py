import memory as m
from memlocs import *

class PPU(object):
    def __init__(self, queue):
        self.queue = queue
        self.lcd = [[0 for pixel in range(160)] for line in range(144)]
        self.last_update = 0
        self.color = 0

    def update(self, cycle):
        if cycle - self.last_update > 456:
            m.write(LY, (m.read(LY) + 1) % 154)
            line = m.read(LY)

            self.last_update = cycle - cycle % 456

            self.lcd[0][0] = int(not self.lcd[0][0])
            if line < 144:
                self.lcd[line] = [self.color for _ in range(160)]


            if line == 153:
                self.queue.put(self.lcd)
                self.color  = (self.color + 1) % 4
        # print(screen[0][0])
