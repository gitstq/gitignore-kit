<div align="center">

# 🧰 gitignore-kit

**Smart .gitignore generator & validator** — keep every repository's ignore rules correct, complete, and verifiable

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.8%2B-orange) ![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

</div>

## 🎉 Introduction

One of the most annoying details of daily development: a missing or incomplete `.gitignore` lets `node_modules`, `__pycache__`, and build artifacts slip into your repository, polluting history — and cleaning up later means `git rm --cached` gymnastics.

**gitignore-kit** solves three problems with one command:

1. **Auto-detect** your project's tech stack (Python / Node / Go / Rust / Java…) and generate a matching `.gitignore`;
2. **Non-destructive merge**: your existing `.gitignore` is never overwritten — only missing sections are added;
3. **Violation check**: find files that are *already tracked by git yet match ignore rules*, before they cause trouble.

Built purely on the Python standard library with **zero third-party dependencies**. 23 templates ship with the package and work fully offline.

## ✨ Features

- 🚀 **Zero dependencies** — stdlib only, installs in seconds, no audit overhead
- 🔍 **Stack auto-detection** — 23 templates across languages, frameworks, IDEs and OS files, intelligently combined from marker files
- 🧩 **Lossless merging** — appended templates never clobber your hand-written rules; duplicate sections are deduplicated
- 🛡️ **Violation check** — scans tracked files via `git ls-files` and warns the moment an ignore rule is violated
- 📦 **Fully offline** — templates are bundled, no external API calls
- 💻 **Cross-platform** — Linux / macOS / Windows, with automatic terminal color adaptation
- 🧪 **Well tested** — rule engine, scanner, merger and CLI covered end to end

## 🚀 Quick Start

```bash
# Install
pip install gitignore-kit

# Generate .gitignore in your project root
gikit init

# Check whether anything is wrongly tracked
gikit check
```

That's it — two commands, one clean staging area.

## 📖 Usage

### 🔍 Generate

```bash
gikit init          # detect stack in current directory, then generate/merge
gikit init -f       # force-overwrite an existing .gitignore
gikit init -p ./my-project      # target another directory
gikit init -t python docker     # pick templates manually, skip detection
```

### ➕ Add templates

```bash
gikit add latex terraform    # append sections to an existing .gitignore (deduped)
```

### 📋 Manage templates

```bash
gikit list          # list all 23 built-in templates
gikit show python   # print a template's contents
```

### 🛡️ Violation check

```bash
gikit check
```

Example output:

```
⚠ 2 violation(s) found (tracked but matched .gitignore rules):
  - debug.log
  - __pycache__/core.cpython-311.pyc
Suggested fix: git rm --cached <file>, then commit.
```

Exit codes: `0` clean / `1` violations found — drop it straight into CI or a pre-commit hook.

### 🧩 Python API

```python
from gitignore_kit import checker, scanner

stacks = scanner.scan(".")              # ['python', 'build', 'macos', ...]
violations = checker.find_violations(".")  # ['debug.log', ...]
```

## 💡 Design Iteration

**v1.0.0 (current)**
- Core: rule engine supporting `*`, `?`, `**`, `[...]`, negation, directory rules and root anchoring
- 23 built-in templates + marker-file based stack detection
- Five subcommands: `init` / `add` / `list` / `show` / `check`
- Cross-platform CI (Ubuntu / macOS / Windows × Python 3.8 / 3.12)

**Roadmap**
- [ ] `check --fix`: automatically run `git rm --cached` and suggest the commit
- [ ] One-shot pre-commit hook installer
- [ ] Community template contributions with versioning

## 📦 Packaging & Deployment

```bash
# Install from source
git clone https://github.com/gitstq/gitignore-kit.git
cd gitignore-kit
pip install .

# Run tests
pytest tests/ -v

# One-shot release build (sdist + wheel + SHA256 checksums)
bash scripts/build.sh
```

The wheel is a universal build — install directly on Windows / macOS / Linux, no compilation needed.

## 🤝 Contributing

Issues and pull requests are welcome! New templates, rule-engine improvements and tests are all valuable. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

Released under the [MIT License](LICENSE).
