#!/bin/bash
num=$(cat cpu.py | grep "        elif op == 0x" | grep -v "\#" | wc -l)
echo "$((($num+1) * 100 / 256))% done!"
