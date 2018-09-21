import memory as m
import ppu
from memlocs import *
import json
import time

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
intrs_ordered = ["v-blank",
                 "lcd_stat",
                 "timer",
                 "serial",
                 "joypad"]
intr_addrs = {
    intrs_ordered[0]: 0x40,
    intrs_ordered[1]: 0x48,
    intrs_ordered[2]: 0x50,
    intrs_ordered[3]: 0x58,
    intrs_ordered[4]: 0x60}

# regs = [0x01, 0xb0, 0x00, 0x13, 0x00, 0xd8, 0x01, 0x4d, 0xff, 0xfe]
regs = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]

pc = 0x00
ime = 0
toggle_ime = False # since the gameboy doesnt update IME immidietly we need helpers

cycle = 0

broken = False
breakpoints = [0x100]

start_time = time.time()

ops = {
    0x00: lambda pc: nop(),
    0x01: lambda pc: loadi16(BC),
    0x02: lambda pc: loadto((BC), A),
    0x03: lambda pc: inc16(BC),
    0x04: lambda pc: inc8(B),
    0x05: lambda pc: dec8(B),
    0x06: lambda pc: loadi8(B),
    0x07: lambda pc: rlca(),
    0x08: lambda pc: loadi16(SP),
    0x09: lambda pc: add16s(HL, BC),
    0x0a: lambda pc: loadfrom(A, (BC)),
    0x0b: lambda pc: dec16(BC),
    0x0c: lambda pc: inc8(C),
    0x0d: lambda pc: dec8(C),
    0x0e: lambda pc: loadi8(C),
    0x0f: lambda pc: rrca(),
    0x11: lambda pc: loadi16(DE),
    0x12: lambda pc: loadto((DE), A),
    0x13: lambda pc: inc16(DE),
    0x14: lambda pc: inc8(D),
    0x15: lambda pc: dec8(D),
    0x16: lambda pc: loadi8(D),
    0x17: lambda pc: rla(),
    0x18: lambda pc: jumpr(),
    0x19: lambda pc: add16s(HL, DE),
    0x1a: lambda pc: loadfrom(A, (DE)),
    0x1b: lambda pc: dec16(DE),
    0x1c: lambda pc: inc8(E),
    0x1d: lambda pc: dec8(E),
    0x1e: lambda pc: loadi8(E),
    0x1f: lambda pc: rra(),
    0x20: lambda pc: jumprf(m.read(pc)),
    0x21: lambda pc: loadi16(HL),
    0x22: lambda pc: loadtoc('+'),
    0x23: lambda pc: inc16(HL),
    0x24: lambda pc: inc8(H),
    0x25: lambda pc: dec8(H),
    0x26: lambda pc: loadi8(H),
    0x28: lambda pc: jumprf(m.read(pc)),
    0x29: lambda pc: add16s(HL, HL),
    0x2a: lambda pc: loadfromc('+'),
    0x2b: lambda pc: dec16(HL),
    0x2c: lambda pc: inc8(L),
    0x2d: lambda pc: dec8(L),
    0x2e: lambda pc: loadi8(L),
    0x2f: lambda pc: cpl(),
    0x30: lambda pc: jumprf(m.read(pc)),
    0x31: lambda pc: loadi16(SP),
    0x32: lambda pc: loadtoc('-'),
    0x33: lambda pc: inc16(SP),
    0x34: lambda pc: incat((HL)),
    0x35: lambda pc: decat((HL)),
    0x36: lambda pc: loadiat((HL)),
    0x37: lambda pc: update(1, 4, n=0, h=0, c=1),
    0x38: lambda pc: jumprf(m.read(pc)),
    0x39: lambda pc: add16s(HL, SP),
    0x3a: lambda pc: loadfromc('-'),
    0x3b: lambda pc: dec16(SP),
    0x3c: lambda pc: inc8(A),
    0x3d: lambda pc: dec8(A),
    0x3e: lambda pc: loadi8(A),
    0x3f: lambda pc: update(1, 4, n=0, h=0, c=int(not c())),
    0x40: lambda pc: load(B, B),
    0x41: lambda pc: load(B, C),
    0x42: lambda pc: load(B, D),
    0x43: lambda pc: load(B, E),
    0x44: lambda pc: load(B, H),
    0x45: lambda pc: load(B, L),
    0x46: lambda pc: loadfrom(B, (HL)),
    0x47: lambda pc: load(B, A),
    0x48: lambda pc: load(C, B),
    0x49: lambda pc: load(C, C),
    0x4a: lambda pc: load(C, D),
    0x4b: lambda pc: load(C, E),
    0x4c: lambda pc: load(C, H),
    0x4d: lambda pc: load(C, L),
    0x4e: lambda pc: loadfrom(C, (HL)),
    0x4f: lambda pc: load(C, A),
    0x50: lambda pc: load(D, B),
    0x51: lambda pc: load(D, C),
    0x52: lambda pc: load(D, D),
    0x53: lambda pc: load(D, E),
    0x54: lambda pc: load(D, H),
    0x55: lambda pc: load(D, L),
    0x56: lambda pc: loadfrom(B, (HL)),
    0x57: lambda pc: load(D, A),
    0x58: lambda pc: load(E, B),
    0x59: lambda pc: load(E, C),
    0x5a: lambda pc: load(E, D),
    0x5b: lambda pc: load(E, E),
    0x5c: lambda pc: load(E, H),
    0x5d: lambda pc: load(E, L),
    0x5e: lambda pc: loadfrom(E, (HL)),
    0x5f: lambda pc: load(E, A),
    0x60: lambda pc: load(H, B),
    0x61: lambda pc: load(H, C),
    0x62: lambda pc: load(H, D),
    0x63: lambda pc: load(H, E),
    0x64: lambda pc: load(H, H),
    0x65: lambda pc: load(H, L),
    0x66: lambda pc: loadfrom(H, (HL)),
    0x67: lambda pc: load(H, A),
    0x68: lambda pc: load(L, B),
    0x69: lambda pc: load(L, C),
    0x6a: lambda pc: load(L, D),
    0x6b: lambda pc: load(L, E),
    0x6c: lambda pc: load(L, H),
    0x6d: lambda pc: load(L, L),
    0x6e: lambda pc: loadfrom(L, (HL)),
    0x6f: lambda pc: load(L, A),
    0x70: lambda pc: loadto((HL), B),
    0x71: lambda pc: loadto((HL), C),
    0x72: lambda pc: loadto((HL), D),
    0x73: lambda pc: loadto((HL), E),
    0x74: lambda pc: loadto((HL), H),
    0x75: lambda pc: loadto((HL), L),
    0x77: lambda pc: loadto((HL), A),
    0x78: lambda pc: load(A, B),
    0x79: lambda pc: load(A, C),
    0x7a: lambda pc: load(A, D),
    0x7b: lambda pc: load(A, E),
    0x7c: lambda pc: load(A, H),
    0x7d: lambda pc: load(A, L),
    0x7e: lambda pc: loadfrom(A, (HL)),
    0x7f: lambda pc: load(A, A),
    0x80: lambda pc: alu8(add, readReg(B), 4),
    0x81: lambda pc: alu8(add, readReg(C), 4),
    0x82: lambda pc: alu8(add, readReg(D), 4),
    0x83: lambda pc: alu8(add, readReg(E), 4),
    0x84: lambda pc: alu8(add, readReg(H), 4),
    0x85: lambda pc: alu8(add, readReg(L), 4),
    0x86: lambda pc: alu8(add, m.read(readRegs(HL)), 8),
    0x87: lambda pc: alu8(add, readReg(A), 4),
    0x88: lambda pc: alu8(adc, readReg(B), 4),
    0x89: lambda pc: alu8(adc, readReg(C), 4),
    0x8a: lambda pc: alu8(adc, readReg(D), 4),
    0x8b: lambda pc: alu8(adc, readReg(E), 4),
    0x8c: lambda pc: alu8(adc, readReg(H), 4),
    0x8d: lambda pc: alu8(adc, readReg(L), 4),
    0x8e: lambda pc: alu8(adc, m.read(readRegs(HL)), 8),
    0x8f: lambda pc: alu8(adc, readReg(A), 4),
    0x90: lambda pc: alu8(sub, readReg(B), 4),
    0x91: lambda pc: alu8(sub, readReg(C), 4),
    0x92: lambda pc: alu8(sub, readReg(D), 4),
    0x93: lambda pc: alu8(sub, readReg(E), 4),
    0x94: lambda pc: alu8(sub, readReg(H), 4),
    0x95: lambda pc: alu8(sub, readReg(L), 4),
    0x96: lambda pc: alu8(sub, m.read(readRegs(HL)), 8),
    0x97: lambda pc: alu8(sub, readReg(A), 4),
    0x98: lambda pc: alu8(sbc, readReg(B), 4),
    0x99: lambda pc: alu8(sbc, readReg(C), 4),
    0x9a: lambda pc: alu8(sbc, readReg(D), 4),
    0x9b: lambda pc: alu8(sbc, readReg(E), 4),
    0x9c: lambda pc: alu8(sbc, readReg(H), 4),
    0x9d: lambda pc: alu8(sbc, readReg(L), 4),
    0x9e: lambda pc: alu8(sbc, m.read(readRegs(HL)), 8),
    0x9f: lambda pc: alu8(sbc, readReg(A), 4),
    0xa0: lambda pc: alu8(and_, readReg(B), 4),
    0xa1: lambda pc: alu8(and_, readReg(C), 4),
    0xa2: lambda pc: alu8(and_, readReg(D), 4),
    0xa3: lambda pc: alu8(and_, readReg(E), 4),
    0xa4: lambda pc: alu8(and_, readReg(H), 4),
    0xa5: lambda pc: alu8(and_, readReg(L), 4),
    0xa6: lambda pc: alu8(and_, m.read(readRegs(HL)), 8),
    0xa7: lambda pc: alu8(and_, readReg(A), 4),
    0xa8: lambda pc: alu8(xor, readReg(B), 4),
    0xa9: lambda pc: alu8(xor, readReg(C), 4),
    0xaa: lambda pc: alu8(xor, readReg(D), 4),
    0xab: lambda pc: alu8(xor, readReg(E), 4),
    0xac: lambda pc: alu8(xor, readReg(H), 4),
    0xad: lambda pc: alu8(xor, readReg(L), 4),
    0xae: lambda pc: alu8(xor, m.read(readRegs(HL)), 8),
    0xaf: lambda pc: alu8(xor, readReg(A), 4),
    0xb0: lambda pc: alu8(or_, readReg(B), 4),
    0xb1: lambda pc: alu8(or_, readReg(C), 4),
    0xb2: lambda pc: alu8(or_, readReg(D), 4),
    0xb3: lambda pc: alu8(or_, readReg(E), 4),
    0xb4: lambda pc: alu8(or_, readReg(H), 4),
    0xb5: lambda pc: alu8(or_, readReg(L), 4),
    0xb6: lambda pc: alu8(or_, m.read(readRegs(HL)), 8),
    0xb7: lambda pc: alu8(or_, readReg(A), 4),
    0xb8: lambda pc: alu8(cp, readReg(B), 4),
    0xb9: lambda pc: alu8(cp, readReg(C), 4),
    0xba: lambda pc: alu8(cp, readReg(D), 4),
    0xbb: lambda pc: alu8(cp, readReg(E), 4),
    0xbc: lambda pc: alu8(cp, readReg(H), 4),
    0xbd: lambda pc: alu8(cp, readReg(L), 4),
    0xbe: lambda pc: alu8(cp, m.read(readRegs(HL)), 8),
    0xbf: lambda pc: alu8(cp, readReg(A), 4),
    0xc0: lambda pc: retff(op),
    0xc1: lambda pc: pop(BC),
    0xc2: lambda pc: jumpff(op),
    0xc3: lambda pc: jump(),
    0xc4: lambda pc: callff(op),
    0xc5: lambda pc: push(BC),
    0xc6: lambda pc: alu8(sub, m.read(pc+1), 8, 2),
    0xc7: lambda pc: rst(0x00),
    0xc8: lambda pc: retff(),
    0xc9: lambda pc: ret(),
    0xca: lambda pc: jumpff(op),
    0xcb: lambda pc: prefixcb(m.read(pc+1)),
    0xcc: lambda pc: callff(op),
    0xcd: lambda pc: call(),
    0xce: lambda pc: alu(adc, m.read(pc+1), 8, 2),
    0xcf: lambda pc: rst(0x08),
    0xd0: lambda pc: retff(op),
    0xd1: lambda pc: pop(DE),
    0xd2: lambda pc: jumpff(op),
    0xd3: lambda pc: nofunction(pc),
    0xd4: lambda pc: callff(op),
    0xd5: lambda pc: push(DE),
    0xd6: lambda pc: alu8(sub, m.read(pc+1), 8, 2),
    0xd7: lambda pc: rst(0x10),
    0xd8: lambda pc: retff(op),
    0xda: lambda pc: jumpff(op),
    0xdb: lambda pc: nofunction(pc),
    0xdc: lambda pc: callff(op),
    0xdd: lambda pc: nofunction(pc),
    0xde: lambda pc: alu8(sbc, m.read(pc+1), 8, 2),
    0xdf: lambda pc: rst(0x18),
    0xe0: lambda pc: ldh_ia(m.read(pc+1)),
    0xe1: lambda pc: pop(HL),
    0xe2: lambda pc: savetoIO(),
    0xe3: lambda pc: nofunction(pc),
    0xe4: lambda pc: nofunction(pc),
    0xe5: lambda pc: push(HL),
    0xe6: lambda pc: alu8(and_, m.read(pc+1), 8, 2),
    0xe7: lambda pc: rst(0x20),
    0xe9: lambda pc: jumpto(),
    0xea: lambda pc: putabs(),
    0xeb: lambda pc: nofunction(pc),
    0xec: lambda pc: nofunction(pc),
    0xed: lambda pc: nofunction(pc),
    0xee: lambda pc: alu8(xor, m.read(pc+1), 8, 2),
    0xef: lambda pc: rst(0x28),
    0xf0: lambda pc: ldh_ai(m.read(pc+1)),
    0xf1: lambda pc: pop(AF),
    0xf2: lambda pc: savetoIO(),
    0xf3: lambda pc: di(),
    0xf4: lambda pc: nofunction,
    0xf5: lambda pc: push(AF),
    0xf6: lambda pc: alu8(or_, m.read(pc+1), 8, 2),
    0xf7: lambda pc: rst(0x30),
    0xf9: lambda pc: ldhlsp(),
    0xfa: lambda pc: loadabs(),
    0xfb: lambda pc: ei(),
    0xfc: lambda pc: nofunction(pc),
    0xfd: lambda pc: nofunction(pc),
    0xfe: lambda pc: alu8(cp, m.read(pc+1), 8, 2),
    0xff: lambda pc: rst(0x38)
}

