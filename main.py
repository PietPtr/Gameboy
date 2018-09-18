import cpu
import memory
from array import array
import sys, os

data = array("B")

if len(sys.argv) < 2:
    print("pls give rom name")
    sys.exit()

filename = sys.argv[1]
filesize = os.stat(filename).st_size

print("Loading", filename, " (" + str(filesize) + " bytes)")

with open(filename, 'rb') as f:
    data.fromfile(f, filesize)

memory.loadROM(data)
memory.loadBootstrap()
cpu.run()
