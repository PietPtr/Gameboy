from array import array

memory = [0 for x in range(0, 2**16)]

def loadROM(data):
    # TODO: add switching ROM banks
    i = 0
    for b in data:
        memory[i] = b
        i += 1


def read(addr):
    # TODO: add memory mapped crap like IO
    return memory[addr]

def write(addr, value):
    # TODO: add write protection and stuff
    memory[addr] = value
