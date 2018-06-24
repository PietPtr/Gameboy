#!/bin/bash

echo "$(($(cat cpu.py | grep "0x" | grep -v "\#" | wc -l) * 100 / 256))% done!"
