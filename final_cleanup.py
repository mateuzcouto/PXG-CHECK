#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix FINAL - FINAL - Últimos 14 erros
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix 1: .[k] → [k] (remover ponto antes de bracket)
content = content.replace('.[k]', '[k]')
content = content.replace('.[cat]', '[cat]')
content = content.replace('.[key]', '[key]')

# Fix 2: Ternary operators finais
content = content.replace('Array.isArray(dados) ~ dados :', 'Array.isArray(dados) ? dados :')
content = content.replace('typeof msg === \'string\' ~ msg :', 'typeof msg === \'string\' ? msg :')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Últimos fixes aplicados!")
