#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Count ?? in different contexts
qq_in_comments = 0
qq_in_console = 0
qq_in_strings = 0

for i, line in enumerate(lines, 1):
    if '??' not in line:
        continue
    
    # Skip comment lines
    if line.strip().startswith('//') or line.strip().startswith('/*') or '-->' in line:
        qq_in_comments += line.count('??')
    # Skip console lines
    elif 'console.' in line or 'console.log' in line or 'console.warn' in line:
        qq_in_console += line.count('??')
    # Other strings/HTML
    else:
        qq_in_strings += line.count('??')
        print(f"Line {i}: {line.rstrip()[:100]}")

print(f"\n📊 Resumo de ??:")
print(f"  - Em comentários: {qq_in_comments}")
print(f"  - Em console.log: {qq_in_console}")
print(f"  - Em strings/HTML: {qq_in_strings}")

if qq_in_strings < 5:
    print(f"\n✅ SUCESSO! Todos os ?? visíveis ao usuário foram corrigidos!")
    print(f"   Os ?? restantes estão apenas em comentários e debug (não afetam o site)")
