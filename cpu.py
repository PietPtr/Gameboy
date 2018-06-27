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
SP = 8

# TODO: fix dat SP gewoon een register word...
regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

pc = 256
# sp = 0
cycle = 0

def run():
    global pc, sp, cycle

    while True:
        op = hex(m.read(pc))
        print(pc, op)
        # input()
        if op == "0x0":
            nop()
        elif op == "0x1":
            loadi16(BC)
        elif op == "0x2":
            loadto((BC), A)
        elif op == "0x3":
            inc16(BC)
        elif op == "0x4":
            inc8(B)
        elif op == "0x5":
            dec8(B)
        elif op == "0x6":
            loadi8(B)
        elif op == "0x7":
            rlca()
        elif op == "0x8":
            loadi16(SP)
        elif op == "0x9":
            add16s(HL, BC)
        elif op == "0xa":
            loadfrom(A, (BC))
        elif op == "0xb":
            dec16(BC)
        elif op == "0xc":
            inc8(C)
        elif op == "0xd":
            dec8(C)
        elif op == "0xe":
            loadi8(C)

        elif op == "0x11":
            loadi16(DE)
        elif op == "0x12":
            loadto((DE), A)
        elif op == "0x13":
            inc16(DE)
        elif op == "0x14":
            inc8(D)
        elif op == "0x15":
            dec8(D)
        elif op == "0x16":
            loadi8(D)

        elif op == "0x19":
            add16s(HL, DE)
        elif op == "0x1a":
            loadfrom(A, (DE))
        elif op == "0x1b":
            dec16(DE)
        elif op == "0x1c":
            inc8(E)
        elif op == "0x1d":
            dec8(E)
        elif op == "0x1e":
            loadi8(E)

        elif op == "0x21":
            loadi16(HL)

        elif op == "0x23":
            inc16(HL)
        elif op == "0x24":
            inc8(H)
        elif op == "0x25":
            dec8(H)
        elif op == "0x26":
            loadi8(H)
        
        elif op == "0x29":
            add16s(HL, HL)

        elif op == "0x2b":
            dec16(HL)
        elif op == "0x2c":
            inc8(L)
        elif op == "0x2d":
            dec8(L)
        elif op == "0x2e":
            loadi8(L)

        elif op == "0x31":
            loadi16(SP)
        elif op == "0x33":
            inc16(SP)
        elif op == "0x34":
            incat((HL))
        elif op == "0x35":
            decat((HL))
        elif op == "0x36":
            loadiat((HL))


        elif op == "0x3b":
            dec16(SP)
        elif op == "0x3c":
            inc8(A)
        elif op == "0x3d":
            dec8(A)
        elif op == "0x3e":
            loadi8(A)

        elif op == "0x40":
            load(B, B)
        elif op == "0x41":
            load(B, C)
        elif op == "0x42":
            load(B, D)
        elif op == "0x43":
            load(B, E)
        elif op == "0x44":
            load(B, H)
        elif op == "0x45":
            load(B, L)
        elif op == "0x46":
            loadfrom(B, (HL))
        elif op == "0x47":
            load(B, A)
        elif op == "0x48":
            load(C, B)
        elif op == "0x49":
            load(C, C)
        elif op == "0x4a":
            load(C, D)
        elif op == "0x4b":
            load(C, E)
        elif op == "0x4c":
            load(C, H)
        elif op == "0x4d":
            load(C, L)
        elif op == "0x4e":
            loadfrom(C, (HL))
        elif op == "0x4f":
            load(C, A)
        elif op == "0x50":
            load(D, B)
        elif op == "0x51":
            load(D, C)
        elif op == "0x52":
            load(D, D)
        elif op == "0x53":
            load(D, E)
        elif op == "0x54":
            load(D, H)
        elif op == "0x55":
            load(D, L)
        elif op == "0x56":
            loadfrom(B, (HL)) 
        elif op == "0x57":
            load(D, A)
        elif op == "0x58":
            load(E, B)
        elif op == "0x59":
            load(E, C)
        elif op == "0x5a":
            load(E, D)
        elif op == "0x5b":
            load(E, E)
        elif op == "0x5c":
            load(E, H)
        elif op == "0x5d":
            load(E, L)
        elif op == "0x5e":
            loadfrom(E, (HL))
        elif op == "0x5f":
            load(E, A)
        elif op == "0x60":
            load(H, B)
        elif op == "0x61":
            load(H, C)
        elif op == "0x62":
            load(H, D)
        elif op == "0x63":
            load(H, E)
        elif op == "0x64":
            load(H, H)
        elif op == "0x65":
            load(H, L)
        elif op == "0x66":
            loadfrom(H, (HL))
        elif op == "0x67":
            load(H, A)
        elif op == "0x68":
            load(L, B)
        elif op == "0x69":
            load(L, C)
        elif op == "0x6a":
            load(L, D)
        elif op == "0x6b":
            load(L, E)
        elif op == "0x6c":
            load(L, H)
        elif op == "0x6d":
            load(L, L)
        elif op == "0x6e":
            loadfrom(L, (HL)) 
        elif op == "0x6f":
            load(L, A)
        elif op == "0x70":
            loadto((HL), B)
        elif op == "0x71":
            loadto((HL), C)
        elif op == "0x72":
            loadto((HL), D)
        elif op == "0x73":
            loadto((HL), E)
        elif op == "0x74":
            loadto((HL), H)
        elif op == "0x75":
            loadto((HL), L)
        # elif op == "0x76":
        # HALT
        elif op == "0x77":
            loadto((HL), A)
        elif op == "0x78":
            load(A, B)
        elif op == "0x79":
            load(A, C)
        elif op == "0x7a":
            load(A, D)
        elif op == "0x7b":
            load(A, E)
        elif op == "0x7c":
            load(A, H)
        elif op == "0x7d":
            load(A, L)
        elif op == "0x7e":
            loadfrom(A, (HL))
        elif op == "0x7f":
            load(A, A)
        elif op == "0x80":
            add8s(A, B)
        elif op == "0x81":
            add8s(A, C) 
        elif op == "0x82":
            add8s(A, D) 
        elif op == "0x83":
            add8s(A, E) 
        elif op == "0x84":
            add8s(A, H) 
        elif op == "0x85":
            add8s(A, L)  

        elif op == "0x87":
            add8s(A, A) 
        elif op == "0x88":
            adc(A, B)
        elif op == "0x89":
            adc(A, C)
        elif op == "0x8a":
            adc(A, D)
        elif op == "0x8b":
            adc(A, E)
        elif op == "0x8c":
            adc(A, H)
        elif op == "0x8d":
            adc(A, L)

        elif op == "0x8f":
            adc(A, A)
        elif op == "0x90":
            subA(B)
        else:
            nop()




