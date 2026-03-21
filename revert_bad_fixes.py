#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revert dos danos causados pelo script anterior
Corrige substituições erradas que corromperam o arquivo
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Revert das substituições erradas
# Padrão: a vírgula foi substituída por í
bad_replacements = [
    ('Pokípark', 'Poképark'),
    ('Estimulaíío', 'Estimulação'),
    ('pulsaííes', 'pulsações'),
    ('íudio', 'áudio'),
    ('dinímico', 'dinâmico'),
    ('iniciaíío', 'iniciação'),
    ('atualizaíío', 'atualização'),
    ('Horírio', 'Horário'),
    ('Usuírios', 'Usuários'),
    ('Conteído', 'Conteúdo'),
    ('Configuraííes', 'Configurações'),
    ('Aníncio', 'Anúncio'),
    ('Anínimo', 'Anônimo'),
    ('Gerenciar Conteído', 'Gerenciar Conteúdo'),
]

replaced = 0
for bad, good in bad_replacements:
    count = content.count(bad)
    if count > 0:
        print(f"✅ Revert ({count}x): '{bad}' → '{good}'")
        content = content.replace(bad, good)
        replaced += count

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total revertido: {replaced}")
print("✅ Arquivo restaurado!")
