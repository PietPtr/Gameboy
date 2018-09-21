import cpu
import memory
from array import array
import sys, os
import renderer
from ppu import PPU
from threading import Thread
from queue import Queue
import time

data = array("B")

if len(sys.argv) < 2:
    print("pls give rom name")
    sys.exit()

filename = sys.argv[1]
filesize = os.stat(filename).st_size

print("Loading", filename, " (" + str(filesize) + " bytes)")

with open(filename, 'rb') as f:
    data.fromfile(f, filesize)

queue = Queue()

render_thread = Thread(target=renderer.render, args=(queue,))
render_thread.start()

memory.loadROM(data)
memory.loadBootstrap()

ppu = PPU(queue)

cpu.run(ppu)
