#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix remaining checkmarks
replacements = {
    'j✓ ': 'já ',
    'conclu✓das': 'concluídas',
    'pend✓ncias': 'pendências',
    'Automa✓✓o': 'Automatização',
    'marca✓✓es': 'marcações',
    'interven✓✓es': 'intervenções',
    'l✓quidos': 'líquidos',
    'explora✓✓o': 'exploração',
    '✓reas': 'áreas',
    'Infla✓✓o': 'Inflação',
    'n✓veis': 'níveis',
    'mec✓nicos': 'mecânicos',
    'depend✓ncia': 'dependência',
    'pre✓os': 'preços',
}

fixed_count = 0
for pattern, replacement in replacements.items():
    if pattern in text:
        count = text.count(pattern)
        text = text.replace(pattern, replacement)
        print(f"✅ Fixed '{pattern}' → '{replacement}' ({count} occurrence(s))")
        fixed_count += count

# Save the file
with open("src/index.html", "w", encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ File saved successfully")
print(f"✅ Total fixes applied: {fixed_count}")
