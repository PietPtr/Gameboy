import memory as m

A = 0
AF = 0
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

interrupts = { "v-blank": 0, "lcd_stat": 1, "timer": 2, "serial": 3, "joypad": 4}


regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

pc = 256
ime = 0
cycle = 0

def run():
    global pc, sp, cycle

    while True:
        op = m.read(pc)
        if (cycle >> 22 & 1 == 1):
            break
        # input()
        if op == 0x0:
            nop()
        elif op == 0x1:
            loadi16(BC)
        elif op == 0x2:
            loadto((BC), A)
        elif op == 0x3:
            inc16(BC)
        elif op == 0x4:
            inc8(B)
        elif op == 0x5:
            dec8(B)
        elif op == 0x6:
            loadi8(B)
        elif op == 0x7:
            rlca()
        elif op == 0x8:
            loadi16(SP)
        elif op == 0x9:
            add16s(HL, BC)
        elif op == 0xa:
            loadfrom(A, (BC))
        elif op == 0xb:
            dec16(BC)
        elif op == 0xc:
            inc8(C)
        elif op == 0xd:
            dec8(C)
        elif op == 0xe:
            loadi8(C)
        elif op == 0xf:
            rrca()

        elif op == 0x11:
            loadi16(DE)
        elif op == 0x12:
            loadto((DE), A)
        elif op == 0x13:
            inc16(DE)
        elif op == 0x14:
            inc8(D)
        elif op == 0x15:
            dec8(D)
        elif op == 0x16:
            loadi8(D)
        elif op == 0x17:
            rla()
        elif op == 0x18:
            jumpr()
        elif op == 0x19:
            add16s(HL, DE)
        elif op == 0x1a:
            loadfrom(A, (DE))
        elif op == 0x1b:
            dec16(DE)
        elif op == 0x1c:
            inc8(E)
        elif op == 0x1d:
            dec8(E)
        elif op == 0x1e:
            loadi8(E)
        elif op == 0x1f:
            rra()
        elif op == 0x20:
            jumprf(m.read(pc))
        elif op == 0x21:
            loadi16(HL)
        elif op == 0x22:
            loadtoc('+')
        elif op == 0x23:
            inc16(HL)
        elif op == 0x24:
            inc8(H)
        elif op == 0x25:
            dec8(H)
        elif op == 0x26:
            loadi8(H)

        elif op == 0x28:
            jumprf(m.read(pc))
        elif op == 0x29:
            add16s(HL, HL)
        elif op == 0x2a:
            loadfromc('+')
        elif op == 0x2b:
            dec16(HL)
        elif op == 0x2c:
            inc8(L)
        elif op == 0x2d:
            dec8(L)
        elif op == 0x2e:
            loadi8(L)
        elif op == 0x2f:
            cpl()
        elif op == 0x30:
            jumprf(m.read(pc))
        elif op == 0x31:
            loadi16(SP)
        elif op == 0x32:
            loadtoc('-')
        elif op == 0x33:
            inc16(SP)
        elif op == 0x34:
            incat((HL))
        elif op == 0x35:
            decat((HL))
        elif op == 0x36:
            loadiat((HL))
        elif op == 0x37:
            update(1, 4, n=0, h=0, c=1)
        elif op == 0x38:
            jumprf(m.read(pc))
        elif op == 0x39:
            add16s(HL, SP)
        elif op == 0x3a:
            loadfromc('-')
        elif op == 0x3b:
            dec16(SP)
        elif op == 0x3c:
            inc8(A)
        elif op == 0x3d:
            dec8(A)
        elif op == 0x3e:
            loadi8(A)
        elif op == 0x3f:
            update(1, 4, n=0, h=0, c=int(not c()))
        elif op == 0x40:
            load(B, B)
        elif op == 0x41:
            load(B, C)
        elif op == 0x42:
            load(B, D)
        elif op == 0x43:
            load(B, E)
        elif op == 0x44:
            load(B, H)
        elif op == 0x45:
            load(B, L)
        elif op == 0x46:
            loadfrom(B, (HL))
        elif op == 0x47:
            load(B, A)
        elif op == 0x48:
            load(C, B)
        elif op == 0x49:
            load(C, C)
        elif op == 0x4a:
            load(C, D)
        elif op == 0x4b:
            load(C, E)
        elif op == 0x4c:
            load(C, H)
        elif op == 0x4d:
            load(C, L)
        elif op == 0x4e:
            loadfrom(C, (HL))
        elif op == 0x4f:
            load(C, A)
        elif op == 0x50:
            load(D, B)
        elif op == 0x51:
            load(D, C)
        elif op == 0x52:
            load(D, D)
        elif op == 0x53:
            load(D, E)
        elif op == 0x54:
            load(D, H)
        elif op == 0x55:
            load(D, L)
        elif op == 0x56:
            loadfrom(B, (HL))
        elif op == 0x57:
            load(D, A)
        elif op == 0x58:
            load(E, B)
        elif op == 0x59:
            load(E, C)
        elif op == 0x5a:
            load(E, D)
        elif op == 0x5b:
            load(E, E)
        elif op == 0x5c:
            load(E, H)
        elif op == 0x5d:
            load(E, L)
        elif op == 0x5e:
            loadfrom(E, (HL))
        elif op == 0x5f:
            load(E, A)
        elif op == 0x60:
            load(H, B)
        elif op == 0x61:
            load(H, C)
        elif op == 0x62:
            load(H, D)
        elif op == 0x63:
            load(H, E)
        elif op == 0x64:
            load(H, H)
        elif op == 0x65:
            load(H, L)
        elif op == 0x66:
            loadfrom(H, (HL))
        elif op == 0x67:
            load(H, A)
        elif op == 0x68:
            load(L, B)
        elif op == 0x69:
            load(L, C)
        elif op == 0x6a:
            load(L, D)
        elif op == 0x6b:
            load(L, E)
        elif op == 0x6c:
            load(L, H)
        elif op == 0x6d:
            load(L, L)
        elif op == 0x6e:
            loadfrom(L, (HL))
        elif op == 0x6f:
            load(L, A)
        elif op == 0x70:
            loadto((HL), B)
        elif op == 0x71:
            loadto((HL), C)
        elif op == 0x72:
            loadto((HL), D)
        elif op == 0x73:
            loadto((HL), E)
        elif op == 0x74:
            loadto((HL), H)
        elif op == 0x75:
            loadto((HL), L)
        # elif op == 0x76:
        # HALT
        elif op == 0x77:
            loadto((HL), A)
        elif op == 0x78:
            load(A, B)
        elif op == 0x79:
            load(A, C)
        elif op == 0x7a:
            load(A, D)
        elif op == 0x7b:
            load(A, E)
        elif op == 0x7c:
            load(A, H)
        elif op == 0x7d:
            load(A, L)
        elif op == 0x7e:
            loadfrom(A, (HL))
        elif op == 0x7f:
            load(A, A)
        elif op == 0x80:
            alu8(add, readReg(B), 4)
        elif op == 0x81:
            alu8(add, readReg(C), 4)
        elif op == 0x82:
            alu8(add, readReg(D), 4)
        elif op == 0x83:
            alu8(add, readReg(E), 4)
        elif op == 0x84:
            alu8(add, readReg(H), 4)
        elif op == 0x85:
            alu8(add, readReg(L), 4)
        elif op == 0x86:
            alu8(add, m.read(readRegs(HL)), 8)
        elif op == 0x87:
            alu8(add, readReg(A), 4)
        elif op == 0x88:
            alu8(adc, readReg(B), 4)
        elif op == 0x89:
            alu8(adc, readReg(C), 4)
        elif op == 0x8a:
            alu8(adc, readReg(D), 4)
        elif op == 0x8b:
            alu8(adc, readReg(E), 4)
        elif op == 0x8c:
            alu8(adc, readReg(H), 4)
        elif op == 0x8d:
            alu8(adc, readReg(L), 4)
        elif op == 0x8e:
            alu8(adc, m.read(readRegs(HL)), 8)
        elif op == 0x8f:
            alu8(adc, readReg(A), 4)
        elif op == 0x90:
            alu8(sub, readReg(B), 4)
        elif op == 0x91:
            alu8(sub, readReg(C), 4)
        elif op == 0x92:
            alu8(sub, readReg(D), 4)
        elif op == 0x93:
            alu8(sub, readReg(E), 4)
        elif op == 0x94:
            alu8(sub, readReg(H), 4)
        elif op == 0x95:
            alu8(sub, readReg(L), 4)
        elif op == 0x96:
            alu8(sub, m.read(readRegs(HL)), 8)
        elif op == 0x97:
            alu8(sub, readReg(A), 4)
        elif op == 0x98:
            alu8(sbc, readReg(B), 4)
        elif op == 0x99:
            alu8(sbc, readReg(C), 4)
        elif op == 0x9a:
            alu8(sbc, readReg(D), 4)
        elif op == 0x9b:
            alu8(sbc, readReg(E), 4)
        elif op == 0x9c:
            alu8(sbc, readReg(H), 4)
        elif op == 0x9d:
            alu8(sbc, readReg(L), 4)
        elif op == 0x9e:
            alu8(sbc, m.read(readRegs(HL)), 8)
        elif op == 0x9f:
            alu8(sbc, readReg(A), 4)
        elif op == 0xa0:
            alu8(and_, readReg(B), 4)
        elif op == 0xa1:
            alu8(and_, readReg(C), 4)
        elif op == 0xa2:
            alu8(and_, readReg(D), 4)
        elif op == 0xa3:
            alu8(and_, readReg(E), 4)
        elif op == 0xa4:
            alu8(and_, readReg(H), 4)
        elif op == 0xa5:
            alu8(and_, readReg(L), 4)
        elif op == 0xa6:
            alu8(and_, m.read(readRegs(HL)), 8)
        elif op == 0xa7:
            alu8(and_, readReg(A), 4)
        elif op == 0xa8:
            alu8(xor, readReg(B), 4)
        elif op == 0xa9:
            alu8(xor, readReg(C), 4)
        elif op == 0xaa:
            alu8(xor, readReg(D), 4)
        elif op == 0xab:
            alu8(xor, readReg(E), 4)
        elif op == 0xac:
            alu8(xor, readReg(H), 4)
        elif op == 0xad:
            alu8(xor, readReg(L), 4)
        elif op == 0xae:
            alu8(xor, m.read(readRegs(HL)), 8)
        elif op == 0xaf:
            alu8(xor, readReg(A), 4)
        elif op == 0xb0:
            alu8(or_, readReg(B), 4)
        elif op == 0xb1:
            alu8(or_, readReg(C), 4)
        elif op == 0xb2:
            alu8(or_, readReg(D), 4)
        elif op == 0xb3:
            alu8(or_, readReg(E), 4)
        elif op == 0xb4:
            alu8(or_, readReg(H), 4)
        elif op == 0xb5:
            alu8(or_, readReg(L), 4)
        elif op == 0xb6:
            alu8(or_, m.read(readRegs(HL)), 8)
        elif op == 0xb7:
            alu8(or_, readReg(A), 4)
        elif op == 0xb8:
            alu8(cp, readReg(B), 4)
        elif op == 0xb9:
            alu8(cp, readReg(C), 4)
        elif op == 0xba:
            alu8(cp, readReg(D), 4)
        elif op == 0xbb:
            alu8(cp, readReg(E), 4)
        elif op == 0xbc:
            alu8(cp, readReg(H), 4)
        elif op == 0xbd:
            alu8(cp, readReg(L), 4)
        elif op == 0xbe:
            alu8(cp, m.read(readRegs(HL)), 8)
        elif op == 0xbf:
            alu8(cp, readReg(A), 4)
        elif op == 0xc0:
            retff(op)
        elif op == 0xc1:
            pop(BC)
        elif op == 0xc2:
            jumpff(op)
        elif op == 0xc3:
            jump()
        elif op == 0xc4:
            callff(op)
        elif op == 0xc5:
            push(BC)
        elif op == 0xc6:
            alu8(sub, m.read(pc+1), 8, 2)
        elif op == 0xc7:
            rst(0x00)
        elif op == 0xc8:
            retff()
        elif op == 0xc9:
            ret()
        elif op == 0xca:
            jumpff(op)

        elif op == 0xcc:
            callff(op)
        elif op == 0xcd:
            call()
        elif op == 0xce:
            alu(adc, m.read(pc+1), 8, 2)
        elif op == 0xcf:
            rst(0x08)
        elif op == 0xd0:
            retff(op)
        elif op == 0xd1:
            pop(DE)
        elif op == 0xd2:
            jumpff(op)
        elif op == 0xd3:
            nofunction()
        elif op == 0xd4:
            callff(op)
        elif op == 0xd5:
            push(DE)
        elif op == 0xd6:
            alu8(sub, m.read(pc+1), 8, 2)
        elif op == 0xd7:
            rst(0x10)
        elif op == 0xd8:
            retff(op)

        elif op == 0xda:
            jumpff(op)
        elif op == 0xdb:
            nofunction()
        elif op == 0xdc:
            callff(op)
        elif op == 0xdd:
            nofunction()
        elif op == 0xde:
            alu8(sbc, m.read(pc+1), 8, 2)
        elif op == 0xdf:
            rst(0x18)
        elif op == 0xe0:
            ldh_ia(m.read(pc+1))
        elif op == 0xe1:
            pop(HL)
        elif op == 0xe2:
            ldh_ia(readReg(C))
        elif op == 0xe3:
            nofunction()
        elif op == 0xe4:
            nofunction();
        elif op == 0xe5:
            push(HL)
        elif op == 0xe6:
            alu8(and_, m.read(pc+1), 8, 2)
        elif op == 0xe7:
            rst(0x20)
        elif op == 0xe9:
            jumpto()

        elif op == 0xeb:
            nofunction()
        elif op == 0xec:
            nofunction()
        elif op == 0xed:
            nofunction()
        elif op == 0xee:
            alu8(xor, m.read(pc+1), 8, 2)
        elif op == 0xef:
            rst(0x28)
        elif op == 0xf0:
            ldh_ai(m.read(pc+1))
        elif op == 0xf1:
            pop(AF)
        elif op == 0xf2:
            ldh_ai(readReg(C))

        elif op == 0xf4:
            nofunction
        elif op == 0xf5:
            push(AF)
        elif op == 0xf6:
            alu8(or_, m.read(pc+1), 8, 2)
        elif op == 0xf7:
            rst(0x30)

        elif op == 0xf9:
            ldhlsp()

        elif op == 0xfc:
            nofunction()
        elif op == 0xfd:
            nofunction()
        elif op == 0xfe:
            alu8(cp, m.read(pc+1), 8, 2)
        elif op == 0xff:
            rst(0x38)

        else:
            print(hex(op), "not implemented.")
            nop()

