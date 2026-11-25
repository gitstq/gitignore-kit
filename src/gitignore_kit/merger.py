""".gitignore 文件的生成与合并。"""

from __future__ import annotations

import gitignore_kit
from . import templates

_SECTION_MARK = "# ═══"
_BANNER_HEAD = "# ─────────────────────────────────────────────────────"


def render_section(name: str) -> str:
    """渲染单个模板分节（含分节标题）。"""
    return f"{_SECTION_MARK} {templates.label_of(name)} {_SECTION_MARK}\n{templates.get_template(name).rstrip()}"


def render_file(names: list[str], note: str = "") -> str:
    """根据模板名列表渲染完整 .gitignore 文件内容。"""
    banner = "\n".join(
        [
            _BANNER_HEAD,
            "# .gitignore — 由 gitignore-kit 生成",
            f"# 版本: v{gitignore_kit.__version__}" + (f" | {note}" if note else ""),
            _BANNER_HEAD,
        ]
    )
    sections = "\n\n".join(render_section(n) for n in names)
    return banner + "\n\n" + sections + "\n"


def parse_sections(text: str) -> set[str]:
    """解析已有文件中的分节标签集合（基于分节标记行）。"""
    labels: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(_SECTION_MARK) and stripped.endswith(_SECTION_MARK):
            inner = stripped[len(_SECTION_MARK) : -len(_SECTION_MARK)].strip()
            if inner:
                labels.add(inner)
    return labels


def merge(existing: str, names: list[str]) -> tuple[str, list[str]]:
    """把缺失的模板分节追加到已有内容末尾。

    返回 (新文件内容, 实际新增的模板名列表)。已存在的分节不重复写入。
    """
    labels = parse_sections(existing)
    wanted = {n: templates.label_of(n) for n in names}
    missing = [n for n in names if wanted[n] not in labels]
    if not missing:
        return existing, []
    additions = "\n\n".join(render_section(n) for n in missing)
    body = existing.rstrip("\n") + "\n\n" + additions + "\n"
    return body, missing
