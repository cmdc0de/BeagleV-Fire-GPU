# S0.4 Prove boot and configure the board

## Goal

Show that the BeagleV-Fire booted the Debian image, then configure it so later slices can build a kernel module on it and program the FPGA from it.

## Features

F0

## In this slice

A login on the new image, a recorded kernel version, a working network, and the board packages from `test.md`.

## Out of this slice

Programming the FPGA is S0.5. The check script is S0.7.

## Done when

`test.md` passes, including a saved copy of the boot evidence in `implementation.md`.

## Procedure

The official ways to reach a shell are listed in the gateware upgrade guide: <https://docs.beagleboard.org/boards/beaglev/fire/demos-and-tutorials/gateware/upgrade-gateware.html>. Use the serial console for the first proof. Use SSH after the network is up.

1. Power the board from USB-C and wait for Linux. On the debug UART from S0.3, or on the USB-C serial port that appears on the laptop (`dmesg | grep tty`, often `/dev/ttyACM0`):

   ```bash
   tio /dev/ttyACM0 -b 115200
   ```

2. Log in with the user and password set in S0.3. A factory image that was never reflashed uses `beagle` / `temppwd` for Cockpit. A board you just flashed uses the `sysconf.txt` password. Change it if it is still a published default:

   ```bash
   passwd
   ```

3. Capture the boot identity. This is the proof the Debian image is the one running.

   ```bash
   hostnamectl
   cat /etc/os-release
   uname -a
   ip -br addr
   ```

   Copy that output into `implementation.md`. `uname -a` must show a riscv64 kernel.

4. Give the board a network path. Ethernet is the straightforward one. USB networking on the gadget interface uses `192.168.7.2` from the laptop. Confirm from the laptop:

   ```bash
   ping -c 3 192.168.7.2
   ```

   Or ping the Ethernet address printed by `ip -br addr`. Then, from the laptop:

   ```bash
   ssh beagle@192.168.7.2
   ```

   Use the username you set. SSH reaching a shell is the second proof, after the serial log.

5. Update the package index and install the packages this project builds with on the board. The board needs a network for this.

   ```bash
   sudo apt update
   sudo apt install build-essential device-tree-compiler bbb.io-gateware
   ```

   `bbb.io-gateware` provides `/usr/share/beagleboard/gateware` and `change-gateware.sh`, which S0.5 uses.

6. Install kernel headers that match the running kernel. The package name depends on the image, so ask the image before guessing:

   ```bash
   uname -r
   apt-cache search linux-headers | head
   ```

   Install the headers package whose version matches `uname -r`, then confirm the build link exists:

   ```bash
   ls -d /lib/modules/$(uname -r)/build
   ```

   Record the exact package name in `implementation.md`.

7. Optional desk check from a browser on the laptop: `https://beaglev.localdomain:9090/` is Cockpit on the stock networking setup. Serial plus SSH is the proof this slice requires. Cockpit is extra.
