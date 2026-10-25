# S0.1 test

## Setup

The build laptop, after following `goals.md`. A new terminal, so the environment comes from shell startup and not from a one-off `export`.

## Steps

1. Open a new terminal.
2. Run:

   ```bash
   command -v libero
   command -v pfsoc_mss
   command -v riscv-unknown-elf-gcc
   riscv-unknown-elf-gcc --version
   test -x "$FPGENPROG" && echo "fpgenprog ok"
   test -d "$LIBERO_INSTALL_DIR" && echo "libero dir ok"
   test -d "$SC_INSTALL_DIR" && echo "softconsole dir ok"
   test -n "$LM_LICENSE_FILE" && echo "license var ok"
   dtc --version
   python3 -c "import git, yaml, requests; print('python ok')"
   git --version
   ```

3. Start Libero. Confirm it obtains a license and reports version 2022.3.

## Expected results

- Every `command -v` prints a path.
- `riscv-unknown-elf-gcc --version` and `dtc --version` print a version.
- The three `echo` lines print.
- Python prints `python ok`.
- Libero’s window or version text says 2022.3 and does not stop on a license error.

## Pass record

| Date | Result |
| --- | --- |
| | |
