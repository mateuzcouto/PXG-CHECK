#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove lines with Poképark and entire object, then replace
# Find and replace Poké variations and re-create them properly
pattern1 = r"'Pok[^']*':\s*\{\s*title:\s*\"[^\"]*POK[^\"]*AGORA![^\"]*\",\s*emoji:\s*\"[^\"]*\",\s*type:\s*\"EVENTO\",\s*threat:\s*\"[^\"]*ALTO[^\"]*\"\s*\}"
replacement1 = "'Poképark': { title: \"🎪 POKÉPARK COMEÇANDO AGORA! 🎪\", emoji: \"🎪\", type: \"EVENTO\", threat: \"⚡ ALTO\" }"

content = re.sub(pattern1, replacement1, content, flags=re.IGNORECASE | re.DOTALL)

# Also fix in epicBossAlerts
pattern2 = r"'Pok[^']*':\s*\{\s*emoji:\s*\"[^\"]*\",\s*title:\s*\"POK[^\"]*AGORA\",\s*type:\s*\"EVENTO[^\"]*\",\s*typeBadge:\s*\"pokemon-type-event\",\s*threat:\s*\"[^\"]*ALTO[^\"]*\"\s*\}"
replacement2 = "'Poképark': { emoji: \"🎪\", title: \"POKÉPARK COMEÇANDO AGORA\", type: \"EVENTO ESPECIAL\", typeBadge: \"pokemon-type-event\", threat: \"⚡ ALTO\" }"

content = re.sub(pattern2, replacement2, content, flags=re.IGNORECASE | re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Poképark corrigido!")