# -------------
# ---- Ops ----
# -------------

# --- Loads --------------------------------------------------------------------
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

# LD A, (HL+) and LD A, (HL-)
def loadfromc(change):
    assert change == '+' or change == '-'
    addr = readRegs(HL)
    value = m.read(addr)
    writeReg(A, value)

    if change == '+':
        inc16(HL)
    elif change == '-':
        dec16(HL)

    update(1, 8)

# LD (HL+), A and LD (HL-), A
def loadtoc(change):
    assert change == '+' or change == '-'
    addr = readRegs(HL)
    value = readReg(A)
    m.write(addr, value)

    if change == '+':
        inc16(HL)
    elif change == '-':
        dec16(HL)

    update(1, 8)

def ldh_ia(value):
    addr = 0xFF00 & value
    m.write(addr, readReg(A))

    update(2, 12)

def ldh_ai(value):
    addr = 0xFF00 & value
    writeReg(A, m.read(addr))

    update(2, 12)

def ldhlsp():
    writeRegs(SP, readRegs(HL))
    update(1, 8)

# --- ALU stuffjes -------------------------------------------------------------

def rlca():
    a = readReg(A)
    bit7 = (a >> 7) & 1
    a = ((a << 1) & 255) | (a >> 7)
    writeReg(A, a)

    update(1, 4, zerocheck=a, n=0, h=0, c=bit7)

