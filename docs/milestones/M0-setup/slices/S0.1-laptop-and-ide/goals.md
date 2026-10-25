# S0.1 Laptop and FPGA IDE

## Goal

Prepare the laptop that builds BeagleV-Fire bitstreams, and install Libero SoC 2022.3, which is the FPGA IDE this gateware tree uses.

## Features

F0

## In this slice

The laptop can start Libero 2022.3, obtain a license, and see the other tools the bitstream builder looks for.

## Out of this slice

Icarus Verilog and the RISC-V Linux cross compiler are S0.2. Building a bitstream is M1. Programming the board is S0.5 and S0.6.

## Done when

`test.md` passes and `implementation.md` records the laptop distro, the install paths, and the Libero version line.

## Procedure

This tree’s gateware builder was tested on Ubuntu 20.04 and on Windows 11. Write these steps for the Linux laptop you are actually using, and record that distro in `implementation.md`. Libero SoC **v2022.3** is the version `support/gateware/sources/FPGA-design/Readme.md` requires. Do not install a newer Libero and expect this tree to build.

1. Install the laptop packages the builder’s Python and device-tree steps need.

   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip git device-tree-compiler
   pip3 install GitPython PyYAML requests
   ```

2. Create a Microchip account if you do not already have one. Download **Libero SoC v2022.3** for Linux from Microchip’s Libero downloads. Download SoftConsole from the same account. SoftConsole supplies `riscv-unknown-elf-gcc`, which the builder uses for the HSS bootloader.

3. Run the Libero installer. Beagle’s programming-tools notes recommend a path under the home directory, such as `~/microchip`. Use one tree for Libero and keep the path. The installer also provides FlashPro Express (`FPExpress`) and `fpgenprog`.

4. Install SoftConsole. Note its install directory. That path is `SC_INSTALL_DIR`.

5. Install the Libero license file Microchip issued for this machine. Note the path or the license-server port. That value is `LM_LICENSE_FILE`.

6. Find these three paths in the install tree and write them down:

   - The directory that contains the `libero` executable. Its parent install root is `LIBERO_INSTALL_DIR`.
   - The `fpgenprog` executable. That full path is `FPGENPROG`.
   - The directory that contains `riscv-unknown-elf-gcc`, usually inside SoftConsole. It must be on `PATH`.
   - The directory that contains `pfsoc_mss` (PolarFire SoC MSS Configurator). It must be on `PATH`. It ships with Libero.

7. Put the variables in a file you can source, for example `~/beaglev-fpga-env.sh`:

   ```bash
   export LIBERO_INSTALL_DIR=$HOME/microchip/Libero_SoC_v2022.3
   export SC_INSTALL_DIR=$HOME/microchip/SoftConsole
   export FPGENPROG=$HOME/microchip/Libero_SoC_v2022.3/bin/fpgenprog
   export LM_LICENSE_FILE=$HOME/microchip/license.dat
   export PATH="$LIBERO_INSTALL_DIR/bin:$SC_INSTALL_DIR/riscv-unknown-elf-gcc/bin:$PATH"
   ```

   Replace every path with the one found in step 6. The `fpgenprog` and toolchain directories above are the usual layout, not a promise. `which` after sourcing the file is the check.

8. Source the file from the laptop’s shell startup so a new terminal still sees it.

   ```bash
   echo '. $HOME/beaglev-fpga-env.sh' >> ~/.bashrc
   source ~/beaglev-fpga-env.sh
   ```

9. Confirm the IDE and the builder’s tools answer:

   ```bash
   command -v libero
   command -v pfsoc_mss
   command -v riscv-unknown-elf-gcc
   riscv-unknown-elf-gcc --version
   test -x "$FPGENPROG" && echo "fpgenprog ok"
   dtc --version
   python3 -c "import git, yaml, requests; print('python ok')"
   ```

10. Start Libero and let it obtain a license. A GUI session that reaches the main window is enough. If it stops on a license error, fix `LM_LICENSE_FILE` before continuing. Record the version string Libero prints. It must be 2022.3.

## References

- `support/gateware/README.md` (environment variables and Python packages)
- `support/gateware/sources/FPGA-design/Readme.md` (Libero v2022.3)
- `support/gateware/gateware_scripts/build_gateware.py`, `check_tool_status` (the tools the builder refuses to start without)
