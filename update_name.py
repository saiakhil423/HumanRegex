with open('pyproject.toml', 'r') as f:
    content = f.read()

content = content.replace('name = "humanregex"', 'name = "human-regex-lib"')

with open('pyproject.toml', 'w') as f:
    f.write(content)

print('Updated pyproject.toml')
