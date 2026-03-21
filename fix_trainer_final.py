#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix lines with trainer UI issues
for i, line in enumerate(lines):
    # Fix level up button
    if 'window.actions.levelUp' in line and 'title=' in line and '>?<' in line:
        lines[i] = line.replace('>?</button>', '>⬆️</button>')
    
    # Fix pokemon caught line
    if 'pokemonCaught' in line and '??' in line:
        # Remove the ?? and replace with proper emoji
        lines[i] = line.replace('📌 ${char.fishingLevel', '📌 Pesca: ${char.fishingLevel')
        lines[i] = lines[i].replace('» ??', '| 🎣 C')
    
    # Fix edit button
    if 'ui.openModal' in line and '${char.id}' in line and '>??<' in line:
        lines[i] = line.replace('>??</button>', '>✏️</button>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Trainer UI fixed!")
