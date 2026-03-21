#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix duplicated line
content = content.replace(
    "⏰ Início: 5 minutos\\n\\n💪 PREPARE-SE SEMPRE!\";`",
    "⏰ Início: 5 minutos\\n\\n💪 PREPARE-SE SEMPRE!\";"
)

# Fix admin panel ?? icons  
replacements = [
    ("'?? Bug'", "'🐛 Bug'"),
    ("'?? SuGestão o'", "'💡 Sugestão'"),
    ("?? Personagens", "👥 Personagens"),
    ("?? Novo An", "📢 Novo An"),
    ("?? ${u.charCount}", "👤 ${u.charCount}"),
    ("?? Gerenciar Conteúdo", "🔧 Gerenciar Conteúdo"),
    ("?? Bosses Dispon", "⚔️ Bosses Dispon"),
    ("?? Dica:", "💡 Dica:"),
    ("?? Modo Manuten", "🔧 Modo Manuten"),
    ("?? Desabilitar Feedback", "⛔ Desabilitar Feedback"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Admin panel corrigido!")
