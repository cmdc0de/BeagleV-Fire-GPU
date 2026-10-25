# S0.3 Debian on the BeagleV-Fire

## Goal

Download a Debian image for the BeagleV-Fire and install it on the board’s eMMC.

## Features

F0

## In this slice

A current BeagleV-Fire Debian IoT image is written to the eMMC and the board is told to boot it.

## Out of this slice

Logging in, accounts, packages, and kernel headers are S0.4. Programming the FPGA is S0.5 and S0.6.

## Done when

The image filename and the block device that was written are recorded in `implementation.md`, and S0.4 can log in. S0.3 itself ends when the flash finishes and the board is reset into the new image.

## Hardware

- The build laptop from S0.1
- BeagleV-Fire and a USB-C cable
- A 3.3 V USB-to-UART adapter on the board’s UART debug header
- The laptop’s serial tool: `sudo apt-get install tio`

The USB-C port later provides a Linux serial console. The debug header is what reaches the Hart Software Services (HSS) prompt used to expose the eMMC. Those are two different serial ports.

## Procedure

Follow the BeagleBoard flashing guide: <https://docs.beagleboard.org/boards/beaglev/fire/demos-and-tutorials/flashing-board.html>. The steps below are that eMMC path.

1. On the laptop, open <https://www.beagleboard.org/distros> and download the latest **BeagleV-Fire Debian IoT** image. When this guide was written, that image was **BeagleV-Fire Debian 13 2026-07-25 IoT (v6.12.x)**, kernel `linux4microchip+fpga-2025.10`. If a newer BeagleV-Fire Debian IoT image is listed, use that one. Record the exact filename and its checksum in `implementation.md`.

2. The image page says to set the user password in `sysconf.txt` on the FAT partition before the first boot, or to set it in bb-imager. If you flash with Etcher, mount the FAT partition after the write (step 8) and set the password there before the first Linux boot. Do not leave the published default password as the one you use on a network.

3. Connect the 3.3 V UART adapter to the debug header. Connect the adapter to the laptop. Connect the board’s USB-C port to the laptop so the eMMC can appear as a USB disk.

4. Find the UART device the adapter just created:

   ```bash
   dmesg | tail -n 30
   ```

   Note the new `ttyUSB` or `ttyACM` name.

5. Open that port at 115200 baud:

   ```bash
   tio /dev/ttyUSB0 -b 115200
   ```

   Use the name from step 4.

6. Press the board’s Reset button. When the HSS progress bar appears, press a key (0-9 or a-z) until the prompt is `>>`. That stops the normal boot and leaves you in HSS.

7. At the HSS prompt, expose the eMMC as a USB disk:

   ```text
   >> mmc
   >> usbdmsc
   ```

8. On the laptop, identify the new disk before writing anything.

   ```bash
   lsblk -o NAME,SIZE,MODEL,TRAN,MOUNTPOINT
   ```

   Run it once before `usbdmsc` if you can, and again after. The new disk is the one that appeared, with a model string like `MCC PolarFireSoC_msd`. Record `NAME`, `SIZE`, and `MODEL` in `implementation.md`. The device will look like `/dev/sdX` or `/dev/mmcblkN`. It is not the laptop’s own system disk.

9. Write the image to that device only.

   Etcher: select the downloaded image, select the PolarFire SoC mass-storage target from step 8, and flash it.

   Or, on Linux, after confirming the device name a second time against `lsblk`:

   ```bash
   sudo dd if=/path/to/sdcard.img of=/dev/sdX bs=1M status=progress conv=fsync
   ```

   Use the decompressed `.img`. If the download is `.img.xz`, decompress it first or use `bmaptool` with the published `.bmap`. Replace `/dev/sdX` with the device from step 8. `dd` to the wrong device erases the laptop.

10. When the write finishes, return to the HSS serial session, press Ctrl+C to leave `usbdmsc`, then type `boot` or press Reset.

11. Leave the serial adapter connected. S0.4 uses the next boot log as the proof.
