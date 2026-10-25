# S0.4 test

## Setup

The board just flashed in S0.3, powered by USB-C, with a serial cable or the USB-C serial port at 115200.

## Steps

On the board, after login:

```bash
cat /etc/os-release
uname -a
ip -br addr
gcc --version
make --version
dtc --version
ls -d /lib/modules/$(uname -r)/build
test -x /usr/share/beagleboard/gateware/change-gateware.sh && echo "change-gateware ok"
```

From the laptop, SSH to the address found above and run `uname -a` again.

## Expected results

- `/etc/os-release` names Debian.
- `uname -a` contains `riscv64` and a kernel version.
- `ip -br addr` shows an address the laptop can reach.
- `gcc`, `make`, and `dtc` print versions.
- The kernel `build` directory exists.
- The script check prints `change-gateware ok`.
- SSH from the laptop prints the same `uname -a`.
- `implementation.md` contains the command output and the headers package name.

## Pass record

| Date | Kernel (`uname -r`) | Result |
| --- | --- | --- |
| | | |
