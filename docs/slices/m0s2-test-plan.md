# M0 S0.2 test plan

Program the stock gateware from Linux on the BeagleV-Fire. No display is required. Do not build a bitstream on the laptop for this test.

## Setup

- S0.1 has been followed far enough that the board boots Debian, SSH or serial login works, and `bbb.io-gateware` is installed. `scripts/check-env.py --board` exiting 0 is the check for that package, because it requires `/usr/share/beagleboard/gateware/change-gateware.sh` to be executable.
- A serial console at 115200 on the debug UART or the USB-C serial port. Leave it open for the whole test.
- The board is powered by USB-C or another supply that will stay connected for several minutes.
- No FlashPro programmer is required.

## Steps

1. From the laptop, confirm the board is up:

   ```bash
   ssh beagle@BOARD_IP
   uname -a
   test -x /usr/share/beagleboard/gateware/change-gateware.sh && echo "change-gateware ok"
   ls /usr/share/beagleboard/gateware/default
   ```

   Use the username and address from the S0.1 boot. `uname -a` must contain `riscv64`. The `default` directory must exist.

2. Read the first screen of the script so the invocation matches the file on the board:

   ```bash
   sed -n '1,40p' /usr/share/beagleboard/gateware/change-gateware.sh
   ```

3. Start programming. From `/usr/share/beagleboard/gateware`, if the script is the upstream form:

   ```bash
   cd /usr/share/beagleboard/gateware
   sudo ./change-gateware.sh default
   ```

   If that script instead requires a directory argument and root, use:

   ```bash
   sudo /usr/share/beagleboard/gateware/change-gateware.sh /usr/share/beagleboard/gateware/default
   ```

4. Leave the power cable in place. Do not press Reset. Wait until the serial console shows the board reboot itself and a Linux login prompt appears. This can take a few minutes. SSH will drop while the board is down.

5. Log in again over serial or SSH and run:

   ```bash
   uname -a
   ```

## Expected results

- Step 1 prints a `riscv64` `uname -a`, prints `change-gateware ok`, and lists the `default` gateware directory.
- Step 3 starts programming. It does not print `No directory found` or `No xxx gateware file found.`
- Step 4: the serial log shows a reboot that was not caused by unplugging power or pressing Reset. Linux prints a login prompt.
- Step 5: login works and `uname -a` contains `riscv64`.
- If the serial log prints a design version, copy that line into the pass record. A same-version program that Linux ignores is still a pass when the script ran and Linux came back.

## Pass record

| Date | Gateware directory | Design version line, if printed | Result |
| --- | --- | --- | --- |
| 2026-11-05 | | | passed, user confirmed via /implement-m close |
