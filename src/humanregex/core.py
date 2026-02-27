"""
humanregex.core
~~~~~~~~~~~~~~~
The Pattern class — the single public API of humanregex.

Every method appends to an internal regex string and returns `self`,
so calls can be chained:

    Pattern().starts_with().digit(3).dash().digit(4).ends_with()

New methods are easy to add:
  1. def your_method(self):
  2.     self._pattern += "<whatever regex>"
  3.     return self
"""

import re


class Pattern:
    """
    A chainable, human-friendly regex builder.

    Usage::

        from humanregex import Pattern

        p = Pattern().digit(3).dash().digit(4)
        p.match("123-4567")   # True
        p.build()             # '\\d{3}\\-\\d{4}'
    """

    def __init__(self):
        self._pattern: str = ""
        self._flags: int = 0

    # ------------------------------------------------------------------
    # Anchors
    # ------------------------------------------------------------------

    def starts_with(self) -> "Pattern":
        """Anchor to the start of the string (^)."""
        self._pattern += "^"
        return self

    def ends_with(self) -> "Pattern":
        """Anchor to the end of the string ($)."""
        self._pattern += "$"
        return self

    # ------------------------------------------------------------------
    # Character classes
    # ------------------------------------------------------------------

    def digit(self, count: int = 1) -> "Pattern":
        """Match exactly *count* digit(s) [0-9]."""
        self._pattern += r"\d" + self._exact(count)
        return self

    def digits(self, min_count: int = 1, max_count: int = None) -> "Pattern":
        """Match between *min_count* and *max_count* digits."""
        self._pattern += r"\d" + self._between(min_count, max_count)
        return self

    def letter(self, count: int = 1) -> "Pattern":
        """Match exactly *count* letter(s) [a-zA-Z]."""
        self._pattern += "[a-zA-Z]" + self._exact(count)
        return self

    def letters(self, min_count: int = 1, max_count: int = None) -> "Pattern":
        """Match between *min_count* and *max_count* letters."""
        self._pattern += "[a-zA-Z]" + self._between(min_count, max_count)
        return self

    def alphanumeric(self, count: int = 1) -> "Pattern":
        """Match exactly *count* alphanumeric character(s) [a-zA-Z0-9_]."""
        self._pattern += r"\w" + self._exact(count)
        return self

    def whitespace(self, count: int = 1) -> "Pattern":
        """Match exactly *count* whitespace character(s)."""
        self._pattern += r"\s" + self._exact(count)
        return self

    def any_char(self, count: int = 1) -> "Pattern":
        """Match any character except newline."""
        self._pattern += "." + self._exact(count)
        return self

    # ------------------------------------------------------------------
    # Literals
    # ------------------------------------------------------------------

    def literal(self, text: str) -> "Pattern":
        """Match an exact string (special chars are auto-escaped)."""
        self._pattern += re.escape(text)
        return self

    def dash(self) -> "Pattern":
        """Match a literal hyphen/dash (-)."""
        self._pattern += r"\-"
        return self

    def dot(self) -> "Pattern":
        """Match a literal dot (.)."""
        self._pattern += r"\."
        return self

    def space(self, count: int = 1) -> "Pattern":
        """Match exactly *count* literal space(s)."""
        self._pattern += " " + self._exact(count)
        return self

    def underscore(self) -> "Pattern":
        """Match a literal underscore (_)."""
        self._pattern += "_"
        return self

    def at(self) -> "Pattern":
        """Match a literal at-sign (@)."""
        self._pattern += "@"
        return self

    # ------------------------------------------------------------------
    # Quantifiers (applied to the previous token)
    # ------------------------------------------------------------------

    def one_or_more(self) -> "Pattern":
        """One or more of the previous token (+)."""
        self._pattern += "+"
        return self

    def zero_or_more(self) -> "Pattern":
        """Zero or more of the previous token (*)."""
        self._pattern += "*"
        return self

    def optional(self) -> "Pattern":
        """Make the previous token optional (?)."""
        self._pattern += "?"
        return self

    # ------------------------------------------------------------------
    # Grouping & alternation
    # ------------------------------------------------------------------

    def one_of(self, *options: str) -> "Pattern":
        """Match one of several literal strings  e.g. one_of('cat','dog')."""
        escaped = [re.escape(o) for o in options]
        self._pattern += "(?:" + "|".join(escaped) + ")"
        return self

    def one_of_chars(self, chars: str) -> "Pattern":
        """Match any single character from *chars*  e.g. one_of_chars('aeiou')."""
        self._pattern += f"[{re.escape(chars)}]"
        return self

    def not_chars(self, chars: str) -> "Pattern":
        """Match any character NOT in *chars*."""
        self._pattern += f"[^{re.escape(chars)}]"
        return self

    def group(self, pattern: str) -> "Pattern":
        """Match a capturing group from a raw regex *pattern*."""
        self._pattern += f"({pattern})"
        return self

    def named_group(self, name: str, pattern: str) -> "Pattern":
        """Match a named capturing group from a raw regex *pattern*."""
        self._pattern += f"(?P<{name}>{pattern})"
        return self

    # ------------------------------------------------------------------
    # Pre-built patterns
    # ------------------------------------------------------------------

    def word_boundary(self) -> "Pattern":
        """Match a word boundary (\b)."""
        self._pattern += r"\b"
        return self

    def email(self) -> "Pattern":
        """Match a practical email pattern (not full RFC validation)."""
        self._pattern += r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
        return self

    def url(self, require_scheme: bool = True) -> "Pattern":
        """Match an http/https URL with optional scheme requirement."""
        scheme = r"https?://" if require_scheme else r"(?:https?://)?"
        self._pattern += scheme + r"[A-Za-z0-9.-]+(?:/[\w\-./?%&=+#]*)?"
        return self

    def ip_address(self) -> "Pattern":
        """Match an IPv4 address in dotted decimal notation."""
        octet = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        self._pattern += rf"(?:{octet}\.){{3}}{octet}"
        return self

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def ignore_case(self) -> "Pattern":
        """Make the whole pattern case-insensitive."""
        self._flags |= re.IGNORECASE
        return self

    def multiline(self) -> "Pattern":
        """Make ^ and $ match start/end of each line instead of the whole string."""
        self._flags |= re.MULTILINE
        return self

    # ------------------------------------------------------------------
    # Actions  (these terminate the chain and do something useful)
    # ------------------------------------------------------------------

    def match(self, text: str) -> bool:
        """Return True if the pattern matches the *entire* string."""
        return bool(re.fullmatch(self._pattern, text, self._flags))

    def search(self, text: str):
        """Return the first Match found anywhere in *text*, or None."""
        return re.search(self._pattern, text, self._flags)

    def find_all(self, text: str) -> list:
        """Return a list of every non-overlapping match in *text*."""
        return re.findall(self._pattern, text, self._flags)

    def find_iter(self, text: str):
        """Return an iterator over non-overlapping Match objects in *text*."""
        return re.finditer(self._pattern, text, self._flags)

    def count(self, text: str) -> int:
        """Return how many non-overlapping matches are found in *text*."""
        return len(self.find_all(text))

    def replace(self, text: str, replacement: str) -> str:
        """Replace every match in *text* with *replacement*."""
        return re.sub(self._pattern, replacement, text, flags=self._flags)

    def split(self, text: str) -> list:
        """Split *text* at every match of this pattern."""
        return re.split(self._pattern, text, flags=self._flags)

    def compile(self) -> re.Pattern:
        """Return a compiled :class:`re.Pattern` object for repeated use."""
        return re.compile(self._pattern, self._flags)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def build(self) -> str:
        """Return the raw regex string that has been built so far."""
        return self._pattern

    def explain(self) -> "Pattern":
        """Print the current raw pattern and flags (handy for debugging)."""
        print(f"pattern : {self._pattern!r}")
        print(f"flags   : {self._flags}")
        return self

    def __repr__(self) -> str:
        return f"Pattern({self._pattern!r})"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _exact(self, count: int) -> str:
        """Return a regex quantifier for exactly *count* repetitions."""
        return "" if count == 1 else f"{{{count}}}"

    def _between(self, min_count: int, max_count) -> str:
        """Return a regex quantifier for a range of repetitions."""
        if max_count is None:
            return f"{{{min_count},}}"
        return f"{{{min_count},{max_count}}}"
