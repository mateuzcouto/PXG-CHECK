#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix simples mas eficaz: Substitui TODOS os ` ~ '` e ` ~ "` por ` ? '` e ` ? "`
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Padrões simples mas eficazes
patterns = [
    (' ~ \'', ' ? \''),   #  ~ ' → ? '
    (' ~ "', ' ? "'),      #  ~ " → ? "
    (' ~`', ' ?`'),        #  ~` → ?`
    ('~ \'', '? \''),      # ~ ' → ? '
    ('~ "', '? "'),        # ~ " → ? "
]

replaced_count = 0
for bad, good in patterns:
    count = content.count(bad)
    if count > 0:
        print(f"✅ Substituindo ({count}x): {repr(bad)} → {repr(good)}")
        content = content.replace(bad, good)
        replaced_count += count

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total de substituições: {replaced_count}")
print("✅ Arquivo corrigido!")
