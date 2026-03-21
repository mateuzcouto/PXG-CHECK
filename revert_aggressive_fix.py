#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revert da substituição agressiva de í
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Revert de substituições que foram demais agressivas
# í deveria ser í (não ✓)
content = content.replace('✓', 'í')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Revertido!")
