#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix agressivo: Substitui TODOS os ~ que deveriam ser ? em ternary operators
Usa regex para pegar em template literals também
"""

import re

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Padrão: algo ~ algo : algo
# Isto é um ternary operator que foi corrompido para ~/

# Substituir TODOS os ~ entre dois : (que indicam ternary operator)
# Mas ser cuidadoso para não quebrar URLs com ~
content = re.sub(
    r'([\`\'\"\w\}])\s*~\s*([\'\"\\$])',  # Caractere ou } seguido de ~ e depois ' ou "
    r'\1 ? \2',
    content
)

# Substituir más usos específicas  
fixes = [
    ('isOpen ~ ', 'isOpen ? '),
    ('isGroupComplete ~ ', 'isGroupComplete ?'),
    ('userDoc.exists() ~ ', 'userDoc.exists() ? '),
]

for bad, good in fixes:
    if bad in content:
        count = content.count(bad)
        print(f"✅ Substituindo ({count}x): '{bad}' → '{good}'")
        content = content.replace(bad, good)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Ternary operators corrigidos globalmente!")
