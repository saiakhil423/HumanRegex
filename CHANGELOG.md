# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Pre-built pattern helpers: `word_boundary()`, `email()`, `url(require_scheme=True)`, and `ip_address()`
- Group capture helpers: `group(pattern)` and `named_group(name, pattern)`
- New actions: `find_iter(text)` and `count(text)`
- Tests covering all new helper methods

## [0.1.0] - 2026-02-25

### Added
- `Pattern` class with fluent chainable API
- Anchors: `starts_with()`, `ends_with()`
- Character classes: `digit()`, `digits()`, `letter()`, `letters()`, `alphanumeric()`, `whitespace()`, `any_char()`
- Literals: `literal()`, `dash()`, `dot()`, `space()`, `underscore()`, `at()`
- Quantifiers: `one_or_more()`, `zero_or_more()`, `optional()`
- Grouping: `one_of()`, `one_of_chars()`, `not_chars()`
- Flags: `ignore_case()`, `multiline()`
- Actions: `match()`, `search()`, `find_all()`, `replace()`, `split()`, `compile()`
- Introspection: `build()`, `explain()`
