# M0 S0.1 test plan

Walk these steps on the build laptop and the BeagleV-Fire. No display and no FPGA programming are required. The image write can erase a disk. Confirm the target with `lsblk` before writing.

## Setup

- A Linux laptop. Ubuntu 20.04 is the distro this gateware tree was tested on. Record the distro you actually use.
- A Microchip account that can download Libero SoC v2022.3 and SoftConsole, and a license file for this machine.
- BeagleV-Fire, a USB-C cable, and a 3.3 V USB-to-UART adapter on the board's debug header.
- `tio` on the laptop (`sudo apt-get install tio`).
- The debug-header UART is how you reach the HSS prompt and expose the eMMC. The USB-C serial port appears only after Linux is up. They are different ports.

## Steps

1. On the laptop, install the packages the builder needs and the two project compilers.

   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip git device-tree-compiler iverilog gcc-riscv64-linux-gnu
   pip3 install GitPython PyYAML requests
   ```

2. Install Libero SoC **v2022.3** and SoftConsole under a directory you choose, such as `~/microchip`. Do not substitute a newer Libero. Point a shell file, for example `~/beaglev-fpga-env.sh`, at the paths you find in those trees, then source it from new shells.

   ```bash
   export LIBERO_INSTALL_DIR=$HOME/microchip/Libero_SoC_v2022.3
   export SC_INSTALL_DIR=$HOME/microchip/SoftConsole
   export FPGENPROG=$LIBERO_INSTALL_DIR/bin/fpgenprog
   export LM_LICENSE_FILE=/licenses/License.dat
   export PATH="$LIBERO_INSTALL_DIR/bin:<dir-with-riscv64-unknown-elf-gcc>:$PATH"
   ```

   Replace the install paths with the ones on this laptop. `fpgenprog` and the bare-metal gcc are not always in those exact subdirectories. The license file for this machine is `/licenses/License.dat`. Start the license manager and leave it running before the proof in the next step:

   ```bash
   /licenses/lmgrd -c /licenses/License.dat -l /licenses/License.log
   ```

   Checkout failures are written to `/licenses/License.log`. `command -v` after a new terminal is the check.

3. Open a new terminal and run the laptop proof:

   ```bash
   command -v libero
   command -v pfsoc_mss
   command -v riscv64-unknown-elf-gcc
   riscv64-unknown-elf-gcc --version
   riscv64-linux-gnu-gcc --version
   iverilog -v
   test -x "$FPGENPROG" && echo "fpgenprog ok"
   test -d "$LIBERO_INSTALL_DIR" && echo "libero dir ok"
   test -d "$SC_INSTALL_DIR" && echo "softconsole dir ok"
   test -n "$LM_LICENSE_FILE" && echo "license var ok"
   dtc --version
   git --version
   python3 -c "import git, yaml, requests; print('python ok')"
   ```

   Start Libero and let it obtain a license. The version it shows must be 2022.3.

4. Download the latest BeagleV-Fire Debian IoT image from <https://www.beagleboard.org/distros>. Check the published checksum. Record the filename. If the image page says to set the password in `sysconf.txt` on the FAT partition, do that before the first Linux boot. Do not leave a published default password in place on a network.

5. Connect the 3.3 V UART adapter to the debug header and to the laptop. Connect the board's USB-C port to the laptop. Find the adapter's device with `dmesg | tail -n 30`, then:

   ```bash
   tio /dev/ttyUSB0 -b 115200
   ```

   Use the device name from `dmesg`. Press Reset. When the HSS progress bar appears, press a key until the prompt is `>>`.

6. At the HSS prompt, expose the eMMC:

   ```text
   >> mmc
   >> usbdmsc
   ```

7. On the laptop, find the new disk. Run `lsblk -o NAME,SIZE,MODEL,TRAN` before and after step 6 if you can. The new disk's model looks like `MCC PolarFireSoC_msd`. Write the image only to that device. Etcher can select that target. On the command line, after checking the name a second time:

   ```bash
   sudo dd if=/path/to/sdcard.img of=/dev/sdX bs=1M status=progress conv=fsync
   ```

   Use the decompressed image, or `bmaptool` with the published `.bmap`. `/dev/sdX` is the device from `lsblk`, not the laptop's system disk.

8. When the write finishes, press Ctrl+C in the HSS session, then type `boot` or press Reset.

9. Wait for Linux. Log in on the debug UART, or on the USB-C serial port that appears (`dmesg | grep tty`, often `/dev/ttyACM0`, 115200). Use the password from step 4. If it is still a published default, change it:

   ```bash
   passwd
   ```

10. On the board, capture the boot proof and the address:

    ```bash
    cat /etc/os-release
    uname -a
    ip -br addr
    ```

    From the laptop, reach that address. USB networking uses `192.168.7.2`. Then SSH in and run `uname -a` again.

    ```bash
    ping -c 3 192.168.7.2
    ssh beagle@192.168.7.2
    ```

    Use the username you set.

11. On the board, with a network path, install the packages the next slice needs and the headers that match the running kernel. The headers package name depends on the image. Search before installing.

    ```bash
    sudo apt update
    sudo apt install build-essential device-tree-compiler bbb.io-gateware
    uname -r
    apt-cache search linux-headers | head
    ```

    Install the headers package whose version matches `uname -r`. Then:

    ```bash
    gcc --version
    make --version
    dtc --version
    ls -d /lib/modules/$(uname -r)/build
    test -x /usr/share/beagleboard/gateware/change-gateware.sh && echo "change-gateware ok"
    ```

    Do not run `change-gateware.sh`.

12. From a checkout of this repository, run the check script on the laptop in a new terminal, and on the board:

    ```bash
    python3 scripts/check-env.py --host
    python3 scripts/check-env.py --board
    python3 scripts/check-env.py
    ```

    Copy the script to the board first if the checkout is only on the laptop. The no-argument run is expected to fail.

## Expected results

- After step 3, every `command -v` prints a path, both RISC-V compilers and `iverilog` and `dtc` print a version, the three `echo` lines appear, and Python prints `python ok`. Libero shows 2022.3 and does not stop on a license error. `iverilog -v` names Icarus Verilog.
- After step 7, `lsblk` shows the PolarFire SoC mass-storage device as the only disk that was written. The write finishes.
- After step 10, `/etc/os-release` names Debian, `uname -a` contains `riscv64`, and SSH from the laptop prints that same `uname -a`. No display is attached.
- After step 11, `gcc`, `make`, and `dtc` print versions, the kernel `build` directory exists, and the script check prints `change-gateware ok`.
- After step 12, `--host` and `--board` each print only `PASS` lines and exit 0. The run with no arguments exits non-zero.

## Pass record

| Date | Image file | Block device written | Host check | Board check | Result |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
