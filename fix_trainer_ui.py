#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Use simple character replacements
# Fix pokemon caught line
content = content.replace(
    '📌 ${char.fishingLevel || 0} » ?? ${char.pokemonCaught || 0}',
    '📌 Pesca: ${char.fishingLevel || 0} | 🎣 Capturados: ${char.pokemonCaught || 0}'
)

# Also fix other remaining ?? in buttons
content = content.replace(
    'title="Editar Configurações">??</button>',
    'title="Editar Configurações">✏️</button>'
)

# If there's still a ? button for level up
content = content.replace(
    'title="Subir de Nível">?</button>',
    'title="Subir de Nível">⬆️</button>'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Trainer icons fixed!")
