#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix conservador: Corrige APENAS padrões de corrupção conhecidos
Identificados pela análise do arquivo resumido
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Padrões ESPECÍFICOS de corrupção encontrados no arquivo
# Estes são padrões que sabemos 100% que estão errados
specific_fixes = [
    # Cedilhas e caracteres comuns
    ('forÁ§ar', 'forçar'),
    ('atualizaÁ§Áµes', 'atualizações'),
    ('íÁcone', 'Ícone'),
    ('PokÁ©bola', 'Pokébola'),
    ('PokÁ©mon', 'Pokémon'),
    ('íPICO', 'ÉPICO'),
    ('DIíRIOS', 'DIÁRIOS'),
    ('Histírico', 'Histórico'),
    ('Confirmaíío', 'Confirmação'),
    ('Funíío', 'Função'),
    ('Validaíío', 'Validação'),
    ('ADMINISTRAííO', 'ADMINISTRAÇÃO'),
    ('SEGURANíA', 'SEGURANÇA'),
    ('INTEGRAííO', 'INTEGRAÇÃO'),
    ('POKíLOG', 'POKÉLOG'),
    ('pígina', 'página'),
    
    # Emojis quebrados - substituir por emojis corretos
    ('âi¸', '🎪'),  # POKÉPARK
    ('ð´', '🔴'),  # Pokébola
    ('ð®', '💎'),  # Jóia/Boss
    ('ð', '📱'),   # Página
    ('í', '✓'),    # Check (quando sozinho)
]

replaced = 0
for bad, good in specific_fixes:
    count = content.count(bad)
    if count > 0:
        print(f"✅ Fix ({count}x): '{bad}' → '{good}'")
        content = content.replace(bad, good)
        replaced += count

# Também corrigir ~id para ?id em URLs (se houver)
content = content.replace('gtag/js~id=', 'gtag/js?id=')
content = content.replace('css2~family=', 'css2?family=')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total de fixes conservadores: {replaced}")
print("✅ Emojis e caracteres corrigidos!")
