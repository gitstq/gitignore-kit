"""merger.py 与 templates.py 测试。"""

import pytest

from gitignore_kit import merger, templates


class TestTemplates:
    def test_list_contains_core(self):
        names = templates.list_templates()
        for t in ["python", "node", "go", "rust", "macos", "windows", "linux"]:
            assert t in names

    def test_get_template(self):
        assert "__pycache__/" in templates.get_template("python")

    def test_get_template_missing(self):
        with pytest.raises(FileNotFoundError):
            templates.get_template("no-such-template")

    def test_label(self):
        assert templates.label_of("node") == "Node.js"


class TestRenderFile:
    def test_render_contains_sections(self):
        text = merger.render_file(["python", "macos"])
        assert "# ═══ Python # ═══" in text
        assert "# ═══ macOS # ═══" in text
        assert "__pycache__/" in text

    def test_sections_parseable(self):
        text = merger.render_file(["python", "macos"])
        assert merger.parse_sections(text) == {"Python", "macOS"}


class TestMerge:
    def test_merge_appends_missing(self):
        existing = merger.render_file(["python"])
        merged, added = merger.merge(existing, ["python", "node"])
        assert added == ["node"]
        assert "# ═══ Node.js # ═══" in merged
        # 原 Python 分节保留一份
        assert merged.count("# ═══ Python # ═══") == 1

    def test_merge_no_duplicate(self):
        existing = merger.render_file(["python", "node"])
        merged, added = merger.merge(existing, ["node"])
        assert added == []
        assert merged == existing

    def test_merge_empty_existing(self):
        merged, added = merger.merge("", ["macos"])
        assert added == ["macos"]
        assert ".DS_Store" in merged
