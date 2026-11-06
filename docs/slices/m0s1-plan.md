# M0 S0.1 plan

Milestone: M0
Slice: S0.1
Name: Machines are ready

## Features

### F0. Project software environment

The laptop that builds bitstreams has the FPGA tools, both RISC-V cross compilers, and Icarus Verilog. The BeagleV-Fire is running a Debian IoT image from its eMMC. Boot is proved with a serial console or SSH. No display is required. `scripts/check-env.py` is the single pass or fail check for the tools on both machines.

This slice installs and proves that environment. It does not program the FPGA.

## In this slice

1. Laptop FPGA development environment. Libero SoC 2022.3, a license Libero can obtain, SoftConsole, `FPGENPROG`, `pfsoc_mss`, git, Python 3 with GitPython, PyYAML, and requests, and `dtc`. The environment variables from `support/gateware/README.md` are set in a file the laptop shells source: `LIBERO_INSTALL_DIR`, `SC_INSTALL_DIR`, `FPGENPROG`, and `LM_LICENSE_FILE`. On this laptop `LM_LICENSE_FILE` is `/licenses/License.dat`. Libero can obtain a license only after `/licenses/lmgrd -c /licenses/License.dat -l /licenses/License.log` is running. The download and license steps are in the repository `README.md`. `libero`, `pfsoc_mss`, and `riscv64-unknown-elf-gcc` are on `PATH`.
2. RISC-V cross compilers for this board. `riscv64-unknown-elf-gcc` comes with SoftConsole and builds the HSS bootloader. `riscv64-linux-gnu-gcc` builds Linux userspace tests and an out-of-tree module.
3. Icarus Verilog (`iverilog`) on the laptop, for later slice simulations.
4. The latest BeagleV-Fire Debian IoT image from <https://www.beagleboard.org/distros>, written to the eMMC. The user password is set before the first boot, in `sysconf.txt` or with bb-imager. When this plan was written the current image was BeagleV-Fire Debian 13 2026-07-25 IoT. Use a newer BeagleV-Fire Debian IoT image if one is listed, and record the exact file.
5. Boot proof with no display. A serial session at 115200, or SSH, shows `/etc/os-release` naming Debian and `uname -a` containing `riscv64`.
6. Board configuration the next slice needs. The password is not a published default. The laptop can reach the board. `gcc`, `make`, `dtc`, kernel headers for `uname -r`, and `bbb.io-gateware` are installed. `change-gateware.sh` is present and is not run in this slice.
7. `scripts/check-env.py --host` and `--board`. One `PASS` or `FAIL` line per tool, with the version it found. Exit 0 only when every required line is `PASS`. No argument prints usage and exits non-zero. The script does not install tools and does not program the FPGA.

`--host` checks git, the three Python imports, `libero` reporting 2022.3 without a license error, `LM_LICENSE_FILE`, `pfsoc_mss`, `LIBERO_INSTALL_DIR`, `SC_INSTALL_DIR`, `FPGENPROG`, `riscv64-unknown-elf-gcc`, `dtc`, `iverilog`, and `riscv64-linux-gnu-gcc`.

`--board` checks `gcc`, `make`, `dtc`, `/lib/modules/$(uname -r)/build`, an executable `change-gateware.sh`, and `uname -m` equal to `riscv64`.

The older step-by-step notes under `docs/milestones/M0-setup/` are source material for this slice. This file is the spec.

## Out of this slice

- Programming the FPGA from the Beagle. That is S0.2. It runs `change-gateware.sh` and waits for the board to reboot itself.
- Programming the FPGA from the laptop with FlashPro Express. That is S0.3. It needs a FlashPro programmer. M0 can finish without one.
- Building a bitstream from this tree. That is F1, in M1.
- A display, a panel, and any GPU cape.

## Done when

`docs/slices/m0s1-test-plan.md` passes.