def run(ppu):
    global pc, sp, cycle, toggle_ime, ime, broken, breakpoint

    while True:

        if breakpoints != [] and pc in breakpoints:
            broken = True

        if broken:
            handleBroken()


        if (pc > 0x2d3):
            print(hex(m.read(pc)), "at", hex(pc))
        op = m.read(pc)
        ops[op](pc)


        # -- Handle interrupts
        if toggle_ime and op not in [0xfb, 0xf3]:
            ime = int(not ime)
            toggle_ime = False

        if ime == 1:
            for intr in intrs_ordered:
                print(intr, getie(intr), getif(intr))
                if getie(intr) and getif(intr):
                    ime = 0
                    pushc(pc)
                    pc = intr_addrs[intr]
                    print("interrupt occured!")
                    input()

        # PPU updates
        ppu.update(cycle)


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

    # no update, performed in inc/dec

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

    # No update, update is done in inc16/dec16

def ldh_ia(value):
    addr = 0xFF00 | value
    m.write(addr, readReg(A))

    update(2, 12)

def ldh_ai(value):
    addr = 0xFF00 | value
    writeReg(A, m.read(addr))

    update(2, 12)

def loadfromIO():
    addr = 0xFF00 | readReg(C)
    m.write(addr, readReg(A))
    update(1, 8)

