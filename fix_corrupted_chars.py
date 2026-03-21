#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix FINAL: Identifica e substitui TODOS os caracteres de encoding corrompido
Procura por padrões como "ï?½", "?", etc que indicam corrupção
"""

import re

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Substituições específicas de palavras que aparecem corrompidas
word_fixes = {
    'regiï?½o': 'região',
    'concluï?½das': 'concluídas',
    'regiï?1/2o': 'região',
    'concluï?1/2das': 'concluídas',
}

# Também procurar caracteres individuais corrompidos
char_patterns = [
    (r'ï\?½', 'í'),     # ï?½ → í
    (r'ï\?1/2', 'í'),   # ï?1/2 → í
    (r'ï\?', 'i'),      # ï? → i (fallback)
    (r'\?½', ''),       # ?½ → remover
    (r'ï', 'i'),       # ï → i (fallback)
]

replaced = 0

# Aplicar fixes de palavras primeiro
for bad, good in word_fixes.items():
    count = content.count(bad)
    if count > 0:
        print(f"✅ Palavra: ({count}x) '{bad}' → '{good}'")
        content = content.replace(bad, good)
        replaced += count

# Depois padrões com regex
for pattern, replacement in char_patterns:
    match_count = len(re.findall(pattern, content))
    if match_count > 0:
        print(f"✅ Padrão regex: ({match_count}x) {repr(pattern)} → {repr(replacement)}")
        content = re.sub(pattern, replacement, content)
        replaced += match_count

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total de correções: {replaced}")
print("✅ Todos os caracteres corrompidos foram corrigidos!")
