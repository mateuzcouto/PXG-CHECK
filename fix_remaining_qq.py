#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining user-visible ?? 
replacements = [
    # Banner icon
    ('pokeball-banner-icon">??</span>', 'pokeball-banner-icon">🔔</span>'),
    
    # Admin labels
    ('text-white mb-3">??', 'text-white mb-3">🔧'),
    ('text-white mb-3">?? G', 'text-white mb-3">🔧 G'),
    
    # Warning and storage
    ("text-yellow-400 mb-2\">?? AVISO:", "text-yellow-400 mb-2\">⚠️ AVISO:"),
    ("text-slate-400 mb-2\">?? Armazen", "text-slate-400 mb-2\">💾 Armazen"),
    
    # Medal rankings (1º, 2º, 3º lugar)
    ('title="1° Lugar">??', 'title="1º Lugar">🥇'),
    ('title="2° Lugar">??', 'title="2º Lugar">🥈'),
    ('title="3° Lugar">??', 'title="3º Lugar">🥉'),
    
    # Character info markers
    ('text-slate-400 uppercase mt-1\">??', 'text-slate-400 uppercase mt-1\">📌'),
    
    # Collapse/expand indicators
    ("'??' : '?'", "'⬆️' : '⬇️'"),
    ("isCollapsed ? '??' : '?'", "isCollapsed ? '⬆️' : '⬇️'"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Últimos ?? corrigidos!")