def savetoIO():
    addr = 0xFF00 | readReg(C)
    writeReg(A, m.read(addr))
    update(1, 8)

def ldhlsp():
    writeRegs(SP, readRegs(HL))
    update(1, 8)

def putabs():
    ls = m.read(pc + 1)
    ms = m.read(pc + 2)
    addr = ms << 8 | ls
    m.write(addr, readReg(A))
    update(3, 16)

def loadabs():
    ls = m.read(pc + 1)
    ms = m.read(pc + 2)
    addr = ms << 8 | ls
    writeReg(A, m.read(addr))
    update(3, 16)


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
    update(pcinc, cyc, zerocheck=(a - b), n=1, h=((~newv >> 4) & 1), c=int(a < b))
    return a

# --- Prefix CB ----------------------------------------------------------------
def operand(op):
    oprd = { 0x0: B,
             0x1: C,
             0x2: D,
             0x3: E,
             0x4: H,
             0x5: L,
             0x6: "(HL)",
             0x7: A }
    return oprd[op & 0b111]

def prefixcb(op):
    oprd = operand(op)
    value = readReg(oprd) if type(oprd) == int else m.read(readRegs(HL))
    newvalue = None

    if op & 0b11111000 == 0:
        newvalue = rlc(value)
    elif op & 0b11111000 == 8:
        newvalue = rrc(value)
    elif op & 0b11111000 == 16:
        newvalue = rl(value)
    elif op & 0b11111000 == 24:
        newvalue = rr(value)
    elif op & 0b11111000 == 32:
        newvalue = sla(value)
    elif op & 0b11111000 == 40:
        newvalue = sra(value)
    elif op & 0b11111000 == 48:
        newvalue = swap(value)
    elif op & 0b11111000 == 56:
        newvalue = srl(value)
    elif op & 0b11000000 == 64:
        bit(value, op)
    elif op & 0b11000000 == 128:
        newvalue = reset(value, op)
    elif op & 0b11000000 == 192:
        newvalue = gset(value, op)

    if newvalue != None:
        if type(oprd) == int:
            writeReg(oprd, newvalue)
        else:
            update(0, 8) # additional 8 cycles for writing to (HL)
            m.write(readRegs(HL), newvalue)

