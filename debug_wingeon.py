#!/usr/bin/env python3
# Debug Wingeon bytes

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

# Find Wingeon
idx = content.find(b'wingeon: { name: "Wingeon"')
if idx != -1:
    snippet = content[idx:idx+200]
    print(f"Hex: {snippet.hex()}")
    print(f"Repr: {repr(snippet)}")
    print(f"Text: {snippet.decode('utf-8', errors='replace')}")
    
    # Find icon pattern
    icon_idx = snippet.find(b'icon:')
    if icon_idx != -1:
        icon_part = snippet[icon_idx:icon_idx+30]
        print(f"\nIcon bytes hex: {icon_part.hex()}")
        print(f"Icon repr: {repr(icon_part)}")
