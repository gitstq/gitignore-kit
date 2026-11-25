"""命令行入口（argparse 实现，零第三方依赖）。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, checker, merger, scanner, templates

# ANSI 颜色（无 TTY 时自动禁用）
_NO_COLOR = not sys.stdout.isatty()
if _NO_COLOR:
    RED = GREEN = YELLOW = CYAN = RESET = BOLD = ""
else:
    RED, GREEN, YELLOW, CYAN = "\033[31m", "\033[32m", "\033[33m", "\033[36m"
    RESET, BOLD = "\033[0m", "\033[1m"


def _err(msg: str) -> None:
    print(f"{RED}✗ {msg}{RESET}", file=sys.stderr)


def _ok(msg: str) -> None:
    print(f"{GREEN}✓ {msg}{RESET}")


def cmd_init(args: argparse.Namespace) -> int:
    """init 子命令：探测技术栈并生成/合并 .gitignore。"""
    root = Path(args.path).resolve()
    gi = root / ".gitignore"
    names = args.templates or scanner.scan(root)
    if not names:
        _err("未探测到任何技术栈，也未指定模板。可用 `gikit list` 查看模板。")
        return 1
    if gi.exists() and not args.force:
        existing = gi.read_text(encoding="utf-8")
        merged, added = merger.merge(existing, names)
        if not added:
            _ok(".gitignore 已覆盖全部推荐模板，无需变更。")
            return 0
        gi.write_text(merged, encoding="utf-8")
        _ok(f"已合并写入 {gi}，新增分节: {', '.join(added)}")
    else:
        gi.write_text(merger.render_file(names, note=f"项目: {root.name}"), encoding="utf-8")
        _ok(f"已生成 {gi}（模板: {', '.join(names)}）")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    """add 子命令：向已有 .gitignore 追加模板分节。"""
    root = Path(args.path).resolve()
    gi = root / ".gitignore"
    for t in args.templates:
        if t not in templates.list_templates():
            _err(f"未知模板: {t}（`gikit list` 查看全部）")
            return 1
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    merged, added = merger.merge(existing, args.templates)
    if not added:
        _ok("所需分节均已存在，文件未变更。")
        return 0
    gi.write_text(merged, encoding="utf-8")
    _ok(f"已向 {gi} 追加分节: {', '.join(added)}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    print(f"{BOLD}可用模板（{len(templates.list_templates())} 个）:{RESET}")
    for t in templates.list_templates():
        print(f"  {CYAN}{t:<12}{RESET} {templates.label_of(t)}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    try:
        print(templates.get_template(args.template).rstrip())
        return 0
    except FileNotFoundError:
        _err(f"未知模板: {args.template}（`gikit list` 查看全部）")
        return 1


def cmd_check(args: argparse.Namespace) -> int:
    """check 子命令：报告被跟踪但应被忽略的文件。"""
    root = Path(args.path).resolve()
    if not (root / ".git").exists():
        _err(f"{root} 不是 git 仓库。")
        return 1
    try:
        violations = checker.find_violations(root)
    except checker.NotGitRepoError as e:
        _err(str(e))
        return 1
    if not violations:
        _ok("检查通过：没有已被跟踪却应忽略的文件。")
        return 0
    print(f"{YELLOW}⚠ 发现 {len(violations)} 个违规文件（已跟踪但命中 .gitignore 规则）:{RESET}")
    for f in violations:
        print(f"  - {f}")
    hint = YELLOW + "建议执行: git rm --cached <文件> 以取消跟踪后提交。" + RESET
    print(hint)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gikit",
        description="gitignore-kit —— 智能 .gitignore 生成与校验工具",
    )
    parser.add_argument("--version", action="version", version=f"gitignore-kit v{__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="探测技术栈并生成/合并 .gitignore")
    p.add_argument("-p", "--path", default=".", help="项目目录（默认当前目录）")
    p.add_argument("-t", "--templates", nargs="+", metavar="TPL", help="手动指定模板，跳过自动探测")
    p.add_argument("-f", "--force", action="store_true", help="已有 .gitignore 时强制覆盖")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add", help="向已有 .gitignore 追加模板分节")
    p.add_argument("templates", nargs="+", metavar="TPL", help="要追加的模板名")
    p.add_argument("-p", "--path", default=".", help="项目目录（默认当前目录）")
    p.set_defaults(func=cmd_add)

    sub.add_parser("list", help="列出全部内置模板").set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="查看某个模板内容")
    p.add_argument("template", help="模板名")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("check", help="检查已被跟踪却应忽略的文件")
    p.add_argument("-p", "--path", default=".", help="git 仓库目录（默认当前目录）")
    p.set_defaults(func=cmd_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as e:
        _err(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
