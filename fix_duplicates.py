#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the duplicated body line with regex
# Find the pattern and remove the duplicate part
pattern = r"(const body = `\$\{msgData\.emoji\}[^`]+PREPARE-SE SEMPRE!`;)[^;]*`;"
replacement = r"\1"

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Also fix any remaining ?? Início in the body
content = content.replace("?? Início:", "⏰ Início:").replace("?? Nível:", "📊 Nível:")

# Fix line 2032 - group complete checkbox
content = content.replace("'?? '", "'✅ '")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Duplicação removida e últimos ?? corrigidos!")
