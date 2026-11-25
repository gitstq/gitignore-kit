"""scanner.py 技术栈探测测试。"""

from pathlib import Path

from gitignore_kit.scanner import scan


def _project(tmp_path: Path, files: dict) -> Path:
    for rel, content in files.items():
        p = tmp_path / rel
        if content is None:
            p.mkdir(parents=True, exist_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
    return tmp_path


def test_python_project(tmp_path):
    root = _project(tmp_path, {"pyproject.toml": "[project]"})
    names = scan(root)
    assert "python" in names
    assert "macos" in names and "windows" in names and "linux" in names
    assert "build" in names


def test_node_project(tmp_path):
    root = _project(tmp_path, {"package.json": "{}"})
    assert "node" in scan(root)


def test_multi_stack_order(tmp_path):
    root = _project(tmp_path, {"package.json": "{}", "Dockerfile": "FROM node"})
    names = scan(root)
    assert names.index("node") < names.index("docker")


def test_empty_project_still_has_os_templates(tmp_path):
    names = scan(tmp_path)
    assert set(["macos", "windows", "linux"]).issubset(set(names))


def test_glob_marker(tmp_path):
    root = _project(tmp_path, {"app.csproj": "<Project/>"})
    assert "dotnet" in scan(root)


def test_deterministic(tmp_path):
    root = _project(tmp_path, {"go.mod": "module x", "Cargo.toml": ""})
    assert scan(root) == scan(root)
