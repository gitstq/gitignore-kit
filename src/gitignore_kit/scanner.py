"""技术栈探测：根据项目目录中的特征文件推断应启用的模板。"""

from __future__ import annotations

from pathlib import Path

# (模板名, [特征文件...]) —— 命中任意特征即启用该模板。
# 顺序即写入 .gitignore 的分节顺序：语言/框架在前，构建、IDE、操作系统在后。
_DETECTORS: list[tuple[str, list[str]]] = [
    ("python", ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", ".venv", "Pipfile"]),
    ("node", ["package.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"]),
    ("go", ["go.mod", "go.sum"]),
    ("rust", ["Cargo.toml"]),
    ("java", ["pom.xml", "build.gradle", "build.gradle.kts"]),
    ("dotnet", ["*.csproj", "*.sln", "*.fsproj"]),
    ("cpp", ["CMakeLists.txt", "Makefile", "meson.build", "*.cpp"]),
    ("ruby", ["Gemfile", "*.gemspec", ".ruby-version"]),
    ("php", ["composer.json"]),
    ("swift", ["Podfile", "*.xcodeproj", "Package.swift"]),
    ("android", ["AndroidManifest.xml", "app/build.gradle", "gradle.properties"]),
    ("unity", ["Assets", "ProjectSettings"]),
    ("godot", ["project.godot"]),
    ("latex", ["*.tex"]),
    ("docker", ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]),
    ("terraform", ["*.tf", "*.tfvars"]),
]

# IDE / 操作系统模板：按目录特征或全局启用。
_IDE_DETECTORS: list[tuple[str, list[str]]] = [
    ("jetbrains", [".idea"]),
    ("vscode", [".vscode"]),
]

_OS_TEMPLATES = ["macos", "windows", "linux"]
_BUILD_TEMPLATES = ["build", "vim"]


def _matches(root: Path, marker: str) -> bool:
    """判断特征文件是否存在，支持 * 通配符。"""
    if any(ch in marker for ch in "*?["):
        return any(root.glob(marker))
    return (root / marker).exists()


def scan(root: str | Path) -> list[str]:
    """探测目录并返回推荐的模板名列表（有序、去重）。"""
    root = Path(root).resolve()
    names: list[str] = []
    for name, markers in _DETECTORS:
        if any(_matches(root, m) for m in markers):
            names.append(name)
    for name, markers in _IDE_DETECTORS:
        if any(_matches(root, m) for m in markers):
            names.append(name)
    names.extend(_BUILD_TEMPLATES)
    names.extend(_OS_TEMPLATES)
    # 去重且保持顺序
    seen: set[str] = set()
    ordered: list[str] = []
    for n in names:
        if n not in seen:
            seen.add(n)
            ordered.append(n)
    return ordered
