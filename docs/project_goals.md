# Project Goals: BeagleV-Fire FPGA GPU (SPI Display Engine)

## Project Description

Use the BeagleV-Fire as a Linux host (hard RISC-V cores) and turn its PolarFire FPGA fabric into a GPU-style display engine. The first version drives an SPI display with a backbuffer. The fabric exposes a clean memory-mapped control interface; a Linux kernel module binds to it and presents the device to userspace. Features are added iteratively in both the HDL and the kernel driver until the ~23K logic elements are substantially used.

This project is the GPU FPGA piece of the larger “yet another processor” system. It also serves as a focused learning vehicle for:

- MSS ↔ fabric signaling (AXI/APB, shared memory, interrupts)
- Pure HDL (Verilog) development on the PolarFire fabric
- Linux kernel modules and device-tree overlays on RISC-V

## High-Level Architecture

- **Host**: BeagleV-Fire hard RISC-V cores running Linux.
- **GPU**: PolarFire fabric implementing scanout, backbuffer management, and (later) simple acceleration.
- **Output**: SPI display (first version). HDMI or other outputs can be added later by swapping the output stage.
- **Interface**: AXI (or APB) registers + framebuffer region visible to the MSS. Device-tree overlay describes the peripheral. Kernel module binds to it.
- **Memory**: Start with on-fabric buffer or a small region of LPDDR4 reachable over AXI; grow as needed.

## Constraints and Decisions

| Topic              | Decision                                                                 |
|--------------------|--------------------------------------------------------------------------|
| Host board         | BeagleV-Fire                                                             |
| Fabric role        | GPU display engine (not the custom CPU emulator in this project)         |
| First output       | SPI display                                                              |
| Interface          | Memory-mapped registers + framebuffer via AXI/APB                        |
| Software side      | Linux kernel module + device-tree overlay                                |
| HDL                | Verilog (primary)                                                        |
| Scope              | Iteratively add features until fabric is largely used                    |
| Relationship       | GPU component of the larger “yet another processor” goals                |

## Non-Goals (this project)

- Discrete MOSFET CPU or the FPGA CPU emulator
- 3D / shader GPU
- Full OS bring-up of the custom ISA (that belongs to the larger project)
- HDMI as the first output (can be a later stage)

## Suggested Order of Work

1. **Tooling and baseline**
   - Install Microchip Libero (version expected by the BeagleV-Fire gateware, commonly 2023.2).
   - Clone the official gateware repository and successfully build + program a known-good bitstream using the board’s Linux self-programming path (`change-gateware.sh`).
   - Confirm device-tree overlays are generated and applied.

2. **Minimal fabric design**
   - Start from the cape Verilog template.
   - Add a small AXI (or APB) slave with a handful of control/status registers (enable, framebuffer base, mode, status).
   - Add a trivial SPI bit-banger that can clock out fixed patterns.
   - Optional: tiny on-fabric buffer so patterns can be generated without DDR yet.

3. **Bring-up from Linux**
   - Device-tree overlay that describes the control registers.
   - Minimal kernel module (or even `/dev/mem` first) that can read/write the registers.
   - Confirm the SPI display shows hard-coded patterns.

4. **Real backbuffer + first kernel driver**
   - Move to a proper framebuffer region (on-fabric or LPDDR4 via AXI).
   - Kernel module that ioremaps registers, registers a framebuffer device (or exposes a simple character device), and handles basic page-flip or vsync if desired.
   - Userspace test that fills the buffer and sees the result on the display.

5. **Iterative feature growth**
   - Double buffering / page flipping.
   - Simple blit or rectangle fill in the fabric.
   - Higher resolution or additional color depths.
   - Optional DMA-style transfer from the RISC-V side.
   - Interrupt-driven completion notification.
   - Continue until LUT usage is high and the control interface remains clean.

6. **Polish and documentation**
   - Clean register map.
   - Updated device-tree binding description.
   - Notes on how the same GPU block can later be reused in the larger custom-machine project.

## First Milestone Definition of Done

- Custom bitstream programmed on the BeagleV-Fire.
- SPI display shows a solid color or simple pattern written from Linux.
- Kernel module loads, binds via device-tree overlay, and can update the display.
- Clear, documented AXI register interface between the fabric GPU and the MSS.

## Repository / Artifact Layout (suggested)

```
docs/                  this file, register map, notes
hdl/                   Verilog sources (or the customized cape template)
kernel/                kernel module sources
dt/                    device-tree overlay
userspace/             simple test programs
```

## References

- BeagleV-Fire gateware repository and docs (openbeagle.org / docs.beagleboard.org)
- “Customize BeagleV-Fire Cape Gateware Using Verilog”
- “Exploring Gateware Design with Libero”
- PolarFire SoC MSS Technical Reference (FIC / AXI details)

---

This document is the starting contract for the BeagleV-Fire FPGA GPU project. Update it as decisions are made.
