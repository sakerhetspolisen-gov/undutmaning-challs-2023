#!/usr/bin/env python
import os
from pwn import *

context.arch = "i386"

challenge = flat(
    asm(shellcraft.i386.echo("mata mig: ")),
    asm("""
			xor eax, eax
			mov al, 0xc0
			xor ebp, ebp
			xor ebx, ebx
			xor ecx, ecx
			mov ch, 0x1000 >> 8
			push -1
			pop edi
			push 7
			pop edx
			push 0x22
			pop esi
			int 0x80
        """),
    asm(shellcraft.i386.read(0, "eax", 0x80)),
    asm("mov ebx, eax"),
    asm(shellcraft.i386.linux.egghunter(0x0054414d)),
    asm("""
			xor ebx, ebx
			mov eax, edi
			add eax, 2
			mov dl, 0x00
			_loop:
			mov byte [eax], dl
			add eax, 4
			cmp ebx, 13
			add ebx, 1
			jl _loop
		"""),
    asm("jmp edi"),
    asm(shellcraft.i386.linux.exit(0))
)

filename = make_elf(challenge, extract=False, strip=True)
os.system("cp {} ./hungrig".format(filename))
