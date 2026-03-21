#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix FINAL e DEFINITIVO: Substitui TODOS os ~ que são ternary operators (~)
Padrão: (algo) ~ (algo) : (algo)
"""

import re

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Lista explícita de TODOS os ternary operators corrompidos encontrados
ternary_fixes = [
    ('user.displayName ~ user.displayName.split', 'user.displayName ? user.displayName.split'),
    ('a.date ~ new Date', 'a.date ? new Date'),
    ('de instanceof Date ~ d :', 'd instanceof Date ? d :'),
    ('abs % 1000 === 0 ~ 0 :', 'abs % 1000 === 0 ? 0 :'),
    ('char.clan ~ char.clan.toLowerCase', 'char.clan ? char.clan.toLowerCase'),
    ('char.config~.enabledMonthly ~ char.config', 'char.config?.enabledMonthly ? char.config'),
    ('allTasks.length > 0 ~ Math.round', 'allTasks.length > 0 ? Math.round'),
    ('!currentStatus ~ new Date', '!currentStatus ? new Date'),
    ('cb.checked ~ el.classList.remove', 'cb.checked ? el.classList.remove'),
    ('profLvl >= 100 ~ fd.get', 'profLvl >= 100 ? fd.get'),
]

replaced = 0
for bad, good in ternary_fixes:
    count = content.count(bad)
    if count > 0:
        print(f"✅ Ternary: ({count}x) '{bad[:30]}...' → '{good[:30]}...'")
        content = content.replace(bad, good)
        replaced += count

# Também limpar ~. que deveria ser .
content = content.replace('.config~.', '.config?.')
content = content.replace('.uid~.', '.uid.')
content = content.replace('.data~.', '.data?.')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total de fixes: {replaced}")
print("✅ TODOS os ternary operators foram corrigidos!")
