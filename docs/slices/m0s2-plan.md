# M0 S0.2 plan

Milestone: M0
Slice: S0.2
Name: Program the FPGA from the Beagle

## Features

No feature id. F0 stays on S0.1. F1 stays on M1.

This slice proves that Linux on the BeagleV-Fire can program the PolarFire fabric and come back up. The gateware is the stock `default` directory from the `bbb.io-gateware` package. This slice does not build a bitstream from this repository.

## In this slice

1. A serial console stays open for the whole run. SSH is the second session.
2. As root, `change-gateware.sh` is run on `/usr/share/beagleboard/gateware/default`. The script on the board is the one that decides the exact invocation. The upstream form is `. ./change-gateware.sh default` from that directory. The copy in this repository is run as root and takes the gateware directory as its argument. If the first try fails, read the top of the script on the board and use the form it implements.
3. Power stays connected. Reset is not pressed while programming runs. The board reboots itself. Programming can take a few minutes.
4. After Linux is back, serial or SSH login works and `uname -a` shows `riscv64`.

The System Controller loads a programmed image when its design version differs from the one already in the fabric. The stock `default` image is the known-good gateware for this Debian image. A same-version file can be ignored. That is acceptable for this proof as long as the script runs and Linux returns. A design-version line from the serial log, if one is printed, is recorded in the test plan's pass record.

The older notes in `docs/milestones/M0-setup/slices/S0.5-program-from-the-board/` are source material. This file is the spec. Official steps: <https://docs.beagleboard.org/boards/beaglev/fire/demos-and-tutorials/gateware/upgrade-gateware.html>.

## Out of this slice

- FlashPro Express from the laptop. That is S0.3.
- Building a bitstream with `build-bitstream.py` and programming that image. That is F1, in M1. M1 will copy a directory that contains `LinuxProgramming/mpfs_bitstream.spi` to the board and pass the parent directory to `change-gateware.sh`. The design version of that file has to differ from the one already programmed.
- A display, a panel, and any GPU cape.

## Done when

`docs/slices/m0s2-test-plan.md` passes.
