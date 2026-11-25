"""gitignore 规则解析与匹配引擎（纯标准库实现）。

支持的语法子集：
- 注释（# 开头）与空行
- 否定规则（! 前缀）
- 目录规则（/ 结尾，仅匹配目录及其内容）
- 根锚定（规则中间含 / 或以 / 开头）
- 通配符 *、?、[...] 与 **
已知限制：不支持字符类的取反转义等冷门语法。
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    """一条编译后的 gitignore 规则。"""

    raw: str          # 原始规则文本
    regex: re.Pattern  # 编译后的正则
    negated: bool      # 是否为否定规则（!）
    dir_only: bool     # 是否仅匹配目录（以 / 结尾）
    anchored: bool     # 是否锚定到仓库根


def _translate(pat: str) -> str:
    """把 gitignore 通配符片段翻译为正则片段。"""
    out: list[str] = []
    i, n = 0, len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            if pat[i : i + 3] == "**/":
                out.append("(?:[^/]+/)*")
                i += 3
            elif pat[i : i + 2] == "**":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            j = pat.find("]", i + 1)
            if j == -1:
                out.append(re.escape(c))
                i += 1
            else:
                out.append("[" + pat[i + 1 : j] + "]")
                i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    return "".join(out)


def parse_pattern(line: str) -> Pattern | None:
    """解析一行规则；空行/注释返回 None。"""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    negated = stripped.startswith("!")
    if negated:
        stripped = stripped[1:]
    dir_only = stripped.endswith("/")
    if dir_only:
        stripped = stripped.rstrip("/")
    if stripped.startswith("./"):
        anchored = True
        stripped = stripped[2:]
    elif stripped.startswith("/"):
        anchored = True
        stripped = stripped[1:]
    else:
        anchored = "/" in stripped
    body = _translate(stripped)
    return Pattern(
        raw=line.strip(),
        regex=re.compile(body),
        negated=negated,
        dir_only=dir_only,
        anchored=anchored,
    )


def _prefixes(path: str) -> list[str]:
    """返回路径的全部祖先目录路径（不含自身）。"""
    parts = path.split("/")
    return ["/".join(parts[:k]) for k in range(1, len(parts))]


def pattern_matches(p: Pattern, path: str) -> bool:
    """判断相对路径 path 是否命中该规则（不考虑否定语义）。"""
    parts = path.split("/")
    if p.dir_only:
        # 目录规则：任一祖先目录命中即视为命中
        if p.anchored:
            return any(p.regex.fullmatch(s) for s in _prefixes(path))
        return any(p.regex.fullmatch(seg) for seg in parts[:-1])
    if p.anchored:
        if p.regex.fullmatch(path):
            return True
        # 未带尾部 / 的锚定规则也可命中同名目录并忽略其内容
        return any(p.regex.fullmatch(s) for s in _prefixes(path))
    # 非锚定：路径任一段命中即命中（目录被忽略时其内容一并忽略）
    return any(p.regex.fullmatch(seg) for seg in parts)


def parse_gitignore(text: str) -> list[Pattern]:
    """把整个 .gitignore 文本解析为有序规则列表。"""
    patterns: list[Pattern] = []
    for line in text.splitlines():
        p = parse_pattern(line)
        if p is not None:
            patterns.append(p)
    return patterns


def is_ignored(patterns: list[Pattern], path: str) -> bool:
    """按 gitignore 语义判断路径是否被忽略（最后一条命中规则生效）。"""
    ignored = False
    for p in patterns:
        if pattern_matches(p, path):
            ignored = not p.negated
    return ignored
