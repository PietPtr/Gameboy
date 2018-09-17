# Gameboy

Another gameboy emulator

# Debug example

Displays memory in the given range

```
> memory 0xff10 0xff2f
       xxx0 xxx1 xxx2 xxx3 xxx4 xxx5 xxx6 xxx7 xxx8 xxx9 xxxa xxxb xxxc xxxd xxxe xxxf
0xff1x 0x00 0xf3 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
0xff2x 0x00 0x00 0x00 0x00 0x00 0x77 0x80 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
```

Shows the current state of the stack

```
> stack 0xffff
  0xfffa:  | 0x0400 | <-
  0xfffc:  | 0x0029 |
  0xfffe:  | 0x0000 |
```

Sets a default command to be executed every step

```
> default stack
Set the default command to: stack
```

Add, remove, and list breakpoints

```
> breakpoint list
['0x99']
> breakpoint add 0x44
['0x99', '0x44']
> breakpoint rm 0x99
['0x44']
```

Run to the next breakpoint

```
> run
```

# Resources

http://fms.komkon.org/EMUL8/

http://bgb.bircd.org/pandocs.htm

http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf

http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
