# S0.7 Environment check script

## Goal

One script reports whether the laptop and the board match the tools the earlier guides installed.

## Features

F0

## In this slice

`scripts/check-env.py` exists, prints one `PASS` or `FAIL` line per tool with the version it found, and exits 0 only when every required item passes.

## Out of this slice

The script does not install missing tools and it does not program the FPGA. S0.1 through S0.5 are the guides. S0.6 is not part of the script, because a FlashPro programmer is optional.

## Done when

`python3 scripts/check-env.py --host` exits 0 on the laptop and `python3 scripts/check-env.py --board` exits 0 on the BeagleV-Fire.

## Procedure

1. Add `scripts/check-env.py` to this repository. It takes `--host` or `--board`. Unknown arguments fail. With no argument it prints usage and exits non-zero.

2. `--host` checks, in this order, and stops only at the end so one run lists every failure:

   - `git` runs.
   - `python3` can import `git` (GitPython), `yaml` (PyYAML), and `requests`.
   - `libero` is on `PATH`. Starting it reports version 2022.3 and does not fail with a license error. Record the invocation that does this in `implementation.md` once it is known. `LM_LICENSE_FILE` is non-empty.
   - `pfsoc_mss` is on `PATH`.
   - `LIBERO_INSTALL_DIR` is a directory.
   - `SC_INSTALL_DIR` is a directory.
   - `FPGENPROG` is an executable file.
   - `riscv-unknown-elf-gcc` is on `PATH` and `--version` exits 0.
   - `dtc --version` exits 0.
   - `iverilog -v` exits 0 and the text names Icarus Verilog.
   - `riscv64-linux-gnu-gcc --version` exits 0.

3. `--board` checks:

   - `gcc --version`, `make --version`, and `dtc --version` exit 0.
   - `/lib/modules/$(uname -r)/build` exists.
   - `/usr/share/beagleboard/gateware/change-gateware.sh` is executable.
   - `uname -m` is `riscv64`.

4. Each line looks like `PASS libero 2022.3` or `FAIL libero not on PATH`. The exit status is 0 only when every line is `PASS`.

5. Run it on both machines after S0.1, S0.2, and S0.4. Fix the guide or the machine, not the script, when a required tool is honestly missing.
