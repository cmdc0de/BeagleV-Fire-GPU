# Project Goals: BeagleV-Fire FPGA GPU (SPI Display Engine)

This file is the contract for the project. It lists every feature, groups them into milestones, and breaks each milestone into slices. A slice is one check-in on the way to a milestone.

Update this file in the same change that adds, drops, retargets, or redefines a feature, milestone, or slice. Detail that does not belong in the index lives in the places named under [Working agreements](#working-agreements).

Status words used below: `planned`, `active`, `done`, `dropped`. IDs stay stable. A dropped feature stays in the list with status `dropped`.

## Project

Use the BeagleV-Fire as a Linux host (hard RISC-V cores) and turn its PolarFire FPGA fabric into a GPU-style display engine. The first version drives one SPI panel from a backbuffer. The fabric exposes a memory-mapped control block. A Linux kernel module binds to that block through a device-tree overlay and presents the device to userspace.

Features land in small slices, in both the HDL and the kernel module, until the fabric (about 23K logic elements) is substantially used and the control interface is still small enough to document on one page.

This is the GPU piece of the larger “yet another processor” system. It is also the learning vehicle for:

- MSS to fabric signaling (APB for control, AXI for framebuffer reads, shared memory, interrupts)
- Verilog on the PolarFire fabric
- Linux kernel modules and device-tree overlays on RISC-V

## Architecture

- **Host.** BeagleV-Fire hard RISC-V cores running Linux.
- **GPU.** PolarFire fabric. Scanout, buffer selection, 2D commands, and a tile rasterizer with one fragment shader.
- **3D.** The RISC-V cores transform vertices, clip, and submit triangles. The fabric rasterizes one pixel at a time inside a tile, tests depth against a tile Z buffer in LSRAM, and runs one straight-line fragment program. Color is written to the DDR framebuffer.
- **Control path.** APB slave on the cape fabric bus, the same style of port the stock Verilog cape template already uses (`FIC_3` clock and reset into the cape). Linux reaches it through a device-tree overlay.
- **Pixel path.** Two stages. First the CPU pushes a frame into a fabric FIFO. Then a fabric AXI initiator reads a framebuffer in LPDDR. Fabric RAM holds a line buffer or a small FIFO. A 240×320 RGB565 frame is about 150 KB, so the framebuffer lives in DDR.
- **Output.** One SPI panel on the cape header (clock, data, chip select, data/command, reset, backlight when the panel has one). The scanout block talks to an output stage. A later HDMI stage can replace the SPI stage without a new command set.
- **Software.** Out-of-tree kernel module in this repo, built against the kernel that is running on the board. Userspace tests live in `userspace/`.

## Constraints

| Topic | Decision |
| --- | --- |
| Host board | BeagleV-Fire |
| Fabric role | Display engine, plus a fixed-point tile rasterizer and one fragment shader |
| 3D | Vertex transform and clipping stay on the RISC-V cores. The fabric shades one fragment at a time. No floating-point, no second shader stage |
| First output | One SPI panel on the cape header |
| Control interface | APB register block, offsets append-only inside a milestone |
| Framebuffer | LPDDR, read by a fabric AXI initiator. A CPU-fed FIFO comes first so a picture does not wait on that master |
| Pixel format on the wire | RGB565 |
| Software | Out-of-tree kernel module + device-tree overlay. Character device first, framebuffer device when scanout exists |
| HDL | Verilog, integrated as a `CAPE_OPTION` |
| HDL home | `support/gateware/sources/FPGA-design/script_support/components/CAPE/GPU/` |
| Build | Existing bitstream builder. Libero SoC **v2022.3**, which is the version this gateware tree documents |
| Environment check | `scripts/check-env.py` passes on the build host and on the board before M1 |
| Scope | Add features until the GPU block uses a substantial share of the fabric |
| Relationship | GPU component of the larger “yet another processor” work |

Linux self-programming ignores a bitstream whose design version matches the one already on the board. Each image programmed from Linux needs a new design version.

## Non-goals

- The discrete MOSFET CPU, and the FPGA CPU emulator
- A hardware vertex shader, floating-point shading, or more than one fragment in flight
- Bringing up the custom ISA or its OS
- HDMI as the first output
- Mainlining the kernel module
- A second display

## Working agreements

1. **This file is the index.** Every feature has a short description here. Milestone membership and slice membership are recorded here. A change to either updates this file in that same change.
2. **Feature files are optional.** Add `docs/features/<id>-<name>.md` when a feature needs a register map, a pin map, a state machine, a coherency rule, or any other design that does not fit in the summary. Link it from the feature entry. If the summary and the feature file disagree, fix them in the same change. The summary stays accurate either way.
3. **Slices are the check-in unit.** Each slice has a directory created when the slice becomes `active`:

   ```
   docs/milestones/<milestone>/slices/<slice>/
     goals.md
     implementation.md
     test.md
   ```

   `goals.md` says what done means, which features the slice touches, and what is deliberately left out.
   `test.md` is the procedure: setup, steps, and expected results (screen, dmesg, register values, or a simulation log).
   `implementation.md` records what the code does not make obvious: pin and timing choices, new offsets, skipped addresses, fabric utilization when a bitstream was built, and the result of running `test.md`. It can be short.

   Write `goals.md` and `test.md` when the slice starts. Fill `implementation.md` as decisions are made. A slice is `done` when `test.md` has been run and the result is written into `implementation.md`.

   Do not create the full slice tree up front. The tables in this file are the plan. M0 is the exception: its `goals.md` files are the step-by-step setup guides, and they are written as part of defining the milestone.

4. **One active slice.** That slice is the next thing to call done. A second slice may be active only when the first is blocked on the board, a license, or a panel. Parking-lot work does not start beside an active slice.
5. **The test is the acceptance bar.** A slice that cannot be checked from `test.md` is not done. Pure logic slices (register file, SPI shifter, fill) name a simulation in `test.md`. Slices that touch pins, the panel, or Linux also name a board procedure.
6. **Offsets stay put.** New registers use new offsets. An offset covered by a done slice stays stable through the end of that milestone. Renumbering is its own slice, and that slice updates every `test.md` that used the old offset.
7. **HDL is a cape option.** New fabric logic is a directory under `script_support/components/CAPE/`, selected with `CAPE_OPTION`, following the gateware README. The bitstream builder is the build. Libero GUI edits that are not saved back into Tcl or Verilog are not part of the design.
8. **Panel and geometry are data.** Init sequences, size, and orientation live in a table or the device tree. The scanout state machine stays independent of one panel’s command list. Slice S3.1 is where the first panel and its cape pins are chosen.
9. **Output stage is a boundary.** SPI is one module behind the pixel source. Later output changes replace that module.
10. **Record fabric use.** Any slice that produces a bitstream writes logic-element, RAM, and math-block counts into its `implementation.md`. After S7.2, if the GPU block is still a small fraction of the 23K logic elements, pull the cursor (F16), the palette (F17), or a nearest-neighbor texture instruction in from the parking lot before adding a new idea.
11. **Done slice docs stay as history.** A later slice supersedes them by saying so in its `goals.md`. Completed `goals.md` files are not rewritten to match a newer plan.

### Slice doc shape

`goals.md`

- Slice id and name
- Goal, in one paragraph
- Features touched
- In this slice
- Out of this slice
- Done when

`test.md`

- Setup (board, cable, panel, bitstream design version, kernel)
- Steps
- Expected results
- Pass record (date, design version, result)

`implementation.md`

- What landed
- Decisions
- Register, pin, and device-tree changes
- Fabric utilization, when a bitstream was built
- Test result
- Follow-ups

## Features

### F0. Project software environment

`planned`. Milestone M0.

The build laptop and the BeagleV-Fire are brought up from written, step-by-step guides, then checked by a script. The laptop guide installs the FPGA IDE (Libero SoC 2022.3) and the rest of the gateware toolchain. The board guide downloads a Debian image, installs it on the eMMC, proves Linux booted, and configures the board. Two more guides program the FPGA: one from Linux on the Beagle, which is the path this project uses, and one from the laptop through a FlashPro programmer when that hardware is attached. `scripts/check-env.py` then prints one pass or fail line per tool and exits non-zero when anything required is missing or the wrong version. A package list without the guides does not finish this feature.

### F1. Build and program gateware

`planned`. Milestone M1.

Build a bitstream from this tree with the existing builder and program it from Linux on the board. The board then boots Linux. The first image can be a stock cape configuration. Later images are the GPU cape. Each Linux-programmed image uses a new design version.

### F2. Control register block

`planned`. Milestone M2. Feature file when the first offsets exist.

An APB slave on the cape exposes identity, version, scratch, enable, and status. Later features add registers beside these. This block is the control path from Linux into the GPU.

### F3. Device tree and kernel binding

`planned`. Milestone M2.

A device-tree overlay describes the register window and, once F10 exists, the interrupt. An out-of-tree module binds to it, maps the window, and reads back identity and scratch. The same module grows the framebuffer and command interfaces in later milestones.

### F4. SPI panel link

`planned`. Milestone M3. Feature file required from S3.1 (pin map, init, timing).

The cape header bit-bangs one SPI panel: clock, data, chip select, data/command, and reset, plus backlight when the panel needs it. The first panel is chosen in S3.1. It must use 3.3 V logic and accept an RGB565 write. The init sequence is data, so a later panel swap edits the table and the pin map.

### F5. Test patterns

`planned`. Milestone M3.

The fabric generates a solid color and one simple pattern with no framebuffer. Linux selects the pattern and the color through F2. This is the first image on the panel.

### F6. Pixel format and geometry

`planned`. Milestone M4. Feature file when width, height, stride, and orientation are fixed.

Pixels in memory are RGB565. Width, height, and stride are registers. Orientation matches the panel so a buffer written by userspace appears upright. The on-the-wire format stays RGB565.

### F7. CPU frame upload

`planned`. Milestone M4.

The CPU writes one full frame through the driver into a fabric FIFO, and the panel shows that frame. This is the first real image. It stays available after F8 as a way to test the panel without the DDR reader.

### F8. DDR framebuffer scanout

`planned`. Milestone M4. Feature file required (AXI path, coherency rule).

The fabric reads a framebuffer in LPDDR using base, stride, width, and height, and sends it to the panel. The driver picks one coherency rule, uncached mapping or an explicit cache clean before scanout, and the slice test checks that rule.

### F9. mmap framebuffer device

`planned`. Milestone M4.

The module registers a framebuffer device. Userspace maps it and writes pixels. A test program fills the buffer and the panel shows the fill.

### F10. Frame-complete interrupt

`planned`. Milestone M4.

The fabric raises an interrupt at the end of a frame and keeps a frame counter. Userspace waits for the next frame through the driver.

### F11. Page flip

`planned`. Milestone M5.

Two buffer bases. A flip request selects the next base. Hardware applies it on a frame boundary. The frame-complete interrupt reports the base that is live.

### F12. Damage-rectangle refresh

`planned`. Milestone M5.

SPI time is the scarce resource: a full RGB565 frame on a small panel is tens of milliseconds. A damage rectangle limits what is sent. Pixels outside that rectangle stay as they are. A one-pixel change must finish faster than a full-frame write.

### F13. Command FIFO

`planned`. Milestone M6. Feature file when opcodes exist.

Fill and blit are words in a small hardware FIFO, with a busy bit and a completion interrupt. The CPU submits a command and waits. It does not write each pixel of an accelerated operation.

### F14. Rectangle fill

`planned`. Milestone M6.

One command fills an axis-aligned rectangle in the backbuffer with a solid RGB565 color.

### F15. Blit

`planned`. Milestone M6.

One command copies an axis-aligned rectangle inside the framebuffer. Same pixel format, no scaling, no blend.

### F16. Hardware cursor

`planned`. Parking lot.

One small sprite is composited at scanout. Position and an enable bit are registers. Moving the cursor does not redraw the backbuffer. This returns to a milestone only when the fabric report after S7.2 still shows a large amount of unused logic.

### F17. Palette or format conversion

`planned`. Parking lot.

Either a palette indexed into RGB565, or a conversion from a wider CPU pixel into RGB565. The panel still receives RGB565. Same return rule as F16.

### F18. Freeze the block for reuse

`planned`. Milestone M7.

Write down the register map, the device-tree binding, and how this block would be reused in the larger machine. Offsets used by done slices stay as they are. The triangle command and the fragment-shader program RAM are part of that map.

### F19. Tile triangle rasterizer

`planned`. Milestone M7. Feature file required (tile size, fixed-point format, triangle command).

The CPU submits triangles that are already transformed and clipped. The fabric walks each triangle one pixel at a time inside a small tile, using edge adders. A 16-bit depth value for the current tile lives in LSRAM. A pixel that passes the depth test is written to the DDR color buffer. The first visible result is a flat-shaded mesh on the panel. Planning budget, to be replaced by synthesis numbers at S6.4 and S7.1: a few thousand to about 8K logic elements and a handful of the 68 math blocks. The MPFS025T has 23K logic elements, 68 math blocks, and about 210 KB of LSRAM, and the MSS fabric interface already uses some of that before the GPU starts.

### F20. Fragment shader

`planned`. Milestone M7. Feature file required (instruction set, register file, program RAM).

One fragment program runs on one pixel at a time. The program is a short straight-line sequence in a small instruction RAM: move, add, multiply, multiply-add, min, max, and a conditional move, across about 16 fixed-point registers (interpolated values, constants, temporaries). The test program is Gouraud shading. There is no vertex shader in the fabric, no floating-point, and no second pixel in flight. A nearest-neighbor texture fetch is parking-lot work, not part of this feature’s first slice.

## Milestones and slices

The original “first milestone” (custom bitstream, pattern on the panel from Linux, module bound through the device tree, documented register interface) is the end of M3. M0 is the setup manual for the laptop and the board. M1 and M2 make M3 testable.

### M0. Laptop and board are set up

`planned`. Features: F0.

Done when the step-by-step guides below have been followed on the build laptop and on the BeagleV-Fire, the board has booted the Debian image, the FPGA has been programmed from the board, and `scripts/check-env.py` exits 0 on both machines. Programming from the laptop is part of the milestone when a FlashPro programmer is attached. The guide for that path is always written.

Each slice’s `goals.md` is the procedure. `test.md` is the proof. `implementation.md` records this machine: distro, installer paths, the exact image file, the disk that was written, and the boot log.

| Slice | Name | Guide |
| --- | --- | --- |
| S0.1 | Laptop and FPGA IDE | Prepare the laptop that builds bitstreams. Install Libero SoC 2022.3, the license, SoftConsole, FPGENPROG, and the bare-metal RISC-V gcc. |
| S0.2 | Laptop project tools | Install Icarus Verilog and the RISC-V Linux cross compiler on that same laptop. |
| S0.3 | Debian on the BeagleV-Fire | Download the Debian IoT image, write it to the eMMC, and boot it. |
| S0.4 | Prove boot and configure the board | Show that Linux came up. Set the password, network, compiler, kernel headers, and `dtc`. |
| S0.5 | Program the FPGA from the Beagle | Copy programming files from the laptop if needed, run `change-gateware.sh` on the board, and show that Linux comes back. |
| S0.6 | Program the FPGA from the laptop | FlashPro Express over a FlashPro programmer. Run it when the programmer is attached. |
| S0.7 | Environment check script | `scripts/check-env.py --host` and `--board` cover S0.1, S0.2, and S0.4. Exit 0 only when every required item passes. |

The guides are in `docs/milestones/M0-setup/slices/`.

### M1. Known-good bitstream

`planned`. Features: F1.

Done when a bitstream built from this tree is programmed from Linux and the board boots Linux again. M0’s check script already passes before this milestone starts.

| Slice | Name | Delivers |
| --- | --- | --- |
| S1.1 | Build a stock image | `build-bitstream.py` produces a stock cape image from this tree. |
| S1.2 | Program and boot | That image is programmed from Linux with a new design version. The board boots, and a stock overlay is present. |

### M2. Linux can see a fabric peripheral

`planned`. Features: F2, F3.

Done when the GPU cape is programmed, the module binds through an overlay, and a scratch register written from Linux reads back.

| Slice | Name | Delivers |
| --- | --- | --- |
| S2.1 | Register block | Identity, version, and scratch in simulation. First register map written into the F2 feature file. |
| S2.2 | GPU cape bitstream | `CAPE_OPTION` `GPU` builds and programs. Design version bumped. |
| S2.3 | Bind from Linux | Overlay plus module. dmesg shows the identity. Scratch write/read passes. |

### M3. The panel shows a fabric pattern

`planned`. Features: F4, F5. First shippable milestone.

Done when Linux selects a solid color, the SPI panel shows it, and the register interface used to do that is written down.

| Slice | Name | Delivers |
| --- | --- | --- |
| S3.1 | Panel contract | Panel part, cape pins, voltage, and init sequence chosen and written into the F4 feature file. |
| S3.2 | SPI master and init | The fabric resets the panel and completes its init sequence. |
| S3.3 | Pattern from Linux | The module selects solid color and one pattern. The panel shows each. |

### M4. A picture from memory

`planned`. Features: F6, F7, F8, F9, F10.

Done when a userspace program maps a framebuffer, fills it, and the panel shows the fill, with a frame-complete interrupt the program can wait on.

| Slice | Name | Delivers |
| --- | --- | --- |
| S4.1 | Geometry contract | RGB565, width, height, stride, and orientation fixed in the F6 feature file and in registers. |
| S4.2 | CPU frame upload | A test image pushed through the driver appears on the panel. |
| S4.3 | DDR scanout and mmap | The fabric reads LPDDR. Userspace maps the buffer and the panel shows what it wrote. Coherency rule tested. |
| S4.4 | Frame interrupt | Frame counter increments. Userspace blocks until the next frame. |

### M5. Tear-free, cheaper updates

`planned`. Features: F11, F12.

Done when an animation flips between two buffers on frame boundaries, and a small damage rectangle updates the panel without a full-frame SPI transfer.

| Slice | Name | Delivers |
| --- | --- | --- |
| S5.1 | Page flip | Two bases. Flip latches on the frame boundary. The interrupt reports the live base. |
| S5.2 | Damage rectangle | A one-pixel change updates the panel and finishes faster than a full-frame write. |
| S5.3 | Animation | A userspace test bounces a rectangle using flip. The panel does not tear the moving edge. |

### M6. A few accelerated commands

`planned`. Features: F13, F14, F15.

Done when userspace can fill a rectangle and copy a rectangle through the command FIFO, and the fabric report is written down.

| Slice | Name | Delivers |
| --- | --- | --- |
| S6.1 | Command FIFO | Submit, busy, and completion. A no-op command completes. |
| S6.2 | Rectangle fill | A filled rectangle appears in the backbuffer and on the panel. |
| S6.3 | Blit | A copied rectangle matches the source. |
| S6.4 | Fabric report | Logic, RAM, and math counts recorded. That report is the budget S7.1 has to fit in. |

### M7. Triangles, one fragment shader, then freeze

`planned`. Features: F19, F20, F18.

Done when a userspace program submits a mesh and the panel shows it flat-shaded with depth, then shows the same mesh through the Gouraud fragment program, and the register map is frozen.

| Slice | Name | Delivers |
| --- | --- | --- |
| S7.1 | Flat triangles | Transform and clip stay on the CPU. The fabric rasterizes a mesh into tiles, tests tile depth, and the panel shows the flat-shaded result in front-to-back order. |
| S7.2 | Fragment program | The driver loads a short program. The Gouraud test shader changes pixel color across a triangle. Utilization is recorded again, and any parking-lot pull (F16, F17, or a texture instruction) is decided here. |
| S7.3 | Freeze and reuse note | Register map, including the triangle command and shader RAM, the binding, and the reuse note checked against the HDL. F18 marked done. |

## Repository layout

```
docs/project_goals.md
docs/features/                          one file per feature, only when needed
docs/milestones/M0-setup/slices/          step-by-step laptop and board guides
docs/milestones/<milestone>/slices/<slice>/{goals,implementation,test}.md
scripts/check-env.py                    M0 install check, --host and --board
kernel/                                 out-of-tree module
userspace/                              tests named by the slice test docs
support/gateware/.../CAPE/GPU/          Verilog cape option
```

## Parking lot

Not in a milestone. Promote an item by giving it a feature id, a milestone, and a changelog line.

| Id | Item |
| --- | --- |
| P1 | A non-SPI output stage (HDMI or similar) behind the same pixel source |
| P2 | A DRM/KMS driver in place of the framebuffer device |
| P3 | A tile or glyph mode |
| P4 | Rotation in the fabric |
| P5 | dma-buf import of a userspace buffer |
| P6 | F16 hardware cursor, only if logic remains after S7.2 |
| P7 | F17 palette or wider-format conversion, only if logic remains after S7.2 |
| P8 | One nearest-neighbor texture instruction in the F20 fragment shader |

## Working choices to confirm

These are the choices the tables above already assume. Replace any of them by editing this file. Nothing is `active` until they are accepted.

1. **HDL home.** GPU Verilog is a `CAPE_OPTION` named `GPU` inside the gateware tree, because that is how this builder selects cape logic. A top-level `hdl/` tree would be a second copy.
2. **Software face.** M2 and M3 use a character device (or sysfs) on the module. M4 adds a framebuffer device for mmap. DRM/KMS stays as P2.
3. **Memory order.** F7 (CPU FIFO upload) lands before F8 (DDR AXI scanout), so the panel can show a real image before the fabric is a bus master.
4. **Refresh before blit.** F12 is in M5, ahead of fill and blit, because SPI time dominates image quality on this panel.
5. **Libero version.** v2022.3, matching `support/gateware/sources/FPGA-design/Readme.md`.
6. **One active slice,** with the exception in agreement 4.
7. **Two machines in M0.** `scripts/check-env.py --host` covers the build machine (Libero, HSS toolchain, simulator, cross compiler). `scripts/check-env.py --board` covers the Beagle (native compiler and headers for the running kernel). Both must pass.
8. **Simulator.** Icarus Verilog (`iverilog`) is the simulator the host check requires.

## References

- BeagleV-Fire gateware in `support/gateware/`
- `support/gateware/sources/FPGA-design/Readme.md` (Libero v2022.3, `CAPE_OPTION`, design version rule)
- Cape Verilog template: `script_support/components/CAPE/VERILOG_TEMPLATE/`
- “Customize BeagleV-Fire Cape Gateware Using Verilog”
- “Exploring Gateware Design with Libero”
- PolarFire SoC MSS Technical Reference (FIC, AXI, APB)

## Changelog

| Date | Change |
| --- | --- |
| 2026-10-25 | Replaced the starting outline with the feature catalog, milestone/slice plan, and working agreements. |
| 2026-10-25 | Eight milestones, M0–M7. M0 is F0: install the host and board tools, then `scripts/check-env.py` must exit 0. The old tooling-and-bitstream milestone is now M1. The original first-milestone definition of done is the end of M3. |
| 2026-10-25 | M7 is a fixed-point tile rasterizer (F19) and one fragment shader (F20), then the register-map freeze. Vertex work stays on the RISC-V cores. F16 and F17 moved to the parking lot. |
| 2026-10-25 | M0 expanded into step-by-step guides: laptop and Libero, Debian on the BeagleV-Fire, boot proof, programming the FPGA from the board, and programming it from the laptop when a FlashPro is attached. |
