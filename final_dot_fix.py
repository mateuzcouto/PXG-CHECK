#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix FINAL: Substitui TODOS os (~.) incorretos por (.)
Isto é o padrão mais comum de corrupção restante
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Substituir TODOS os ~. por .
count_before = content.count('~.')
content = content.replace('~.', '.')
count_after = content.count('~.')

replaced = count_before - count_after

print(f"✅ Substituindo (~.) → (.)")
print(f"   Encontrados: {count_before}")
print(f"   Após fix: {count_after}")
print(f"   Corrigidos: {replaced}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ ÚLTIMO FIX CONCLUÍDO!")
print("✅ Arquivo corrigido globalmente!")
