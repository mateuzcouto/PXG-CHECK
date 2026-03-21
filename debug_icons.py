#!/usr/bin/env python3
# Find exact bytes for the corrupted icon patterns

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

# Find key patterns
patterns = [
    b"'Aurora'",
    b"'Omega':",
    b"'Steel'",
    b"volcanic:",
    b"'Sunflora'",
    b'icon:'
]

for pattern in patterns:
    idx = content.find(pattern)
    if idx != -1:
        start = max(0, idx)
        end = min(len(content), idx + 150)
        snippet = content[start:end]
        print(f"Pattern: {pattern}")
        print(f"  Hex: {snippet.hex()}")
        print(f"  Text: {snippet.decode('utf-8', errors='replace')}\n")
