#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix all remaining checkmark corruptions (comprehensive)
replacements = {
    '✓Ácone': 'Ícone',
    'Pok✓ball': 'Pokéball',
    'Liga✓✓o': 'Ligação',
    'Aten✓✓o': 'Atenção',
    'ap✓s ': 'após ',
    'Cient✓ficos': 'Científicos',
    'T✓tico': 'Tático',
    'T✓ticos': 'Táticos',
    't✓tico': 'tático',
    'exig✓ncia': 'exigência',
    'otimiza✓✓o': 'otimização',
    'Unifica✓✓o': 'Unificação',
    'Remo✓✓o': 'Remoção',
    'Bot✓es': 'Botões',
    'ATUALIZA✓✓O': 'ATUALIZAÇÃO',
    'sanitiza✓✓o': 'sanitização',
    'exp✓e': 'expõe',
    'Pr✓x': 'Próx',
    'Lend✓rios': 'Legendários',
    'cient✓fico': 'científico',
    'V✓rgula': 'Vírgula',
    'v✓rgula': 'vírgula',
    'cabe✓alho': 'cabeçalho',
    's✓ cont✓m': 'só contêm',
    't✓tulos': 'títulos',
    'Din✓mico': 'Dinâmico',
    'POSI✓✓O': 'POSIÇÃO',
    'Cen✓rio': 'Cenário',
    'V✓ ': 'Vá',
    'v✓ ': 'vá ',
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

# Count remaining checkmarks
remaining = text.count('✓')
print(f"\nRemaining checkmarks: {remaining}")
if remaining > 0:
    print("⚠️  Some checkmarks remain (may be intentional like ✓ ENTENDI or copyright symbols)")
