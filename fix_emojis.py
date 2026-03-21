#!/usr/bin/env python3
"""Fix remaining corrupted emojis and text."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'rb') as f:
    data = f.read()

text = data.decode('utf-8')
fixes = 0

# FIX 1: Restore corrupted 3-byte emojis
emoji_map = {
    '\u00e2\u009c\u0085': '\u2705',     # checkmark
    '\u00e2\u008f\u00b0': '\u23f0',     # alarm clock
    '\u00e2\u009b\u0094': '\u26d4',     # no entry
    '\u00e2\u00ac\u0086': '\u2b06',     # up arrow
    '\u00e2\u009c\u008f': '\u270f',     # pencil
    '\u00e2\u0098\u0081': '\u2601',     # cloud
    '\u00e2\u008b\u00ae': '\u22ee',     # vertical ellipsis
    '\u00e2\u0086\u0092': '\u2192',     # right arrow
}

for old_e, new_e in emoji_map.items():
    c = text.count(old_e)
    if c > 0:
        text = text.replace(old_e, new_e)
        fixes += c
        print(f"FIX: -> {new_e} (U+{ord(new_e):04X}) ({c}x)")

# FIX 2: ice emoji
old_ice = '\u2744i\u00b8'
new_ice = '\u2744\ufe0f'
c = text.count(old_ice)
if c > 0:
    text = text.replace(old_ice, new_ice)
    fixes += c
    print(f"FIX: ice emoji ({c}x)")

with open('src/index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print(f"\nTOTAL: {fixes} fixes")
print(f"Remaining ice: {text.count(old_ice)}")
