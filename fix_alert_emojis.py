#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix específico para emojis corrompidos no alerta visual
Apenas padrões que sabemos 100% que estão errados
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Padrões específicos que sabemos estar errados na seção de ALERTA VISUAL
emoji_fixes = [
    # Alerta de Boss - emojis corrompidos
    ('âi¸', '🎭'),       # Boss emoji corrompido → use palco/teatro (temático)
    ('â i¸', '🎪'),      # Variante corrompida
    ('â¡', '⚡'),        # Raio
    ('ðª', '👊'),        # Punho
    ('📱ª', '💪'),       # Braço forte
    ('~ ENTENDI', '✓ ENTENDI'),  # Botão errado
]

replaced = 0
for bad, good in emoji_fixes:
    count = content.count(bad)
    if count > 0:
        print(f"✅ Fix emoji ({count}x): '{bad}' → '{good}'")
        content = content.replace(bad, good)
        replaced += count

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total de emojis corrigidos: {replaced}")
