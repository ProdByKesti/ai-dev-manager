"""Check the tools required for the dependency-free Rust baseline."""
import re
import shutil
import subprocess
import sys

MINIMUM = (1, 100, 0)


def check_tool(name):
    path = shutil.which(name)
    if path is None:
        return f"{name} not found on PATH; configure an existing stable {name} 1.100.0 or newer."
    try:
        result = subprocess.run([path, "--version"], capture_output=True, text=True,
                                timeout=10, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Cannot run {name} --version ({exc}); check the existing tool installation."
    if result.returncode != 0:
        return f"{name} --version failed (exit {result.returncode}); check the existing tool installation."
    match = re.fullmatch(rf"{name} (\d+)\.(\d+)\.(\d+)(?: \([^\r\n]*\))?\s*", result.stdout)
    if not match:
        return f"Unrecognized or non-stable {name} version; use stable {name} 1.100.0 or newer."
    version = tuple(map(int, match.groups()))
    if version < MINIMUM:
        return f"{name} {'.'.join(map(str, version))} is too old; use stable {name} 1.100.0 or newer."
    return None


def main():
    errors = []
    if sys.version_info < (3, 11):
        errors.append("Python 3.11 or newer is required; run this script with an existing compatible Python.")
    for name in ("rustc", "cargo"):
        error = check_tool(name)
        if error:
            errors.append(error)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Toolchain requirements satisfied: Python >= 3.11, stable rustc and cargo >= 1.100.0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
