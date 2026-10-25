# S0.5 test

## Setup

S0.4 passed. Serial console open. SSH works. `bbb.io-gateware` is installed. The board is on external or USB-C power that will stay connected for several minutes.

## Steps

1. From a shell on the board, run path A in `goals.md` (`change-gateware.sh` on the stock `default` directory).
2. Watch the serial console. Wait until the board reboots itself and Linux prints a login prompt.
3. SSH in again and run `uname -a`.

## Expected results

- The script starts programming and does not print “No directory found” or “No xxx gateware file found.”
- The board reboots without the power cable being removed.
- Linux comes back. `uname -a` still shows riscv64.
- `implementation.md` notes the time it took and any design-version line the serial log printed.

## Pass record

| Date | Gateware directory | Result |
| --- | --- | --- |
| | default | |
