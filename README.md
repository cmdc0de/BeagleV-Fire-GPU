# BeagleV-Fire-GPU

The PolarFire fabric on a BeagleV-Fire, used as a display engine for one SPI panel. Feature and milestone index: [docs/project_goals.md](docs/project_goals.md). The first slice's walkthrough is [docs/slices/m0s1-test-plan.md](docs/slices/m0s1-test-plan.md).

## Setup

Install the FPGA tools on the build laptop, start the license manager, then run the environment check. Libero SoC **v2022.3** is the version this tree builds with. A newer Libero is not a substitute.

### Downloads

- Libero SoC v2022.3 for Linux, from your Microchip account. This is the FPGA IDE. It also provides `pfsoc_mss` and `fpgenprog`.
- SoftConsole, from the same account. It provides `riscv64-unknown-elf-gcc`, the bare-metal compiler the gateware builder uses for the HSS bootloader.
- A Libero license file for this machine. On the build laptop it lives at `/licenses/License.dat`. The license manager binary is `/licenses/lmgrd`.
- The latest BeagleV-Fire Debian IoT image from <https://www.beagleboard.org/distros>. Writing that image to the board is in the S0.1 test plan.

Laptop packages the checker and the builder need:

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip git device-tree-compiler iverilog gcc-riscv64-linux-gnu
pip3 install GitPython PyYAML requests
```

Point a shell file at the install trees, then source it from new terminals. Replace the paths with the ones on this laptop. The directory that contains `riscv64-unknown-elf-gcc` is inside SoftConsole, and its name varies.

```bash
export LIBERO_INSTALL_DIR=$HOME/microchip/Libero_SoC_v2022.3
export SC_INSTALL_DIR=$HOME/microchip/SoftConsole
export FPGENPROG=$LIBERO_INSTALL_DIR/bin/fpgenprog
export LM_LICENSE_FILE=/licenses/License.dat
export PATH="$LIBERO_INSTALL_DIR/bin:<dir-with-riscv64-unknown-elf-gcc>:$PATH"
```

### License manager

Libero cannot obtain a license until `lmgrd` is running. Start it before the environment check, and leave it running:

```bash
/licenses/lmgrd -c /licenses/License.dat -l /licenses/License.log
```

`-c` is the license file. `-l` is the log. A failed checkout is written to `/licenses/License.log`.

`LM_LICENSE_FILE` must name that same license file. The shell snippet above sets it.

### Environment check

With the license manager running and the shell variables set:

```bash
python3 scripts/check-env.py --host
```

Every line must be `PASS`, and the command must exit 0. `libero` has to report 2022.3. On the BeagleV-Fire, after Debian is installed and the board packages from the test plan are in place:

```bash
python3 scripts/check-env.py --board
```

The script does not install tools and does not program the FPGA.
