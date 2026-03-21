#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reverte os problemas causados pelo clean_utf8.hy
Substitui ~ errado de volta para ? nos ternary operators e object accessors
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Revertemos as coisas erradas
bad_replacements = [
    ('window.ui~.', 'window.ui.'),     # Object accessor errado
    ('document.getElementById(\'orb-search\')~', 'document.getElementById(\'orb-search\')'),  # Method call errado
    ('lines.length > 1 ~ lines', 'lines.length > 1 ? lines'),  # Ternary operator errado
    ('cols[3] ~ cols', 'cols[3] ? cols'),  # Ternary operator errado
    ('exist() ~ ', 'exists() ? '),  # Method call + ternary
    ('\'undefined\' ~ ', '\'undefined\' ? '),  # String comparison + ternary
    ('total > 0 ~ ', 'total > 0 ? '),  # Math comparison + ternary
    ('isGroupComplete ~ ', 'isGroupComplete ? '),  # Boolean + ternary
    (' ~ `', ' ? `'),  # Ternary com template literal
]

for bad, good in bad_replacements:
    if bad in content:
        count = content.count(bad)
        print(f"✅ Revertendo ({count}x): '{bad}' → '{good}'")
        content = content.replace(bad, good)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Arquivo revertido - Ternary operators e accessors restaurados!")
