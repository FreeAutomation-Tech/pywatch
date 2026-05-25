import os
import time
import fnmatch
import threading


GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def _color(text, color):
    return f"{color}{text}{RESET}"


def _should_ignore(name, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(name, f"*/{pattern}") or name == pattern:
            return True
        if os.path.isdir(name) and pattern.endswith("/"):
            if fnmatch.fnmatch(name, pattern.rstrip("/")):
                return True
    return False


def _walk_files(root, extensions, ignore_patterns):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not _should_ignore(os.path.join(dirpath, d), ignore_patterns)
            and not _should_ignore(d, ignore_patterns)
        ]
        for filename in filenames:
            if _should_ignore(filename, ignore_patterns):
                continue
            if extensions and not any(filename.endswith(ext) for ext in extensions):
                continue
            yield os.path.join(dirpath, filename)


def _get_mtimes(root, extensions, ignore_patterns):
    mtimes = {}
    for filepath in _walk_files(root, extensions, ignore_patterns):
        try:
            mtimes[filepath] = os.stat(filepath).st_mtime
        except FileNotFoundError:
            pass
    return mtimes


def watch(root, extensions, ignore_patterns, debounce_ms, callback, verbose):
    debounce_sec = debounce_ms / 1000.0
    poll_interval = 0.5

    print(_color(f"  Watching: {os.path.abspath(root)}", GREEN))
    if extensions:
        print(_color(f"  Extensions: {', '.join(extensions)}", CYAN))
    print(_color(f"  Ignoring: {', '.join(ignore_patterns)}", CYAN))
    print(_color(f"  Debounce: {debounce_ms}ms", CYAN))
    print()

    mtimes = _get_mtimes(root, extensions, ignore_patterns)
    last_trigger = 0.0
    pending = False

    while True:
        time.sleep(poll_interval)
        changed = []
        current_mtimes = _get_mtimes(root, extensions, ignore_patterns)

        all_paths = set(mtimes.keys()) | set(current_mtimes.keys())
        for path in all_paths:
            old_mtime = mtimes.get(path)
            new_mtime = current_mtimes.get(path)
            if old_mtime is None:
                changed.append(path)
            elif new_mtime is None:
                changed.append(path)
            elif new_mtime != old_mtime:
                changed.append(path)

        if changed:
            mtimes = current_mtimes
            now = time.time()
            if verbose:
                for path in changed:
                    rel = os.path.relpath(path, root)
                    print(_color(f"  Changed: {rel}", YELLOW))
            if now - last_trigger >= debounce_sec:
                last_trigger = now
                pending = False
                callback(changed)
            else:
                pending = True
        elif pending:
            now = time.time()
            if now - last_trigger >= debounce_sec:
                last_trigger = now
                pending = False
                callback([])
