#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Read the file with UTF-8 encoding
with open("src/index.html", "rb") as f:
    content = f.read()

# Remove UTF-8 BOM if present (bytes: EF BB BF)
if content.startswith(b'\xef\xbb\xbf'):
    print("✅ Removing UTF-8 BOM")
    content = content[3:]

# Convert bytes to string
text = content.decode('utf-8', errors='replace')

# Fix checkmark corruptions (✓ replacing various Portuguese letters)
replacements = {
    # Common patterns with double checkmarks (ão, ão endings, ção)
    'Pulsa✓✓o': 'Pulsação',
    'Vibra✓✓o': 'Vibração',
    'Informa✓✓es': 'Informações',
    'ObservaÃ§Ã£es': 'Observações',
    'Observa✓✓es': 'Observações',
    'A✓✓o': 'Ação',
    'NOTIFICA✓✓O': 'NOTIFICAÇÃO',
    'NOTIFICAÇÃO': 'NOTIFICAÇÃO',
    'VIS✓O': 'VISÃO',
    'Dram✓tica': 'Dramática',
    'Pok✓log': 'Pokélog',
    
    # Single checkmark replacements
    'R✓pida': 'Rápida',
    'El✓tricos': 'Elétricos',
    'Energ✓tico': 'Energético',
    'Urg✓ncia': 'Urgência',
    'T✓tulo': 'Título',
    'Bot✓o': 'Botão',
    '✓pico': 'típico',
    '✓cone': 'ícone',
    
    # Encoding corruption patterns (Latin-1 artifacts)
    'GestÁ£o o do': 'Gestão do',
    'AnimaÁ§Á£o': 'Animação',
    'AnimaÃ§Ã£o': 'Animação',
    'i»?<!DOCTYPE': '<!DOCTYPE',  # Remove corrupted BOM character
}

fixed_count = 0
for pattern, replacement in replacements.items():
    if pattern in text:
        count = text.count(pattern)
        text = text.replace(pattern, replacement)
        print(f"✅ Fixed '{pattern}' → '{replacement}' ({count} occurrence(s))")
        fixed_count += count

# Save the file with proper UTF-8 encoding (no BOM)
with open("src/index.html", "w", encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ File saved successfully with UTF-8 encoding (no BOM)")
print(f"✅ Total fixes applied: {fixed_count}")