def rla():
    a = readReg(A)
    bit7 = (a >> 7) & 1
    a = (((a << 1) | c()) & 255)
    writeReg(A, a)

    update(1, 4, zerocheck=a, n=0, h=0, c=bit7)

def rrca():
    a = readReg(A)
    bit0 = a & 1
    a = (a >> 1) | (bit0 << 7)
    writeReg(A, a)

    update(1, 4, zerocheck=a, n=0, h=0, c=bit0)

def rra():
    a = readReg(A)
    bit0 = a & 1
    bit7 = c()
    a = (bit7 << 7) | (a >> 1)
    writeReg(A, a)
    update(1, 4, zerocheck=a, n=0, h=0, c=bit0)

def cpl():
    writeReg(A, ~(readReg(A)) & 0xff)
    update(1, 4, n=1, h=1)

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

def add16s(regs1, regs2):
    value1 = readRegs(regs1)
    value2 = readRegs(regs2)
    newv = value1 + value2

    writeRegs(regs1, newv)

    # H flag likely bullshit
    update(1, 8, n=0, h=(int(newv > 2**11)), c=(newv >> 16))

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


# --- ALU (80 - BF) ------------------------------------------------------------
def alu8(func, value, cyc, pcinc=1):
    writeReg(A, func(readReg(A), value, cyc, pcinc))