def rlc(v):
    bit7 = (v >> 7) & 1
    rotated = (v << 1 & 0xff) | bit7
    update(2, 8, zerocheck=rotated, n=0, h=0, c=bit7)
    return rotated

def rrc(v):
    bit0 = v & 1
    rotated = v >> 1 | (bit0 << 7)
    update(2, 8, zerocheck=rotated, n=0, h=0, c=bit0)
    return rotated

def rl(v):
    bit7 = (v >> 7) & 1
    rotated = (v << 1 & 0xff) | c()
    update(2, 8, zerocheck=rotated, n=0, h=0, c=bit7)
    return rotated

def rr(v):
    bit0 = v & 1
    rotated = v >> 1 | (c() << 7)
    update(2, 8, zerocheck=rotated, n=0, h=0, c=bit0)
    return rotated

def sla(v):
    bit7 = v >> 7 & 1
    newv = (v << 1) & 0xff
    update(2, 8, zerocheck=newv, n=0, h=0, c=bit7)
    return newv

def sra(v):
    bit7 = v >> 7 & 1
    print(bit7)
    newv = ((v >> 1) & 0xff) | (bit7 << 7)
    return newv

def swap(v):
    lsbits = v & 0x0f
    msbits = v & 0xf0
    newv = (lsbits << 4) | (msbits >> 4)
    update(2, 8, zerocheck=newv, n=0, h=0, c=0)
    return newv

