#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Último fix: Corrigir padrões de corrupção restantes
Procura por "ií" que deveria ser outras coisas
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Padrões comuns de corrupção
fixes = [
    ('atualizaííío', 'atualização'),
    ('atualizaíío', 'atualização'),
    ('ationaíío', 'ação'),
    ('açãoíío', 'ação'),
]

replaced = 0
for bad, good in fixes:
    count = content.count(bad)
    if count > 0:
        print(f"✅ Fix ({count}x): '{bad}' → '{good}'")
        content = content.replace(bad, good)
        replaced += count

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total corrigido: {replaced}")
print("✅ Últimas corrupções limpas!")
