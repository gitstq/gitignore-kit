"""违规检查：找出已被 git 跟踪、但按 .gitignore 规则本应忽略的文件。"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .patterns import is_ignored, parse_gitignore


class NotGitRepoError(RuntimeError):
    """当前目录不是 git 仓库。"""


def _run_git(root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise NotGitRepoError(proc.stderr.strip() or "无法执行 git 命令")
    return proc.stdout


def tracked_files(root: str | Path) -> list[str]:
    """列出仓库中全部已跟踪文件（相对路径）。"""
    root = Path(root).resolve()
    out = _run_git(root, ["ls-files"])
    return [line for line in out.splitlines() if line.strip()]


def find_violations(root: str | Path) -> list[str]:
    """返回已被跟踪却命中忽略规则的文件列表（按路径排序）。

    若仓库没有 .gitignore，返回空列表。
    """
    root = Path(root).resolve()
    gi = root / ".gitignore"
    if not gi.exists():
        return []
    patterns = parse_gitignore(gi.read_text(encoding="utf-8"))
    if not patterns:
        return []
    violations = [
        f for f in tracked_files(root) if f != ".gitignore" and is_ignored(patterns, f)
    ]
    return sorted(violations)