def srl(v):
    bit0 = v & 0b1
    newv = v >> 1
    update(2, 8, zerocheck=newv, n=0, h=0, c=bit0)
    return newv

def bit(value, op):
    place = op >> 3 & 0b111
    bitvalue = value >> place & 1
    update(2, 8, zerocheck=bitvalue, n=0, h=1)

def reset(value, op):
    place = op >> 3 & 0b111
    mask = 1 << place ^ 0xff
    return value & mask

def gset(value, op):
    place = op >> 3 & 0b111
    mask = 1 << place
    return value | mask

# --- Jumps --------------------------------------------------------------------
def jump():
    # lsb first, apparently
    addr = (m.read(pc+2) << 8) | m.read(pc+1)
    update(3, 16, newpc=addr)


def jumpff(op):
    assert op in [0xc2, 0xca, 0xd2, 0xda]
    dojump = False

    if op == 0xc2:
        dojump = z() == 0
    elif op == 0xca:
        dojump = z() == 1
    elif op == 0xd2:
        dojump = c() == 0
    elif op == 0xda:
        dojump = c() == 1

    if dojump:
        jump()
    else:
        update(3, 12)

def jumpto():
    addr = readRegs(HL)
    update(1, 4, newpc=addr)

def jumpr():
    rel = m.read(pc+1)
    update(twos(rel) + 2, 12)