# -------------
# ---- Ops ----
# -------------

def nop():
    update(1, 4)

def load(toReg, fromReg):
    writeReg(toReg, readReg(fromReg))

    update(1, 4)

def loadi8(toReg):
    value = m.read(pc+1)
    writeReg(toReg, value)

    update(2, 8)

def loadi16(toRegs):
    value = (m.read(pc+2) << 8) + (m.read(pc+1))
    writeRegs(toRegs, value)

    update(3, 12)

def loadiat(regs):
    addr = readRegs(regs)
    value = m.read(pc+1)
    m.write(addr, value)

    update(2, 12)

#def loadisp():
#    value = (m.read(pc+2) << 8) + (m.read(pc+1))
#
#    update(3, 12, newsp=value)

#def loadmemtosp():
#    addr = ((m.read(pc+2)) << 8) + (m.read(pc+1))
#    value = m.read(addr)
#
#    update(3, 20, newsp=value)

def rlca():
    a = readReg(A)
    bit7 = (a >> 7) & 1
    a = ((a << 1) & 255) | (a >> 7)
    writeReg(A, a)

    update(1, 4, zerocheck=0, n=0, h=0, c=bit7)

def inc8(reg):
    value = readReg(reg) + 1
    writeReg(reg, value)

    update(1, 4, zerocheck=value, n=0, h=((value >> 4) & 1))

def dec8(reg):
    value = readReg(reg) - 1
    writeReg(reg, value)

    update(1, 4, zerocheck=value, n=1, h=((value >> 4) & 1))

def inc16(regs):
    value = readRegs(regs) + 1
    writeRegs(regs, value)

    update(1, 8)

def dec16(regs):
    value = readRegs(regs) - 1
    writeRegs(regs, value)

    update(1, 8)

def add8s(reg1, reg2):
    value1 = readReg(reg1)
    value2 = readReg(reg2)
    newv = value1 + value2

    writeReg(reg1, value1 + value2)

    # H flag likely bullshit here too
    update(1, 4, zerocheck=(newv & 255), n=0, h=((newv >> 4) & 1), c=(newv >> 8))

def subA(reg2):
    v1 = readReg(A)
    v2 = readReg(reg2)
    newv = v1 - v2
    
    writeReg(reg1, newv)

    update(1, 4, zerocheck=(newv & 255), n=1, h=(((newv & 255) >> 4) & 1), c=(newv >> 8)) 

def adc(reg1, reg2):
    v1 = readReg(reg1)
    v2 = readReg(reg2)
    newv = v1 + v2 + c()
    writeReg(reg1, newv)

    update(1, 4, zerocheck=newv, n=0, h=((newv >> 4) & 1), c=(newv >> 8))