def add(a, b, cyc, pcinc):
    newv = a + b
    update(pcinc, cyc, zerocheck=(newv & 255), n=0, h=((newv >> 4) & 1), c=(newv >> 8))
    return newv

def adc(a, b, cyc, pcinc):
    newv = a + b + c()
    update(pcinc, cyc, zerocheck=newv, n=0, h=((newv >> 4) & 1), c=(newv >> 8))
    return newv

def sub(a, b, cyc, pcinc):
    newv = a - b
    update(pcinc, cyc, zerocheck=(newv & 255), n=1, h=((~newv >> 4) & 1), c=(~(newv >> 8) & 1))
    return newv

def sbc(a, b, cyc, pcinc):
    newv = a - b - c()
    update(pcinc, cyc, zerocheck=newv, n=1, h=((~newv >> 4) & 1), c=(~(newv >> 8) & 1))
    return newv

def and_(a, b, cyc, pcinc):
    newv = a & b
    update(pcinc, cyc, zerocheck=newv, n=0, h=1, c=0)
    return newv

def xor(a, b, cyc, pcinc):
    newv = a ^ b
    update(pcinc, cyc, zerocheck=newv, n=0, h=0, c=0)
    return newv

def or_(a, b, cyc, pcinc):
    newv = a | b
    update(pcinc, cyc, zerocheck=newv, n=0, h=0, c=0)
    return newv

