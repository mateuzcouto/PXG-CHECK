#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Final ?? replacements
content = content.replace('\\n?? Nível:', '\\n📊 Nível:')
content = content.replace('\\n?? Início:', '\\n⏰ Início:')
content = content.replace('AGORA! ??"', 'AGORA! 🎪"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo final corrigido!")
