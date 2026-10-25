# S0.3 test

## Setup

Laptop, BeagleV-Fire, USB-C cable, 3.3 V USB-UART on the debug header.

## Steps

1. Confirm the downloaded file is a BeagleV-Fire Debian IoT image and that its checksum matches the one published next to it.
2. Follow `goals.md` through the write.
3. Before the write, save the `lsblk` line of the target. Read it back and confirm the model is the PolarFire SoC mass-storage device.
4. After the write and the reset, confirm the HSS session accepted `boot` or that the board reset, and that serial output continues. The login proof is S0.4.

## Expected results

- `implementation.md` names the image file, the checksum, and the block device that was written.
- The block device’s model is the board’s eMMC gadget, recorded from `lsblk`.
- The write finishes, and the board is reset into that image.

## Pass record

| Date | Image | Device | Result |
| --- | --- | --- | --- |
| | | | |
