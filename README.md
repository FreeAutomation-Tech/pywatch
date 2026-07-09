<div align="center">
  <h1>PyWatch <g-emoji class="g-emoji" alias="eyes">👀</g-emoji></h1>
  <p><strong>Auto-run commands when files change — because you have better things to do.</strong></p>

  <p>
    <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+">
    <img src="https://img.shields.io/github/license/FreeAutomation-Tech/pywatch" alt="License">
    <img src="https://img.shields.io/github/stars/FreeAutomation-Tech/pywatch?style=social" alt="GitHub stars">
    <img src="https://img.shields.io/badge/PRs-welcome-green" alt="PRs Welcome">
  </p>
</div>

---

## Why PyWatch?

You know the drill: you make a change, switch to your terminal, press <kbd>↑</kbd> + <kbd>Enter</kbd>, wait for tests, see a failure, fix it, switch back, repeat. Every context switch costs you focus.

**PyWatch eliminates the loop.** It watches your project directory, and the instant a file changes, it runs your command — automatically. No alt-tabbing. No keystrokes. Just code and see results.

```
# Instead of this:
#   edit file → alt-tab → ↑ → Enter → wait → alt-tab → edit → repeat

# Do this:
$ pywatch "pytest"

# Now every time you save a .py file, pytest runs automatically.
```

---

## Quick Start

```bash
pip install pywatch
```

Then in any project:

```bash
pywatch "pytest"
```

That's it. Every time a `.py` file changes, `pytest` re-runs. Watch your terminal while you code.

---

## Features

| Feature | Description |
|---|---|
| **File Watching** | Watches entire directory trees recursively |
| **Debouncing** | Groups rapid changes into a single trigger (configurable) |
| **File Filtering** | Watch only specific extensions (`.py`, `.js`, `.rs`, etc.) |
| **Ignore Patterns** | Skip `__pycache__`, `.git`, `node_modules`, `.venv`, and custom paths |
| **Colored Output** | Green for watching, yellow for changes, red for errors |
| **Execution Timing** | Shows how long each command took |
| **Initial Run** | Option to run the command immediately on start (`--init`) |
| **Verbose Mode** | See exactly which files changed |
| **Graceful Exit** | <kbd>Ctrl</kbd>+<kbd>C</kbd> cleans up with a message |
| **Zero Dependencies** | Pure Python — uses `os.stat` polling, cross-platform |

---

## How It Works

PyWatch uses **polling** via `os.stat` to check file modification times every 500ms. No external dependencies, no C extensions, no platform-specific filesystem events — it works everywhere Python runs.

When a change is detected:

1. The screen clears
2. Changed file names are printed
3. A **debounce timer** starts (default 500ms)
4. If more files change during the timer, they're grouped
5. Once the timer expires, your command runs
6. Execution time is printed

---

## Advanced Usage

### Watch multiple extensions

```bash
pywatch --ext .py .js .tsx "npm test"
```

### Ignore additional paths

```bash
pywatch --ignore __pycache__ .git .venv build dist "make"
```

### Change debounce window

```bash
pywatch --debounce 200 "flake8 ."
```

### Watch a specific directory

```bash
pywatch --path src "ruff check ."
```

### Run command immediately on start

```bash
pywatch --init "pytest -x"
```

### Verbose mode (see every file change)

```bash
pywatch --verbose "python -m unittest"
```

### Combined usage

```bash
pywatch -e .py .md -i __pycache__ .git -d 300 -p ./app -n -v "pytest -v"
```

---

## Example Workflows

**TDD loop:**
```bash
pywatch --init "pytest --tb=short"
```

**Lint on save:**
```bash
pywatch --ext .py "ruff check --fix ."
```

**Build on save:**
```bash
pywatch --ext .md "mkdocs build"
```

**Compile + test:**
```bash
pywatch -e .py "python -c 'import compileall; compileall.compile_dir(\".\")' && pytest"
```

**Multi-language project:**
```bash
pywatch -e .rs "cargo test"
```

---

## Comparison

| Tool | Language | Approach | Dependencies |
|---|---|---|---|
| **PyWatch** | Python | `os.stat` polling | None |
| nodemon | Node.js | fs.watch + fallback polling | npm |
| entr | C | inotify (Linux only) | None (but Linux-only) |
| watchdog | Python | inotify/fsevents | platform-specific libs |
| watchexec | Rust |各种 backend | Binary download |

**Why PyWatch over the alternatives?**

- **Zero dependencies** — `pip install` and done
- **Cross-platform** — works on Windows, macOS, Linux identically
- **Python-native** — stays in the Python ecosystem
- **Simple** — one command, sensible defaults, no config file needed

---

## Architecture

```
pywatch/
├── pywatch/
│   ├── __init__.py    # Version info
│   ├── __main__.py    # `python -m pywatch` support
│   ├── cli.py         # Argument parsing, command execution, UI
│   └── watcher.py     # File polling engine with debounce
├── pyproject.toml     # Package metadata and entry point
├── setup.py           # Setuptools shim
├── LICENSE            # MIT
├── .gitignore
└── README.md
```

The **watcher** module handles filesystem scanning. The **cli** module handles user interaction. The two are decoupled — you could import `pywatch.watcher.watch()` into your own tools.

---

## Contributing

Contributions are welcome! Please open an issue or pull request.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

Please ensure your code is tested and runs on Python 3.8+.

---

## License

MIT © 2026 [FreeAutomation-Tech](https://github.com/FreeAutomation-Tech/pywatch)
---
*If you find this useful, please consider giving it a star ⭐ — it helps others discover it too!*

*Thank you for your support! 🙏*

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=FreeAutomationTech&button_colour=FFDD00&font_colour=000000&font=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/FreeAutomationTech)
