#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any remaining ?? with 📝 in history buttons, and fix pokemon caught
content = content.replace('>??</button>', '>📝</button>')

# Fix the "Pesca" line if it wasn't done
if '📌 Pesca: ${char.fishingLevel' in content:
    # Already fixed
    pass
else:
    # Need to fix it
    content = content.replace(
        '📌 ${char.fishingLevel || 0} » ?? ${char.pokemonCaught',
        '📌 Pesca: ${char.fishingLevel || 0} | 🎣 Capturados: ${char.pokemonCaught'
    )

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Final ?? fixes applied!")
