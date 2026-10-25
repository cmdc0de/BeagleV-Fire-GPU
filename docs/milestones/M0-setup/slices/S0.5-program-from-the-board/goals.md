# S0.5 Program the FPGA from the Beagle

## Goal

Program the PolarFire fabric from Linux running on the BeagleV-Fire, and show that the board comes back. This is the path the later milestones use for bitstreams built on the laptop.

## Features

F0. The first bitstream built from this repository is M1. This slice proves the programming path with the gateware that is already on the image.

## In this slice

`change-gateware.sh` programs a gateware directory and the board reboots into Linux without anyone powering it off.

## Out of this slice

A direct JTAG program from the laptop is S0.6. Building `build-bitstream.py` output is M1.

## Done when

`test.md` passes. The serial log shows the program-and-reboot cycle, and SSH works again afterward.

## Procedure

The on-board script and the warning not to power off are documented at <https://docs.beagleboard.org/boards/beaglev/fire/demos-and-tutorials/gateware/upgrade-gateware.html>.

Linux programming writes the bitstream into the System Controller SPI flash and reboots. On the way back up, HSS asks the System Controller to load the FPGA. The System Controller loads it when the design version in the file differs from the one already in the fabric. A file with the same design version is ignored. M1 has to bump that version. This slice can use the stock `default` directory, which is the image’s known-good gateware.

### A. Program the gateware that is already on the board

1. SSH in, from S0.4.
2. Keep a serial console open as well, so the reboot is visible if SSH drops.
3. Run the stock script as root. The installed copy lives with the gateware package from S0.4:

   ```bash
   cd /usr/share/beagleboard/gateware
   sudo ./change-gateware.sh default
   ```

   The upstream guide sources the script (`. ./change-gateware.sh default`). The script in this repository must be run as root and takes the gateware directory as its argument. Use whichever form the file on the board actually implements. Read the first screen of `change-gateware.sh` if the invocation fails.

4. Do not unplug power and do not press Reset while it runs. Programming takes a few minutes. The board reboots itself.
5. When Linux is back, log in over serial or SSH and run `uname -a` again.

### B. Program a bitstream that was built on the laptop

Use this once M1 has produced programming files. The same steps are how every later bitstream moves from the laptop onto the FPGA.

1. On the laptop, the builder’s output directory for a design contains `LinuxProgramming/mpfs_bitstream.spi`. The script in this repository accepts a directory that contains that `LinuxProgramming` folder. Copy the directory, not only the `.spi` file:

   ```bash
   scp -r LinuxProgramming beagle@BOARD_IP:~/gateware/my-design/LinuxProgramming
   ```

   `BOARD_IP` is the address from S0.4. The parent `my-design` is the argument the script expects, because it looks for `$1/LinuxProgramming/mpfs_bitstream.spi`.

2. On the board, as root, point the script at that parent directory:

   ```bash
   sudo /usr/share/beagleboard/gateware/change-gateware.sh /home/beagle/gateware/my-design
   ```

   The script copies `mpfs_bitstream.spi` into the firmware directory and starts the Microchip update script. On a 6.1 kernel it uses `update-gateware-6-1.sh`. On other kernels it uses `update-gateware.sh`.

3. Same rule as path A: leave power alone until the board has rebooted by itself.
4. If the board reboots but the fabric did not change, check the design version. It has to differ from the version already programmed. Record the version you sent in `implementation.md`.

Path A is the proof for this slice. Path B is the procedure M1 will run, and it is part of this guide so the copy step is written down before the first custom bitstream exists.
