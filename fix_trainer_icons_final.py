#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Simple direct replacements
replacements = {
    '📌 Pesca: ${char.fishingLevel || 0} » ?? ${char.pokemonCaught || 0}': 
    '📌 Pesca: ${char.fishingLevel || 0} | 🎣 Capturados: ${char.pokemonCaught || 0}',
    
    'title="Hist">??</button>':
    'title="Histórico">📝</button>',
    
    'title="Editar Configura">??</button>':
    'title="Editar Configurações">✏️</button>',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Trainer icons final fixes applied!")