def cp(a, b, cyc, pcinc):
    newv = a
    update(pcinc, cyc, zerocheck=(newv & 255), n=1, h=((~newv >> 4) & 1), c=int(a < b))
    return a

# --- Jumps --------------------------------------------------------------------
def jump():
    # lsb first, apparently
    addr = (m.read(pc+2) << 8) | m.read(pc+1)
    update(3, 16, newpc=addr)


def jumpff(op):
    assert op in [0xc2, 0xca, 0xd2, 0xda]
    dojump = False

    if op == 0xc2:
        dojump = not bool(z())
    elif op == 0xca:
        dojump = bool(z())
    elif op == 0xd2:
        dojump = not bool(c())
    elif op == 0xda:
        dojump = bool(c())

    if dojump:
        jump()
    else:
        update(3, 12)

def jumpto():
    addr = readRegs(HL)
    update(1, 4, newpc=addr)

def jumpr():
    update(m.read(pc+1), 12)

def jumprf(op):
    assert op in [0x20, 0x30, 0x28, 0x38]
    dojump = False

    if op == 0x20:
        dojump = not bool(z())
    elif op == 0x28:
        dojump = bool(z())
    elif op == 0x30:
        dojump = not bool(c())
    elif op == 0x38:
        dojump = bool(c())

    if dojump:
        jumpr()
    else:
        update(2, 8)