def jumprf(op):
    assert op in [0x20, 0x30, 0x28, 0x38]
    dojump = False

    if op == 0x20:
        dojump = z() == 0
    elif op == 0x28:
        dojump = z() == 1
    elif op == 0x30:
        dojump = c() == 0
    elif op == 0x38:
        dojump = c() == 1

    if dojump:
        jumpr()
    else:
        update(2, 8)


def call():
    pushc(pc+3)
    addr = (m.read(pc+2) << 8) | m.read(pc+1)
    update(3, 24, newpc=addr)

def callff(op):
    assert op in [0xc4, 0xcc, 0xd4, 0xdc]
    docall = False

    if op == 0xc4:
        docall = z() == 0
    elif op == 0xcc:
        docall = z() == 1
    elif op == 0xd4:
        docall = c() == 0
    elif op == 0xdd:
        docall = c() == 1

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
        doreturn = z() == 0
    elif op == 0xc8:
        doreturn = z() == 1
    elif op == 0xd0:
        doreturn = c() == 0
    elif op == 0xd8:
        doreturn = c() == 1

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
    return msbits | lsbits

def pop(regs):
    writeRegs(regs, popc())

    update(1, 12)

def nofunction(pc):
    raise ValueError("Instruction does not exist at pc=" + hex(pc), "op=" + hex(m.read(pc)))

def ei():
    if ime == 0:
        toggle_ime = True

    update(1, 4)

def di():
    if ime == 1:
        toggle_ime = True

    update(1, 4)

# -----------------
# ---- Helpers ----
# -----------------

def update(pcinc, cycles, zerocheck=None, n=-1, h=-1, c=-1, newpc=None):
    global pc, cycle

    if zerocheck != None:
        zero(zerocheck)

    setFlags(n=n, h=h, c=c)
    if newpc == None:
        pc = (pc + pcinc) & 0b1111111111111111
    else:
        pc = newpc
    cycle += cycles

def zero(value):
    if (value & 0xff) == 0:
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

def ones(value):
    value = value & 0xff
    return value if value < 128 else value - 255

def twos(value):
    if (value >> 7) & 1 == 1:
        value = value - (1 << 8)
    return value

# --- DEBUG ----------------------------------------------


def printState():
    print("{0:#0{1}x}".format(pc, 6), "{0:#0{1}x}".format(m.read(pc), 4))
    printRegs()
    printFlags()
    printLCD()

def printFlags():
    f = readReg(F)
    print("z=" + str((f >> 7) & 1), end="  ")
    print("n=" + str((f >> 6) & 1), end="  ")
    print("h=" + str((f >> 5) & 1), end="  ")
    print("c=" + str((f >> 4) & 1), end="  ")
    print("if=" + "{0:#0{1}x}".format(m.read(0xff0f), 4), end="  ")
    print("ie=" + "{0:#0{1}x}".format(m.read(0xffff), 4), end="  ")

    print("ime=" + str(ime))

def printRegs():
    names = "AFBCDEHL"
    # print("Registers: ", end="")
    # for i in range(0, L+1):
    #     print(str(names[i]) + ":", "{0:#0{1}x}, ".format(regs[i], 4), end="")
    # print()

    names = ["AF", "BC", "DE", "HL", "SP"]
    for i in range(0, 5):
        print(str(names[i]) + "=" + "{0:#0{1}x}  ".format(readRegs(i*2), 6), end="")
    print()

