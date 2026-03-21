#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige o encoding UTF-8 de forma inteligente
Lê como UTF-8 com fallback para Latin-1 e re-salva
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

# Tentar ler como UTF-8 com ignore de erros
try:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
except:
    # Se UTF-8 falhar, tenta Latin-1
    with open(filepath, 'r', encoding='latin-1') as f:
        content = f.read()

# Agora corrigir caracteres corrompidos comuns
fixes = {
    'PrÃ³x': 'Próx',
    'à ': 'às ',
    'à': 'à',
    'Ã³': 'ó',
    'Ã': 'Á',
    'Ã©': 'é',
    'Ã¡': 'á',
    'Ã¢': 'â',
    'Ã§': 'ç',
    'Ã£': 'ã',
    'ão': 'ção',
    'ões': 'ções',
    'ão': 'ção',
    '??': '??',
}

for bad, good in fixes.items():
    content = content.replace(bad, good)

# Re-salvar em UTF-8 puro (sem BOM)
with open(filepath, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("✅ Encoding UTF-8 reajustado!")
print("✅ Acentos e caracteres especiais corrigidos!")
