#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix final remaining checkmark corruption patterns
replacements = {
    'Di✓rias': 'Diárias',
    'Gin✓sios': 'Ginásios',
    'C✓es': 'Cães',
    'SE✓✓O': 'SEÇÃO',
    'at✓ Level': 'até Level',
    'a✓✓o ✓ permanente': 'ação é permanente',
    'poder✓ ser': 'poderá ser',
    'VERS✓O': 'VERSÃO',
    'Atualiza✓✓o': 'Atualização',
    'N✓vel': 'Nível',
    '✓nica': 'única',
    'tem✓tico': 'temático',
    'identifica✓✓o': 'identificação',
    'r✓pida': 'rápida',
    '✓Ácone': 'Ícone',
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
