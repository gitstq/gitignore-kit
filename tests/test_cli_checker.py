"""CLI 与 checker 端到端测试（含真实 git 仓库）。"""

import subprocess

import pytest

from gitignore_kit import checker
from gitignore_kit.cli import main


def _init_repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.email", "t@t.io"], check=True
    )
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "t"], check=True)
    return tmp_path


class TestChecker:
    def test_violation_found(self, tmp_path):
        _init_repo(tmp_path)
        (tmp_path / ".gitignore").write_text("*.log\n")
        (tmp_path / "debug.log").write_text("x")
        (tmp_path / "keep.txt").write_text("x")
        subprocess.run(
            ["git", "-C", str(tmp_path), "add", "-A"], check=True, capture_output=True
        )
        # 违规场景模拟：文件曾被强制跟踪（或规则后补）
        subprocess.run(
            ["git", "-C", str(tmp_path), "add", "-f", "debug.log"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "commit", "-qm", "init"],
            check=True,
            capture_output=True,
        )
        assert checker.find_violations(tmp_path) == ["debug.log"]

    def test_clean_repo(self, tmp_path):
        _init_repo(tmp_path)
        (tmp_path / ".gitignore").write_text("*.log\n")
        (tmp_path / "main.py").write_text("print(1)")
        subprocess.run(
            ["git", "-C", str(tmp_path), "add", "-A"], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "commit", "-qm", "init"],
            check=True,
            capture_output=True,
        )
        assert checker.find_violations(tmp_path) == []

    def test_no_gitignore(self, tmp_path):
        _init_repo(tmp_path)
        assert checker.find_violations(tmp_path) == []


class TestCli:
    def test_init_generates(self, tmp_path, capsys):
        (tmp_path / "pyproject.toml").write_text("[project]")
        code = main(["init", "-p", str(tmp_path)])
        assert code == 0
        text = (tmp_path / ".gitignore").read_text(encoding="utf-8")
        assert "__pycache__/" in text and ".DS_Store" in text

    def test_init_merge_not_overwrite(self, tmp_path):
        (tmp_path / ".gitignore").write_text("# 我自己的注释\n*.secret\n")
        code = main(["init", "-p", str(tmp_path), "-t", "macos"])
        assert code == 0
        text = (tmp_path / ".gitignore").read_text(encoding="utf-8")
        assert "*.secret" in text and ".DS_Store" in text

    def test_init_force_overwrite(self, tmp_path):
        (tmp_path / ".gitignore").write_text("old-content\n")
        main(["init", "-p", str(tmp_path), "-t", "macos", "-f"])
        text = (tmp_path / ".gitignore").read_text(encoding="utf-8")
        assert "old-content" not in text

    def test_add_dedup(self, tmp_path):
        main(["init", "-p", str(tmp_path), "-t", "macos"])
        code = main(["add", "-p", str(tmp_path), "macos"])
        assert code == 0
        text = (tmp_path / ".gitignore").read_text(encoding="utf-8")
        assert text.count(".DS_Store") == 1

    def test_add_unknown_template(self, tmp_path):
        assert main(["add", "-p", str(tmp_path), "ghost"]) == 1

    def test_list_and_show(self, capsys):
        assert main(["list"]) == 0
        assert "python" in capsys.readouterr().out
        assert main(["show", "python"]) == 0
        assert "__pycache__/" in capsys.readouterr().out

    def test_show_unknown(self):
        assert main(["show", "ghost"]) == 1

    def test_check_clean(self, tmp_path, capsys):
        _init_repo(tmp_path)
        (tmp_path / ".gitignore").write_text("*.log\n")
        (tmp_path / "a.py").write_text("")
        subprocess.run(
            ["git", "-C", str(tmp_path), "add", "-A"], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "commit", "-qm", "init"],
            check=True,
            capture_output=True,
        )
        assert main(["check", "-p", str(tmp_path)]) == 0
        assert "检查通过" in capsys.readouterr().out

    def test_check_violation_exit_code(self, tmp_path):
        _init_repo(tmp_path)
        (tmp_path / ".gitignore").write_text("*.log\n")
        (tmp_path / "bad.log").write_text("")
        subprocess.run(
            ["git", "-C", str(tmp_path), "add", "-A"], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "add", "-f", "bad.log"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "commit", "-qm", "init"],
            check=True,
            capture_output=True,
        )
        assert main(["check", "-p", str(tmp_path)]) == 1

    def test_check_not_git_repo(self, tmp_path):
        assert main(["check", "-p", str(tmp_path)]) == 1
