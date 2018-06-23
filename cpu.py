import memory as m



ops = \
{

}

def run():
    pc = 256

    while True:
        opcode = hex(m.read(pc))
        print(opcode)

        pc += 1
