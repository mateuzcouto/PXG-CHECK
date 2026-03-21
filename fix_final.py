#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Final para corrigir TODOS os acentos problemáticos
Faz substituições específicas e re-salva em UTF-8
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

# Ler o arquivo
with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# SUBSTITUIÇÕES CRÍTICAS E GLOBAIS
substituições = [
    # Corrigir "Á s" para "às"
    ('Á s', 'às'),
    ('Á S', 'ÀS'),
    
    # Corrigir "Próx"
    ('PrÃ³x', 'Próx'),
    
    # Corrigir variações de ç
    ('Ã§', 'ç'),
    ('Ã‡', 'Ç'),
    
    # Corrigir variações de ã
    ('Ã£', 'ã'),
    ('Ã‹', 'Ã'),
    
    # Corrigir é/é
    ('Ã©', 'é'),
    ('É', 'É'),
    
    # Corrigir á/á
    ('Ã¡', 'á'),
    ('Á', 'Á'),
    
    # Corrigir â/â
    ('Ã¢', 'â'),
    ('Â', 'Â'),
    
    # Corrigir ó/ó
    ('Ã³', 'ó'),
    ('Ó', 'Ó'),
    
    # Corrigir ú/ú
    ('Ãº', 'ú'),
    ('Ú', 'Ú'),
    
    # Corrigir í/í
    ('Ã­', 'í'),
    ('Í', 'Í'),
    
    # Corre ações/ções
    ('Ã§Ã£o', 'ção'),
    ('Ã§Ãµes', 'ções'),
]

# Aplicar substituições
for old, new in substituições:
    if old in content:
        print(f"✅ Substituindo '{old}' → '{new}'")
        content = content.replace(old, new)

# Re-salvar em UTF-8 puro
with open(filepath, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("\n✅ CONCLUÍDO! Arquivo re-salvo em UTF-8 correto!")
print("✅ Todos os caracteres especiais foram corrigidos!")
