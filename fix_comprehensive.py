#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix all remaining checkmarks
replacements = {
    'di✓rios,': 'diários,',
    'di✓rios ': 'diários ',
    'Conex✓o': 'Conexão',
    '✓nico': 'único',
    'informa✓✓o': 'informação',
    'Administra✓✓o': 'Administração',
    'an✓ncios': 'anúncios',
    'configura✓✓es': 'configurações',
    'Estat✓sticas': 'Estatísticas',
    '✓ltimas': 'últimas',
    'Pok✓XGames': 'PokéXGames',
    'Fa✓a': 'Faça',
    'poder✓ aced✓-los': 'poderá acessá-los',
    'conclu✓da': 'concluída',
    'desmarc✓-la': 'desmarcá-la',
    'progresso~': 'progresso?',
    'Especializa✓✓o': 'Especialização',
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
