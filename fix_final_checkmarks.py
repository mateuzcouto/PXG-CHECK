#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix remaining checkmark and encoding corruptions
replacements = {
    '✓Ácone': 'Ícone',
    'experi✓ncia': 'experiência',
    'tamb✓m': 'também',
    'Por✓m': 'Porém',
    'porém': 'porém',  # ensure lowercase
    'encriptados': 'encriptados',  # correct spelling
    's✓o': 'são',
    'sincroniza✓✓o': 'sincronização',
    'di✓rias': 'diárias',
    'telem✓vel': 'telemóvel',
    '✓ blindado': 'é blindado',
    '✓ superior': 'é superior',
    'n✓o': 'não',
    'estratÁ©gias': 'estratégias',
    'AÃ§': 'ação',
    'Á©': 'é',
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
