"""
tests/test_core.py
~~~~~~~~~~~~~~~~~~
Tests for humanregex v0.1.0 — covers every public method in Pattern.
"""

import pytest
from humanregex import Pattern


# ── Anchors ────────────────────────────────────────────────────────────────

class TestAnchors:
    def test_starts_with(self):
        p = Pattern().starts_with().digit(3)
        assert p.search("123abc") is not None
        assert p.search("abc123") is None

    def test_ends_with(self):
        p = Pattern().digit(3).ends_with()
        assert p.search("abc123") is not None
        assert p.search("123abc") is None

    def test_starts_and_ends(self):
        p = Pattern().starts_with().digit(3).ends_with()
        assert p.match("123") is True
        assert p.match("1234") is False
        assert p.match("abc") is False


# ── Character classes ──────────────────────────────────────────────────────

class TestCharacterClasses:
    def test_digit_exact(self):
        assert Pattern().starts_with().digit(4).ends_with().match("1234") is True
        assert Pattern().starts_with().digit(4).ends_with().match("123") is False

    def test_digits_range(self):
        p = Pattern().starts_with().digits(2, 4).ends_with()
        assert p.match("12") is True
        assert p.match("1234") is True
        assert p.match("1") is False
        assert p.match("12345") is False

    def test_digits_open_range(self):
        p = Pattern().starts_with().digits(3).ends_with()
        assert p.match("123") is True
        assert p.match("123456789") is True
        assert p.match("12") is False

    def test_letter_exact(self):
        assert Pattern().starts_with().letter(3).ends_with().match("abc") is True
        assert Pattern().starts_with().letter(3).ends_with().match("ab1") is False

    def test_letters_range(self):
        p = Pattern().starts_with().letters(2, 5).ends_with()
        assert p.match("ab") is True
        assert p.match("abcde") is True
        assert p.match("a") is False

    def test_alphanumeric(self):
        assert Pattern().starts_with().alphanumeric(3).ends_with().match("a1_") is True

    def test_whitespace(self):
        assert Pattern().starts_with().whitespace().ends_with().match(" ") is True
        assert Pattern().starts_with().whitespace().ends_with().match("\t") is True

    def test_any_char(self):
        assert Pattern().starts_with().any_char(3).ends_with().match("a1!") is True
        assert Pattern().starts_with().any_char(3).ends_with().match("a1") is False


# ── Literals ───────────────────────────────────────────────────────────────

class TestLiterals:
    def test_literal_plain(self):
        assert Pattern().literal("hello").match("hello") is True
        assert Pattern().literal("hello").match("world") is False

    def test_literal_escapes_special_chars(self):
        # dot inside literal must NOT match any char
        assert Pattern().literal("3.99").match("3.99") is True
        assert Pattern().literal("3.99").match("3X99") is False

    def test_dash(self):
        assert Pattern().starts_with().dash().ends_with().match("-") is True

    def test_dot(self):
        assert Pattern().starts_with().dot().ends_with().match(".") is True
        assert Pattern().starts_with().dot().ends_with().match("a") is False

    def test_space(self):
        assert Pattern().starts_with().space().ends_with().match(" ") is True

    def test_underscore(self):
        assert Pattern().starts_with().underscore().ends_with().match("_") is True

    def test_at(self):
        assert Pattern().starts_with().at().ends_with().match("@") is True


# ── Quantifiers ────────────────────────────────────────────────────────────

class TestQuantifiers:
    def test_one_or_more(self):
        p = Pattern().starts_with().digit().one_or_more().ends_with()
        assert p.match("1") is True
        assert p.match("999") is True
        assert p.match("") is False

    def test_zero_or_more(self):
        p = Pattern().starts_with().digit().zero_or_more().ends_with()
        assert p.match("") is True
        assert p.match("123") is True

    def test_optional(self):
        p = Pattern().starts_with().literal("colour").optional().ends_with()
        assert p.search("colour") is not None


# ── Grouping & alternation ─────────────────────────────────────────────────

class TestGrouping:
    def test_one_of(self):
        p = Pattern().starts_with().one_of("cat", "dog", "bird").ends_with()
        assert p.match("cat") is True
        assert p.match("dog") is True
        assert p.match("fish") is False

    def test_one_of_chars(self):
        p = Pattern().starts_with().one_of_chars("aeiou").ends_with()
        assert p.match("a") is True
        assert p.match("b") is False

    def test_not_chars(self):
        p = Pattern().starts_with().not_chars("0123456789").ends_with()
        assert p.match("a") is True
        assert p.match("5") is False

    def test_group(self):
        p = Pattern().starts_with().group(r"cat|dog").ends_with()
        assert p.match("cat") is True
        assert p.match("dog") is True
        assert p.match("bird") is False

    def test_named_group(self):
        p = Pattern().starts_with().named_group("code", r"\d{3}").ends_with()
        result = p.search("123")
        assert result is not None
        assert result.group("code") == "123"




