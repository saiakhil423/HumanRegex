# humanregex 🧠

> Write regex using plain English — no more memorizing cryptic syntax.

[![PyPI version](https://img.shields.io/pypi/v/humanregex)](https://pypi.org/project/humanregex/)
[![Python](https://img.shields.io/pypi/pyversions/humanregex)](https://pypi.org/project/humanregex/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quick start

```python
from humanregex import Pattern

# Match a 7-digit phone number
Pattern().digit(3).dash().digit(4).match("123-4567")   # True

# Find all numbers in a string
Pattern().digit().one_or_more().find_all("Call 123 or 4567")  # ['123', '4567']

# Replace numbers
Pattern().digit().one_or_more().replace("Ref 2024-42", "NUM")  # 'Ref NUM-NUM'

# Build a pattern for a name with honorific
(
    Pattern()
    .starts_with()
    .one_of("Mr", "Ms", "Dr")
    .space()
    .letters(min_count=2)
    .ends_with()
    .match("Dr Smith")   # True
)
```

## Installation

```bash
pip install humanregex
```

Or install from source for local development:

```bash
git clone https://github.com/YOUR_USERNAME/humanregex
cd humanregex
pip install -e ".[dev]"
```

## API — v0.2.0

### Anchors
| Method | Regex | Description |
|---|---|---|
| `.starts_with()` | `^` | Anchor to start of string |
| `.ends_with()` | `$` | Anchor to end of string |

### Character Classes
| Method | Regex | Description |
|---|---|---|
| `.digit(n=1)` | `\d{n}` | Exactly n digits |
| `.digits(min, max)` | `\d{min,max}` | Range of digits |
| `.letter(n=1)` | `[a-zA-Z]{n}` | Exactly n letters |
| `.letters(min, max)` | `[a-zA-Z]{min,max}` | Range of letters |
| `.alphanumeric(n=1)` | `\w{n}` | Letters, digits, underscore |
| `.whitespace(n=1)` | `\s{n}` | Whitespace characters |
| `.any_char(n=1)` | `.{n}` | Any character (not newline) |

### Literals
| Method | Matches |
|---|---|
| `.literal("text")` | Exact string (auto-escaped) |
| `.dash()` | `-` |
| `.dot()` | `.` |
| `.space(n=1)` | One or more spaces |
| `.underscore()` | `_` |
| `.at()` | `@` |

### Quantifiers
| Method | Regex | Description |
|---|---|---|
| `.one_or_more()` | `+` | One or more of previous |
| `.zero_or_more()` | `*` | Zero or more of previous |
| `.optional()` | `?` | Previous token is optional |
| `.times(min, max=None)` | `{min,max}` | Repeat previous token a custom number of times |

### Grouping & Alternation
| Method | Description |
|---|---|
| `.one_of("a", "b", "c")` | Match one of the given strings |
| `.one_of_chars("aeiou")` | Match one character from the set |
| `.not_chars("0-9")` | Match any character NOT in the set |
| `.group(pattern)` | Add a capturing group from raw regex text |
| `.named_group(name, pattern)` | Add a named capturing group from raw regex text |
| `.either(*patterns)` | Alternation with raw regex snippets or `Pattern` objects |
| `.raw(pattern)` | Append raw regex text directly |

### Lookarounds
| Method | Description |
|---|---|
| `.lookahead(pattern)` | Assert a pattern appears immediately ahead |
| `.negative_lookahead(pattern)` | Assert a pattern does not appear immediately ahead |
| `.lookbehind(pattern)` | Assert a pattern appears immediately behind |
| `.negative_lookbehind(pattern)` | Assert a pattern does not appear immediately behind |

### Pre-built Patterns
| Method | Description |
|---|---|
| `.word_boundary()` | Add a word boundary (`\b`) |
| `.email()` | Match a practical email pattern |
| `.url(require_scheme=True)` | Match an `http`/`https` URL |
| `.ip_address()` | Match an IPv4 address |
| `.phone_number()` | Match practical North American phone formats |
| `.hex_color()` | Match `#RGB` and `#RRGGBB` hex colors |

### Flags
| Method | Description |
|---|---|
| `.ignore_case()` | Case-insensitive matching |
| `.multiline()` | `^`/`$` match each line boundary |

### Actions
| Method | Returns | Description |
|---|---|---|
| `.match(text)` | `bool` | Full string must match |
| `.search(text)` | `Match \| None` | Find anywhere in string |
| `.find_all(text)` | `list` | All non-overlapping matches |
| `.find_iter(text)` | `iterator` | Iterate over match objects |
| `.count(text)` | `int` | Count non-overlapping matches |
| `.replace(text, repl)` | `str` | Replace all matches |
| `.split(text)` | `list` | Split string by pattern |
| `.compile()` | `re.Pattern` | Compiled regex for reuse |

### Introspection
| Method | Description |
|---|---|
| `.build()` | Return the raw regex string |
| `.explain()` | Print pattern + flags for debugging |

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## Feature ideas to make this project more "featuristic"

- Add ergonomic lookaround helpers for validation without consuming characters.
- Add richer prebuilt patterns for common real-world data (phone numbers, hex colors, IDs, etc.).
- Add an escape-hatch API for advanced users (`raw`) while keeping fluent chain readability.
- Add a generic custom quantifier (`times`) instead of relying only on `+`, `*`, and `?`.
- Improve alternation ergonomics so full `Pattern` blocks can be combined with `either`.

### Implemented in this update

- ✅ `times(min, max=None)`
- ✅ `raw(pattern)`
- ✅ `either(*patterns)` with support for both strings and `Pattern` objects
- ✅ Lookarounds: `lookahead`, `negative_lookahead`, `lookbehind`, `negative_lookbehind`
- ✅ Prebuilt helpers: `phone_number()` and `hex_color()`

## Roadmap

- `v0.3.0` — Additional pre-built patterns (`credit_card()`, `postal_code()`, …)
- `v0.4.0` — Richer group composition helpers
- `v1.0.0` — Stable public API


Pull requests are welcome! Please open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)
