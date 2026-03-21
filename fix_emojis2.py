#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Simple direct replacements for remaining ?? issues
replacements = [
    # Fix Poképark in epicNotifications
    ('POK_PARK COME_ANDO AGORA! ??", emoji: "??", type: "EVENTO", threat: "??', 
     'POKÉPARK COMEÇANDO AGORA! 🎪", emoji: "🎪", type: "EVENTO", threat: "⚡'),
    
    # Fix body with ???????
    ('\\n?????????????????????\\n⚡ TIPO:', 
     '\\n🔔🔔🔔🔔🔔🔔🔔🔔🔔\\n⚡ TIPO:'),
    
    # Fix level marker in body
    ('\\n?? Nível: ${msgData.threat}\\n?? Início:',
     '\\n📊 Nível: ${msgData.threat}\\n⏰ Início:'),
    
    # Fix danger levels in remaining ?? instances
    ('"?? Crítico"', '"⚠️ Crítico"'),
    ('"?? EXTREMO"', '"🔥 EXTREMO"'),
    ('"?? ALTO"', '"⚡ ALTO"'),
    ('emoji: "??"', 'emoji: "⚔️"'),
    ('title: "??', 'title: "⚔️'),
    ('" emoji: "??"', '" emoji: "⚔️"'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo corrigido com replacements diretos!")
