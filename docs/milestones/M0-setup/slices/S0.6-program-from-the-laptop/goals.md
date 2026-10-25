# S0.6 Program the FPGA from the laptop

## Goal

Program the BeagleV-Fire FPGA from the laptop, with the programmer attached to the laptop, and record whether that hardware is actually here.

## Features

F0

## In this slice

FlashPro Express on the laptop programs a job file through a FlashPro5 or FlashPro6. If that programmer is not attached, the slice records that and does not block M0. Day-to-day programming stays on the board (S0.5).

## Out of this slice

Copying a laptop build to the board and running `change-gateware.sh` is S0.5 path B. That path does not use a FlashPro.

## Done when

Either `test.md` records a FlashPro Express `PASSED`, or `implementation.md` records that no FlashPro programmer is attached. The procedure in this file is part of the milestone either way.

## Why this is a separate path

S0.5 writes the bitstream into SPI flash from Linux, and HSS loads it on the next boot. That is how this project ships bitstreams.

The laptop path talks JTAG through a FlashPro programmer and FlashPro Express, which is installed with Libero (S0.1). Beagle’s recovery guide uses that path when Linux is not available to run `change-gateware.sh`. It needs extra hardware: a FlashPro5 or FlashPro6, and the Tag-Connect TC2050 cable Beagle lists for the programming header. See <https://docs.beagleboard.org/boards/beaglev/fire/demos-and-tutorials/flashing-board.html>.

A JTAG program does not, by itself, replace the copy in SPI flash. On the next boot HSS can load the previous SPI image back into the fabric. Do not erase SPI flash as part of normal work. Erasing it is a recovery step, used only when a bad gateware prevents Linux from booting, and it is not part of this slice’s passing run.

## Procedure

Skip to the last step if you do not have a FlashPro programmer.

1. Install the udev rule so the programmer is usable without root. Beagle publishes `60-openocd.rules` from the flashing guide.

   ```bash
   sudo cp 60-openocd.rules /etc/udev/rules.d/
   sudo udevadm trigger
   ```

2. Plug the FlashPro into the laptop and into the board’s programming header. Power the board.

3. Start FlashPro Express from the Libero tree. The executable is `FPExpress`, under the Program & Debug tools `bin` directory. S0.1’s install path is the place to look:

   ```bash
   find "$LIBERO_INSTALL_DIR" -name FPExpress -type f
   ```

4. Create a project with Ctrl+N. Choose the `.job` file for the gateware you are programming, then a project directory. The programmer must already be plugged in or the project window will not show it.

5. Set the action to `Program` and press `RUN`. Wait until the status is `PASSED`.

6. Reboot the board and confirm Linux still comes up (S0.4’s SSH or serial check). If the fabric image you programmed is only in the FPGA and SPI still holds the previous one, the reboot loads SPI again. That is expected for a JTAG-only program. Say so in `implementation.md`.

7. If no programmer is attached, do not buy one for M0. Write “FlashPro not attached” in `implementation.md`. S0.5 is the path that must have been run.
