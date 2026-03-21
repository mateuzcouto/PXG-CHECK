#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix remaining checkmark corruptions
replacements = {
    '✓Ácone': 'Ícone',
    'Alternar Visualiza✓✓o': 'Alternar Visualização',
    't✓ticos': 'táticos',
    'conclu✓rem': 'concluírem',
    'conte✓dos': 'conteúdos',
    'Otimiza✓✓o': 'Otimização',
    'CrÁ­tico': 'Crítico',
    'crÁ­ticos': 'críticos',
    '✓til': 'útil',
    'TÁ¡tica': 'Tática',
    'Sobreviv✓ncia': 'Sobrevivência',
    'm✓o': 'mão',
    'm✓ximo': 'máximo',
    'poss✓vel': 'possível',
    'N✓o': 'Não',
    'Experi✓ncia': 'Experiência',
    'est✓tuas': 'estátuas',
    'padr✓es': 'padrões',
    'execuÁ§Á£o': 'execução',
    'Á§Á£o': 'ção',
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
print(f"✅ Total additional fixes applied: {fixed_count}")
