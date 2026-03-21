#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Última tentativa: Remove bytes corrompidos de forma agressiva
e substitui com acentos corretos
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

# Ler como binary first para ver o que realmente está lá
with open(filepath, 'rb') as f:
    raw_bytes = f.read()

# Decodificar com fallback
try:
    content = raw_bytes.decode('utf-8')
except:
    content = raw_bytes.decode('utf-8', errors='replace')

# Mapa de TODOS os caracteres corrompidos conhecidos
fixes = {
    # Caracteres individuais corrompidos
    '\ud883': '',
    '\ufffd': '',
    '\u00c3': 'Ã',
    '\u00a9': 'é',
    '\u00e9': 'é',
    
    # Sequências comuns
    'Á s': 'às',
    'Á¡': 'á',
    'Á©': 'é',
    'Á³': 'ó',
    'Á¢': 'â',
    'Á§': 'ç',
    'Á£': 'ã',
}

for bad_char, good_char in fixes.items():
    content = content.replace(bad_char, good_char)

# Lista de palavras problemáticas e suas correções
word_fixes = {
    'Próx': 'Próx',      # Verificar se está correto
    'pokremon': 'pokémon',
    'pokepark': 'poképark',
    'Pokepark': 'Poképark',
}

# Aplicar mais substituições se necessário usando regex-like patterns
import re

# Corrigir padrões: espaço + letra maiúscula + 's' que poderia ser 'às'
content = re.sub(r'\s+[Á][\s]s\s+', ' às ', content)
content = re.sub(r'\s+[Á]\s+s\s+', ' às ', content)

# Re-salvar
with open(filepath, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("✅ SCRIPT FINAL: Caracteres corrompidos removidos!")
print("✅ Arquivo limpo e re-salvo em UTF-8!")
