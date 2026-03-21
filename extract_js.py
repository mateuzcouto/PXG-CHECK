#!/usr/bin/env python3
"""Extract JS from module script and check for syntax issues."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the module script
match = re.search(r'<script type="module">(.*?)</script>', content, re.DOTALL)
if not match:
    print("ERROR: No module script found!")
    sys.exit(1)

js_code = match.group(1)

# Write to temp file for node --check
with open('_temp_module.mjs', 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"Extracted {len(js_code)} chars of JS module code to _temp_module.mjs")
print("Run: node --check _temp_module.mjs")
