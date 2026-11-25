"""内置模板管理：模板随包分发，完全离线可用。"""

from __future__ import annotations

from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent / "data" / "templates"

# 模板名 -> 展示标签（用于生成的文件中的分节标题）
LABELS: dict[str, str] = {
    "python": "Python",
    "node": "Node.js",
    "go": "Go",
    "rust": "Rust",
    "java": "Java",
    "dotnet": ".NET",
    "cpp": "C / C++",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift / iOS",
    "android": "Android",
    "unity": "Unity",
    "godot": "Godot",
    "latex": "LaTeX",
    "docker": "Docker",
    "terraform": "Terraform",
    "jetbrains": "JetBrains IDE",
    "vscode": "VS Code",
    "vim": "Vim / Emacs",
    "macos": "macOS",
    "windows": "Windows",
    "linux": "Linux",
    "build": "Build Artifacts",
}


def list_templates() -> list[str]:
    """返回全部可用模板名（按字母排序）。"""
    return sorted(p.stem for p in _DATA_DIR.glob("*.gitignore"))


def get_template(name: str) -> str:
    """读取指定模板内容；不存在时抛出 FileNotFoundError。"""
    path = _DATA_DIR / f"{name}.gitignore"
    if not path.exists():
        raise FileNotFoundError(f"模板不存在: {name}")
    return path.read_text(encoding="utf-8")


def label_of(name: str) -> str:
    """取模板的展示标签，未知模板回退为原名。"""
    return LABELS.get(name, name)
