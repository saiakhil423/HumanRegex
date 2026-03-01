import re

with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_text = """## [Unreleased]

### Added
- Pre-built pattern helpers: `word_boundary()`, `email()`, `url(require_scheme=True)`, and `ip_address()`
- Group capture helpers: `group(pattern)` and `named_group(name, pattern)`
- New actions: `find_iter(text)` and `count(text)`
- Tests covering all new helper methods"""

new_text = """## [Unreleased]

---

## [0.1.1] - 2026-02-25

### Added
- Pre-built pattern helpers: `word_boundary()`, `email()`, `url(require_scheme=True)`, and `ip_address()`
- Group capture helpers: `group(pattern)` and `named_group(name, pattern)`
- New actions: `find_iter(text)` and `count(text)`
- Tests covering all new helper methods"""

content = content.replace(old_text, new_text)

with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('CHANGELOG.md updated successfully')
