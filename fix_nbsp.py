#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige 'Á\xa0s' (com NBSP) para 'às '
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# O padrão REAL é 'Á' + NBSP (\xa0) + 's'
# Vamos substituir por 'à' + 's' + espaço regular
old_pattern = 'Á\xa0s'  # U+00C1 + U+00A0 + 'ús' 
new_pattern = 'às '      # U+00E0 + 's' + U+0020

count = content.count(old_pattern)
print(f"Encontrados {count} ocorrências de '{repr(old_pattern)}'")

content = content.replace(old_pattern, new_pattern)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Substituído para '{repr(new_pattern)}'")
print("✅ Arquivo corrigido!")