def printLCD():
    print("LY=" + str(hex(m.read(0xff44))), " LCDC=" + str(hex(m.read(0xff41))))

def printMemRange(start, end):
    values = m.memory[start:(end+1)]

    result = "       "

    for i in range(16):
        digit = str(hex((start & 0xf) + i))[2]
        result += "xxx" + digit + " "

    i = 0
    for value in values:
        if i % 16 == 0:
            address = ("{0:#0{1}x}".format(start + i, 6))[:-1] + "x"
            result += "\n" + address

        result += " " + "{0:#0{1}x}".format(value, 4)

        i += 1

    print(result)

def printStack(stackstart=0xffff):
    sp = readRegs(SP)
    size = (stackstart+1) - sp
    result = ""
    for i in range(size // 2):
        address = sp + i * 2
        address_str = "{0:#0{1}x}".format(address, 6)
        value_str = "{0:#0{1}x}".format(m.reads(address), 6)
        result += "  " + address_str + ":  | " + value_str + " |"

        if i == 0:
            result += " <-"

        result += "\n"

    print(result)

default_debug_command = "nothing"
default_debug_arguments = []

def handleBroken():
    global default_debug_command
    global default_debug_arguments, start_time
    print(time.time() - start_time)
    printState()

    commands = {
        "m": cmd_memory,
        "memory": cmd_memory,
        "s": cmd_stack,
        "stack": cmd_stack,
        "r": cmd_run,
        "run": cmd_run,
        "br": cmd_breakpoint,
        "breakpoint": cmd_breakpoint,
        "c": cmd_cycles,
        "cycles": cmd_cycles,
        "nothing": lambda args: True
    }

    command = "-"
    while command != "":
        full_cmd = input("> ")
        command = full_cmd.split(" ")[0]
        args = full_cmd.split(" ")[1:]
        if command in commands:
            commands[command](args)
        elif command == "d" or command == "default":
            default_debug_command = args[0]
            default_debug_arguments = args[1:]
            print("Set the default command to:",
                default_debug_command, " ".join(default_debug_arguments))
    else:
        commands[default_debug_command](default_debug_arguments)

def cmd_breakpoint(args):
    global breakpoints
    if len(args) == 1:
        if args[0] == "list":
            print([hex(x) for x in breakpoints])
    elif len(args) == 2:
        line = int(args[1], 0)
        if args[0] == "add":
            breakpoints.append(line)
            print([hex(x) for x in breakpoints])
        elif args[0] == "rm":
            if line in breakpoints:
                breakpoints.remove(line)
                print([hex(x) for x in breakpoints])
            else:
                print("No such breakpoint.")
        else:
            print("Unknown breakpoint argument")


def cmd_stack(args):
    if len(args) >= 1:
        printStack(stackstart=(int(args[0], 0)))
    else:
        printStack()

def cmd_cycles(args):
    global cycle
    print(str(cycle) + " cycles, (" + str(round(cycle / (4.1943 * 10 ** 6), 4)) + " seconds)")

def cmd_run(args):
    global broken
    broken = False
    print("[Enter]", end="")

def cmd_memory(args):
    if len(args) == 1:
        address = int(args[0], 0)
        print(hex(m.read(address)))
    elif len(args) == 2:
        start_addr = int(args[0], 0)
        end_addr = int(args[1], 0)
        printMemRange(start_addr, end_addr)
    else:
        print("Unsupported amount of arguments")

def save_state(args):
    state = {
        "regs": regs,
        "pc": pc,
        "ime": ime,
        "toggle_ime": toggle_ime,
        "cycle": cycle,
        "mem": m.memory
    }

    filename = "state.sav"
    if len(args) > 0:
        filename = " ".join(args)

    with open(filename, 'w') as outfile:
        json.dump(state, outfile)

def load_state(args):
    global regs, pc, ime, toggle_ime, cycle

    filename = "state.sav"
    if len(args) > 0:
        filename = " ".join(args)

    # state = {}
    with open(filename) as outfile:
        state = json.load(outfile)

    return state
