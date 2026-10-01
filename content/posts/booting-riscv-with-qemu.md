---
title: "Booting a RISCV kernel using QEMU"
date: 2026-01-28T12:02:00+03:00
draft: true
summary: "An overview of a RISCV boot process using QEMU"
---


Let's first install the qemu emulator for riscv. That would be the command
I have already installed it on my machine. Its currently `v7.2.0`

Let's then learn some basic qemu commands

### -machine
Helps you choose the emulated machine, available options are
```
qemu-system-riscv64 -machine (none|virt|shakti_c|sifive_e|sifive_u|spike)
```

### Assembly

Lets write a simple assembly program compile it,execute it 
and finally connect a gdb debugger to it

```asm
.section .text 
.globl _start

_start:
    # where should we point the stack pointer to
    la sp,

```

```asm
.section .text 
.global _entry 
entry:
    la   sp, stack0 
    li   a0, 1024 * 4
    csrr a1, mhartid
    addi a1, a1, 1
    mul  a0, a0, a1
    add  sp, sp, a0
    # jump to the start() routine in start.c
    call start

spin:
    j spi
```

### C code 
```c
void main();
void timerinit();
```

    

