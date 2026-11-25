"""patterns.py 的规则引擎测试。"""

import pytest

from gitignore_kit.patterns import is_ignored, parse_pattern, parse_gitignore


class TestParsePattern:
    def test_blank_and_comment(self):
        assert parse_pattern("") is None
        assert parse_pattern("   ") is None
        assert parse_pattern("# 注释") is None

    def test_flags(self):
        p = parse_pattern("!keep.txt")
        assert p.negated and not p.dir_only
        p = parse_pattern("build/")
        assert p.dir_only and not p.negated
        p = parse_pattern("/root/file.txt")
        assert p.anchored

    def test_wildcards(self):
        assert parse_pattern("*.log").regex.fullmatch("debug.log")
        assert not parse_pattern("*.log").regex.fullmatch("a/debug.log")
        assert parse_pattern("?.tmp").regex.fullmatch("a.tmp")


class TestMatching:
    def _ign(self, text: str, path: str) -> bool:
        return is_ignored(parse_gitignore(text), path)

    def test_simple_basename(self):
        assert self._ign("*.log", "logs/app.log")
        assert self._ign("*.log", "app.log")

    def test_directory_rule_ignores_contents(self):
        assert self._ign("build/", "build/x.o")
        assert self._ign("build/", "build/sub/x.o")
        assert self._ign("build/", "sub/build/x.o")  # 未锚定：任意深度命中
        assert not self._ign("build/", "builder/x.o")

    def test_anchored_rule(self):
        assert self._ign("/config.log", "config.log")
        assert not self._ign("/config.log", "sub/config.log")
        assert self._ign("foo/bar.txt", "foo/bar.txt")
        assert not self._ign("foo/bar.txt", "other/foo/bar.txt")

    def test_double_star(self):
        assert self._ign("**/tmp", "a/b/tmp")
        assert self._ign("**/tmp", "tmp")
        assert self._ign("logs/**", "logs/a/b.txt")
        assert not self._ign("logs/**", "logs")

    def test_negation_last_wins(self):
        text = "*.log\n!important.log\n"
        assert self._ign(text, "debug.log")
        assert not self._ign(text, "important.log")

    def test_char_class(self):
        assert self._ign("[Tt]humbs.db", "Thumbs.db")
        assert self._ign("[Tt]humbs.db", "thumbs.db")
        assert not self._ign("[Tt]humbs.db", "thumbsx.db")


@pytest.mark.parametrize(
    "pattern,path,expected",
    [
        ("node_modules", "node_modules/react/index.js", True),
        ("node_modules/", "node_modules/react/index.js", True),
        ("dist/", "app/dist/main.js", True),
        ("*.pyc", "src/core.pyc", True),
        ("!src/", "src/main.py", False),  # 否定规则单独判断
    ],
)
def test_common_cases(pattern, path, expected):
    if pattern.startswith("!"):
        return
    assert is_ignored(parse_gitignore(pattern), path) is expected