def call():
    pushc(pc+1)
    addr = (m.read(pc+2) << 8) | m.read(pc+1)
    update(3, 24, newpc=addr)

def callff(op):
    assert op in [0xc4, 0xcc, 0xd4, 0xdc]
    docall = False

    if op == 0xc4:
        docall = not bool(z())
    elif op == 0xcc:
        docall = bool(z())
    elif op == 0xd4:
        docall = not bool(c())
    elif op == 0xdd:
        docall = bool(c())

    if docall:
        call()
    else:
        update(3, 12)


def ret():
    addr = popc()
    update(1, 16, newpc=addr)

def retff(op):
    assert op in [0xc0, 0xc8, 0xd0, 0xd8]
    doreturn = False

    if op == 0xc0:
        doreturn = not bool(z())
    elif op == 0xc8:
        doreturn = bool(z())
    elif op == 0xd0:
        doreturn = not bool(c())
    elif op == 0xd8:
        doreturn = bool(c())

    if doreturn:
        call()
    else:
        update(1, 8)


def rst(addr):
    pushc(pc)
    update(1, 16, newpc=addr)

# --- Misc ---------------------------------------------------------------------

# WARNING: this function decreases the stack pointer!
def pushc(value):
    writeRegs(SP, readRegs(SP) - 2)
    addr = readRegs(SP)
    # BUG: should maybe be the other way around
    m.write(addr, value & 255)
    m.write(addr + 1, value >> 8)


def push(regs):
    pushc(readRegs(regs))

    update(1, 16)

# WARNING: this function has the side effect of increasing the SP!
def popc():
    addr = readRegs(SP)
    lsbits = m.read(addr)
    msbits = m.read(addr + 1) << 8
    writeRegs(SP, readRegs(SP) + 2)
    return msbits & lsbits

def pop(regs):
    writeRegs(regs, popc())

    update(1, 12)

def nofunction():
    raise ValueError("Instruction does not exist.")

# -----------------
# ---- Helpers ----
# -----------------

def update(pcinc, cycles, zerocheck=-1, n=-1, h=-1, c=-1, newpc=-1):
    global pc, cycle

    if zerocheck != -1:
        zero(zerocheck)

    setFlags(n=n, h=h, c=c)
    if newpc == -1:
        pc = (pc + pcinc) & 0b1111111111111111
    else:
        pc = newpc
    cycle += cycles

    # printState()

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
        f = f & (0b11100000)

    regs[F] = f

def z():
    return (readReg(F) >> 7) & 1

def n():
    return (readReg(F) >> 6) & 1

def h():
    return (readReg(F) >> 5) & 1

def c():
    return (readReg(F) >> 4) & 1

def getie(interrupt):
    return bool(m.read(0xffff) >> (interrupts[interrupt]) & 1)

def getif(interrupt):
    return bool(m.read(0xff0f) >> (interrupts[interrupt]) & 1)

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
    assert reg % 2 == 0

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
