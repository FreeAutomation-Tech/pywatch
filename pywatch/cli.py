import argparse
import os
import subprocess
import sys
import time
import signal

from pywatch import __version__
from pywatch.watcher import watch, _color, GREEN, YELLOW, RED, CYAN, RESET


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="pywatch",
        description="Auto-run commands when files change.",
        epilog="Example: pywatch --ext .py -- pytest",
    )
    parser.add_argument(
        "command",
        nargs="+",
        help="The command to run when files change",
    )
    parser.add_argument(
        "--ext", "-e",
        default=[".py"],
        type=str,
        nargs="*",
        help="File extensions to watch (default: .py)",
    )
    parser.add_argument(
        "--ignore", "-i",
        default=["__pycache__", ".git", ".venv", "node_modules", ".tox", ".eggs", "*.egg-info"],
        type=str,
        nargs="*",
        help="Ignore patterns (default: __pycache__, .git, .venv, node_modules)",
    )
    parser.add_argument(
        "--debounce", "-d",
        default=500,
        type=int,
        help="Debounce time in milliseconds (default: 500)",
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        type=str,
        help="Directory to watch (default: .)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print file change events",
    )
    parser.add_argument(
        "--init", "-n",
        action="store_true",
        help="Run command immediately on start",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pywatch {__version__}",
    )
    return parser.parse_args(argv)


def run_command(cmd_parts):
    start = time.time()
    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=False,
            text=True,
        )
        elapsed = time.time() - start
        if result.returncode != 0:
            print(_color(f"  Command exited with code {result.returncode} ({elapsed:.2f}s)", RED))
        else:
            print(_color(f"  Done in {elapsed:.2f}s", GREEN))
        return result.returncode
    except FileNotFoundError:
        print(_color(f"  Command not found: {' '.join(cmd_parts)}", RED))
        return 1
    except KeyboardInterrupt:
        return 0


def clear_screen():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


def main():
    args = parse_args()

    cmd = args.command
    if len(cmd) == 1:
        cmd = cmd[0].split()

    root = os.path.abspath(args.path)

    if not os.path.isdir(root):
        print(_color(f"  Path does not exist: {root}", RED))
        sys.exit(1)

    ext_list = []
    for e in args.ext:
        if isinstance(e, list):
            ext_list.extend(e)
        else:
            ext_list.append(e)
    ext_list = [e if e.startswith(".") else f".{e}" for e in ext_list]

    ignore_list = args.ignore
    if isinstance(ignore_list, list) and len(ignore_list) == 1 and isinstance(ignore_list[0], list):
        ignore_list = ignore_list[0]

    if args.init:
        print(_color("  Running command (--init)...", CYAN))
        run_command(cmd)

    def on_change(changed_files):
        clear_screen()
        if changed_files:
            rel_paths = [os.path.relpath(p, root) for p in changed_files[:3]]
            display = ", ".join(rel_paths)
            if len(changed_files) > 3:
                display += f" ... and {len(changed_files) - 3} more"
            print(_color(f"  File{'s' if len(changed_files) != 1 else ''} changed: {display}", YELLOW))
            print()
        run_command(cmd)

    def handle_signal(signum, frame):
        print()
        print(_color("  Shutting down pywatch...", YELLOW))
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        watch(
            root=root,
            extensions=ext_list,
            ignore_patterns=ignore_list,
            debounce_ms=args.debounce,
            callback=on_change,
            verbose=args.verbose,
        )
    except KeyboardInterrupt:
        print()
        print(_color("  Shutting down pywatch...", YELLOW))
        sys.exit(0)


if __name__ == "__main__":
    main()
