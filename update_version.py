with open('pyproject.toml', 'r') as f:
    content = f.read()

content = content.replace('version = "0.1.1"', 'version = "0.1.2"')

with open('pyproject.toml', 'w') as f:
    f.write(content)

print('Updated version to 0.1.2')
