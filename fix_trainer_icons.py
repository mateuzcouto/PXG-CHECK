#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replacements for character card UI improvements
replacements = [
    # Level up button - change ? to ⬆️
    ('title="Subir de Nível">?</button>', 'title="Subir de Nível">⬆️</button>'),
    
    # Pokemon caught count - fix ?? to proper icon
    ('📌 ${char.fishingLevel || 0} » ?? ${char.pokemonCaught || 0}', 
     '📌 Pesca: ${char.fishingLevel || 0} | 🎣 Capturados: ${char.pokemonCaught || 0}'),
    
    # Export data button
    ('title="Exportar Dados">??</button>', 'title="Exportar Dados">💾</button>'),
    
    # Edit settings button  
    ('title="Editar Configurações">??</button>', 'title="Editar Configurações">✏️</button>'),
    
    # Finance set button
    ('title="${tStrings.finSet}">??</button>', 'title="${tStrings.finSet}">📊</button>'),
    
    # History button
    ('title="Histórico">??</button>', 'title="Histórico">📝</button>'),
    
    # Done at timestamp emoji
    ("? ${t.doneAt}:", "✅ ${t.doneAt}:"),
    
    # Reset at timestamp emoji
    ("? ${t.resetAt}:", "🔄 ${t.resetAt}:"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Icons de Treinadores corrigidos!")