def add16s(regs1, regs2):
    value1 = readRegs(regs1)
    value2 = readRegs(regs2)
    newv = value1 + value2

    writeRegs(regs1, newv)

    # H flag likely bullshit
    update(1, 8, n=0, h=(int(newv > 2**11)), c=(newv >> 16))

#def decsp():
#    global sp
#    update(1, 8, newsp=sp-1)
#
#def incsp():
#    global sp
#    update(1, 8, newsp=sp+1)

def incat(regs):
    addr = readRegs(regs)
    value = m.read(addr) + 1
    m.write(addr, value)

    update(1, 12, zerocheck=value, n=0, h=((value >> 4) & 1))

# Decrements the value stored at the address contained by the register
# Requires a double register
def decat(regs):
    addr = readRegs(regs)
    value = m.read(addr) - 1
    m.write(addr, value)

    update(1, 12, zerocheck=value, n=1, h=((value >> 4) & 1))

# Loads the value stored at the address contained by the register
# Requires a double register for specifying address
# r = (HL)    LD B,(HL)
def loadfrom(reg, regs):
    addr = readRegs(regs)
    value = m.read(addr)
    writeReg(reg, value)

    update(1, 8)
# (HL) = r   LD (HL),B
def loadto(regs, reg):
    addr = readRegs(regs)
    value = readReg(reg)
    m.write(addr, value)

    update(1, 8)


# -----------------
# ---- Helpers ----
# -----------------

def update(pcinc, cycles, zerocheck=-1, n=-1, h=-1, c=-1):
    global pc, cycle

    # print(pc, cycle, bin(regs[F]), sp)

    if zerocheck != -1:
        zero(zerocheck)

    #if newsp != -1:
    #    sp = newsp & 0b1111111111111111

    setFlags(n=n, h=h, c=c)

    pc = (pc + pcinc) & 0b1111111111111111
    cycle += cycles

    # print(pc, cycle, bin(regs[F]), sp)
    printState()

def zero(value):
    if value == 0:
        setFlags(z=1)
    else:
        setFlags(z=0)

def setFlags(z=-1, n=-1, h=-1, c=-1):
    assert z >= -1 and z <= 1 and \
           n >= -1 and n <= 1 and \
           h >= -1 and h <= 1 and \
           c >= -1 and h <= 1

    global F
    f = readReg(F)

    if z == 1:
        f = f | (0b10000000)
    elif z == 0:
        f = f & (0b01110000)

    if n == 1:
        f = f | (0b01000000)
    elif n == 0:
        f = f & (0b10110000)

    if h == 1:
        f = f | (0b00100000)
    elif h == 0:
        f = f & (0b11010000)

    if c == 1:
        f = f | (0b00010000)
    elif c == 0:
        f = f | (0b11100000)

    regs[F] = f

def z():
    return (readReg(F) >> 7) & 1

def n():
    return (readReg(F) >> 6) & 1

def h():
    return (readReg(F) >> 5) & 1

def c():
    return (readReg(F) >> 4) & 1

def to16bitnum(lsbits, msbits):
    return (msbits << 8) + lsbits

def printState():
    printRegs()
    printFlags()

def printFlags():
    f = readReg(F)
    print("Flags: z=" + str((f >> 7) & 1), end=", ")
    print("n=" + str((f >> 6) & 1), end=", ")
    print("h=" + str((f >> 5) & 1), end=", ")
    print("c=" + str((f >> 4) & 1))

def printRegs():
    names = "AFBCDEHL"
    print("Registers: ", end="")
    for i in range(0, L+1):
        print(str(names[i]) + ":", "{0:#0{1}x}, ".format(regs[i], 4), end="")
    print()

    print("Double registers: ", end="") 
    names = ["", "BC", "DE", "HL", "SP"]
    for i in range(1, 5):
        print(str(names[i]) + ":", "{0:#0{1}x}, ".format(readRegs(i*2), 6), end="")
    print()

def writeA(value):
    global A
    regs[A] = value

def writeReg(reg, value):
    assert reg < 8

    value = value & 255

    regs[reg] = value

def writeRegs(reg, value):
    assert reg % 2 == 0 and reg != 0

    value = value & 65535

    msbits = value >> 8
    lsbits = value & 255

    regs[reg] = msbits
    regs[reg+1] = lsbits

def readRegs(reg):
    assert reg % 2 == 0 and reg <= 8

    msbits = regs[reg]
    lsbits = regs[reg+1]

    value = (msbits << 8) + lsbits

    return value

def readReg(reg):
    assert reg <= 8

    return regs[reg]
