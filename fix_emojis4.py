#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace line by line for better control
for i, line in enumerate(lines):
    # Fix body line with numeric backslashes
    if 'N\u0301vel:' in line or 'N+' in line:
        lines[i] = line.replace('?? N', '📊 N').replace('?? I', '⏰ I')
    if '?? Nível:' in line:
        lines[i] = line.replace('?? Nível:', '📊 Nível:')
    if '?? Início:' in line:
        lines[i] = line.replace('?? Início:', '⏰ Início:')

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Arquivo corrigido com sucesso!")
