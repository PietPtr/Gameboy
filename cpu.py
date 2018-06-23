import memory as m

A = 0
F = 1
B = 2
BC = 2
C = 3
D = 4
DE = 4
E = 5
H = 6
HL = 6
L = 7

regs = [0, 0, 0, 0, 0, 0, 0, 0]

ops = \
{

}

def run():
    pc = 256
    sp = 0

    while True:
        opcode = hex(m.read(pc))
        print(opcode)

        pc += 1

def printRegs():
    names = "AFBCDEHL"
    for i in range(0, L+1):
        print(str(names[i]) + ": ", regs[i], hex(regs[i]))

def writeReg(reg, value):
    assert reg >= 2 and value < 2**8

    regs[reg] = value

def writeRegs(reg, value):
    assert reg % 2 == 0 and reg != 0 and value < 2**16

    msbits = value >> 8
    lsbits = value & 255

    regs[reg] = msbits
    regs[reg+1] = lsbits

def readRegs(reg):
    assert reg % 2 == 0 and reg < 8

    msbits = regs[reg]
    lsbits = regs[reg+1]

    value = (msbits << 8) + lsbits

    return value

def readReg(reg):
    assert reg < 8

    return regs[reg]