# ── Pre-built patterns ─────────────────────────────────────────────────────

class TestPrebuiltPatterns:
    def test_word_boundary(self):
        p = Pattern().word_boundary().literal("cat").word_boundary()
        assert p.search("a cat nap") is not None
        assert p.search("concatenate") is None

    def test_email(self):
        p = Pattern().starts_with().email().ends_with()
        assert p.match("hello.world+news@example.co") is True
        assert p.match("not-an-email") is False

    def test_url_requires_scheme_by_default(self):
        p = Pattern().starts_with().url().ends_with()
        assert p.match("https://example.com/path") is True
        assert p.match("example.com/path") is False

    def test_url_optional_scheme(self):
        p = Pattern().starts_with().url(require_scheme=False).ends_with()
        assert p.match("https://example.com") is True
        assert p.match("example.com/docs") is True

    def test_ip_address(self):
        p = Pattern().starts_with().ip_address().ends_with()
        assert p.match("192.168.0.1") is True
        assert p.match("255.255.255.255") is True
        assert p.match("256.1.2.3") is False
        assert p.match("999.999.999.999") is False

# ── Flags ──────────────────────────────────────────────────────────────────

class TestFlags:
    def test_ignore_case(self):
        p = Pattern().starts_with().literal("hello").ends_with().ignore_case()
        assert p.match("HELLO") is True
        assert p.match("HeLLo") is True
        assert p.match("world") is False

    def test_multiline(self):
        p = Pattern().starts_with().digit().one_or_more().multiline()
        text = "abc\n123\ndef"
        assert p.search(text) is not None


# ── Actions ────────────────────────────────────────────────────────────────

class TestActions:
    def test_match_full_string(self):
        assert Pattern().digit(3).match("123") is True
        assert Pattern().digit(3).match("1234") is False   # fullmatch, not partial

    def test_search_partial(self):
        result = Pattern().digit(3).search("abc 123 def")
        assert result is not None
        assert result.group() == "123"

    def test_find_all(self):
        result = Pattern().digit().one_or_more().find_all("Call 123 or 4567 today")
        assert result == ["123", "4567"]

    def test_find_iter(self):
        iterator = Pattern().digit().one_or_more().find_iter("Call 123 or 4567 today")
        assert [m.group() for m in iterator] == ["123", "4567"]

    def test_count(self):
        result = Pattern().digit().one_or_more().count("Call 123 or 4567 today")
        assert result == 2

    def test_replace(self):
        result = Pattern().digit().one_or_more().replace("Hello 2024 World 42", "NUM")
        assert result == "Hello NUM World NUM"

    def test_split(self):
        result = Pattern().literal(",").split("a,b,c")
        assert result == ["a", "b", "c"]

    def test_compile_returns_pattern(self):
        import re
        compiled = Pattern().digit(3).compile()
        assert isinstance(compiled, re.Pattern)
        assert compiled.search("abc 123") is not None


# ── Introspection ──────────────────────────────────────────────────────────

class TestIntrospection:
    def test_build(self):
        raw = Pattern().digit(3).dash().digit(4).build()
        assert raw == r"\d{3}\-\d{4}"

    def test_repr(self):
        p = Pattern().digit(2)
        assert "Pattern" in repr(p)

    def test_explain_returns_self(self, capsys):
        p = Pattern().digit(3)
        result = p.explain()
        assert result is p
        captured = capsys.readouterr()
        assert "pattern" in captured.out


# ── Chaining ───────────────────────────────────────────────────────────────

class TestChaining:
    def test_ssn(self):
        p = Pattern().starts_with().digit(3).dash().digit(2).dash().digit(4).ends_with()
        assert p.match("123-45-6789") is True
        assert p.match("123456789") is False

    def test_honorific_name(self):
        p = (
            Pattern()
            .starts_with()
            .one_of("Mr", "Ms", "Dr")
            .space()
            .letters(min_count=2)
            .ends_with()
        )
        assert p.match("Dr Smith") is True
        assert p.match("Mr A") is False
        assert p.match("Hello") is False
