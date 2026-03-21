#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIMPEZA FINAL: Remove BOM e reconstrói o arquivo em UTF-8 puro
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

# Ler como UTF-8, ignorando erros
with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
    content = f.read()

# Fazer substituições globais de acentos corrompidos
fixes = {
    '️Ícone Pokébola': '🔴 Ícone Pokébola',
    'Á s': 'às',
    'Á ': 'ó ',
    'Ã©': 'é',  
    'Ã¡': 'á',
   'Ã§': 'ç',
    'Ã£': 'ã',
    'Ã¢': 'â',
    'Ã©': 'é',
   '¿': '?',
}

for bad, good in fixes.items():
    content = content.replace(bad, good)

# Re-salvar em UTF-8 PURO (sem BOM)
with open(filepath, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("✅ arquivo limpoe reconstruído em UTF-8 puro!")
print("✅ BOM removido, acentos corrigidos!")
