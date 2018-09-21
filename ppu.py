import memory as m
from memlocs import *
import time

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

            self.draw_line(line)

            try:
                self.queue.get_nowait()
            except Exception:
                self.queue.put(self.lcd)


    def draw_line(self, line):
        if line < 144:
            self.lcd[line] = [self.get_bg_pix(pixel, line) for pixel in range(160)]


    def get_bg_pix(self, pixel, line):
        scroll_x = m.read(SCX)
        scroll_y = m.read(SCY)

        # coordinates on the background picture
        coords = x, y = (pixel + scroll_x, line + scroll_y)

        tile_coords = tx, ty = (x // 8, y // 8)

        bg_tile_map_address = 0x9800 if (m.read(LCDC) >> 3 & 1) == 0 else 0x9c00
        tile_address = bg_tile_map_address + ty * 32 + tx

        bg_window_data_address = 0x8800 if (m.read(LCDC) >> 4 & 1) == 0 else 0x8000
        data_address = bg_window_data_address + m.read(tile_address) * 16
        lsb = m.read(data_address + (y % 8) * 2)
        msb = m.read(data_address + (y % 8) * 2 + 1)

        byte = 7 - pixel % 8
        color_id = (msb >> byte & 1) << 1 | (lsb >> byte & 1)

        palette = m.read(BGP)
        color = palette >> (color_id * 2) & 3

        return color
