#!/usr/bin/env python3
"""Check the S0.1 laptop or BeagleV-Fire tool set.

Print one PASS or FAIL line per tool. Exit 0 only when every line is PASS.
This script does not install tools and does not program the FPGA.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LIBERO_VERSION = "2022.3"
LIBERO_TIMEOUT_S = 180
TOOL_TIMEOUT_S = 30
CHANGE_GATEWARE = Path("/usr/share/beagleboard/gateware/change-gateware.sh")

LICENSE_FAILURES = (
    "checkout failed",
    "unable to check out",
    "unable to checkout",
    "failed to check out",
    "license checkout failed",
    "flexnet licensing error",
    "cannot find license file",
)


def usage():
    print(
        "usage: check-env.py --host | --board\n"
        "  --host   FPGA tools and cross compilers on the build laptop\n"
        "  --board  compiler, headers, and gateware script on the BeagleV-Fire",
        file=sys.stderr,
    )


def result(ok, name, detail):
    print(f"{'PASS' if ok else 'FAIL'} {name} {detail}")
    return ok


def run(cmd, timeout):
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        out = _as_text(exc.stdout) + _as_text(exc.stderr)
        return None, out or "timed out"
    except OSError as exc:
        return None, str(exc)
    return completed.returncode, (completed.stdout or "") + (completed.stderr or "")


def _as_text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def first_line(text):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "no output"


def check_version(name, cmd, timeout=TOOL_TIMEOUT_S):
    if shutil.which(cmd[0]) is None:
        return result(False, name, "not on PATH")
    code, text = run(cmd, timeout)
    if code is None:
        return result(False, name, first_line(text))
    if code != 0:
        return result(False, name, f"exit {code}")
    return result(True, name, first_line(text))


def check_python_import(module, label):
    code, _text = run([sys.executable, "-c", f"import {module}"], TOOL_TIMEOUT_S)
    if code == 0:
        return result(True, label, module)
    return result(False, label, f"cannot import {module}")


def check_libero():
    if shutil.which("libero") is None:
        return result(False, "libero", "not on PATH")
    tcl = (
        'if {[info commands get_libero_version] ne ""} {\n'
        "  puts [get_libero_version]\n"
        '} elseif {[info commands get_libero_release] ne ""} {\n'
        "  puts [get_libero_release]\n"
        "} else {\n"
        '  puts "NO_VERSION_COMMAND"\n'
        "}\n"
        "exit 0\n"
    )
    with tempfile.TemporaryDirectory(prefix="check-env-") as directory:
        script = Path(directory) / "print_version.tcl"
        script.write_text(tcl, encoding="utf-8")
        code, text = run(["libero", f"SCRIPT:{script}"], LIBERO_TIMEOUT_S)
    lowered = text.lower()
    if any(phrase in lowered for phrase in LICENSE_FAILURES):
        return result(False, "libero", "license checkout failed")
    if code is None:
        return result(False, "libero", first_line(text))
    if code != 0:
        return result(False, "libero", f"exit {code}: {first_line(text)}")
    if LIBERO_VERSION not in text:
        return result(False, "libero", f"version is not {LIBERO_VERSION}")
    return result(True, "libero", LIBERO_VERSION)


def check_env_dir(name):
    value = os.environ.get(name)
    if not value:
        return result(False, name, "not set")
    if not Path(value).is_dir():
        return result(False, name, "not a directory")
    return result(True, name, value)


def check_fpgenprog():
    value = os.environ.get("FPGENPROG")
    if not value:
        return result(False, "FPGENPROG", "not set")
    path = Path(value)
    if not path.is_file() or not os.access(path, os.X_OK):
        return result(False, "FPGENPROG", "not an executable file")
    return result(True, "FPGENPROG", value)


def check_license_var():
    value = os.environ.get("LM_LICENSE_FILE")
    if not value:
        return result(False, "LM_LICENSE_FILE", "not set")
    return result(True, "LM_LICENSE_FILE", "set")


def check_on_path(name):
    found = shutil.which(name)
    if found is None:
        return result(False, name, "not on PATH")
    return result(True, name, found)


def check_iverilog():
    if shutil.which("iverilog") is None:
        return result(False, "iverilog", "not on PATH")
    # -v prints the version banner and then exits 1 because no source file was given.
    code, text = run(["iverilog", "-v"], TOOL_TIMEOUT_S)
    if code is None:
        return result(False, "iverilog", first_line(text))
    if "Icarus Verilog" not in text:
        return result(False, "iverilog", "output does not name Icarus Verilog")
    return result(True, "iverilog", first_line(text))


def check_host():
    checks = [
        check_version("git", ["git", "--version"]),
        check_python_import("git", "GitPython"),
        check_python_import("yaml", "PyYAML"),
        check_python_import("requests", "requests"),
        check_libero(),
        check_license_var(),
        check_on_path("pfsoc_mss"),
        check_env_dir("LIBERO_INSTALL_DIR"),
        check_env_dir("SC_INSTALL_DIR"),
        check_fpgenprog(),
        check_version("riscv64-unknown-elf-gcc", ["riscv64-unknown-elf-gcc", "--version"]),
        check_version("dtc", ["dtc", "--version"]),
        check_iverilog(),
        check_version("riscv64-linux-gnu-gcc", ["riscv64-linux-gnu-gcc", "--version"]),
    ]
    return all(checks)


def check_board():
    code, machine = run(["uname", "-m"], TOOL_TIMEOUT_S)
    machine = machine.strip()
    arch_ok = code == 0 and machine == "riscv64"
    build = Path("/lib/modules") / os.uname().release / "build"
    checks = [
        check_version("gcc", ["gcc", "--version"]),
        check_version("make", ["make", "--version"]),
        check_version("dtc", ["dtc", "--version"]),
        result(build.exists(), "kernel-headers", str(build) if build.exists() else "build directory missing"),
        result(
            CHANGE_GATEWARE.is_file() and os.access(CHANGE_GATEWARE, os.X_OK),
            "change-gateware.sh",
            str(CHANGE_GATEWARE) if CHANGE_GATEWARE.is_file() else "not executable",
        ),
        result(arch_ok, "uname-m", machine or "unknown"),
    ]
    return all(checks)


def main(argv):
    if not argv:
        usage()
        return 2
    if argv == ["--host"]:
        return 0 if check_host() else 1
    if argv == ["--board"]:
        return 0 if check_board() else 1
    usage()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
