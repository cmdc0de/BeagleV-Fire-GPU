# S0.2 Laptop project tools

## Goal

Install the two tools this project uses on the laptop that Libero does not provide: a Verilog simulator, and a RISC-V compiler that targets Linux.

## Features

F0

## In this slice

`iverilog` and `riscv64-linux-gnu-gcc` run on the build laptop.

## Out of this slice

Libero and the bare-metal HSS toolchain are S0.1. Kernel builds for the board are S0.4. Those use the board’s own compiler.

## Done when

`test.md` passes.

## Procedure

1. Source the environment from S0.1 so you are still on the same laptop setup.

2. Install Icarus Verilog and the RISC-V Linux cross compiler.

   ```bash
   sudo apt-get install iverilog gcc-riscv64-linux-gnu
   ```

3. Confirm both compilers answer with a version:

   ```bash
   iverilog -v
   riscv64-linux-gnu-gcc --version
   ```

`iverilog` is the simulator later slice tests name. `riscv64-linux-gnu-gcc` is the compiler for userspace tests and for an out-of-tree module built on the laptop. The module still needs the board’s kernel headers. Those are installed on the board in S0.4, and a laptop module build points `KDIR` at a copy of that kernel tree when M2 starts.
