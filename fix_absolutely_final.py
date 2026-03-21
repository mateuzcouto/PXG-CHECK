#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Fix absolutely final remaining checkmarks
replacements = {
    '✓Ácone': 'Ícone',
    'n✓vel': 'nível',
    'exibi✓✓o': 'exibição',
}

fixed_count = 0
for pattern, replacement in replacements.items():
    if pattern in text:
        count = text.count(pattern)
        text = text.replace(pattern, replacement)
        print(f"✅ Fixed '{pattern}' → '{replacement}' ({count} occurrence(s))")
        fixed_count += count

# Save the file
with open("src/index.html", "w", encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ File saved successfully")
print(f"✅ Total fixes applied: {fixed_count}")

# Verify no checkmarks remain
if '✓' not in text:
    print("✅ SUCCESS: No checkmarks remaining in file!")
else:
    remaining = text.count('✓')
    print(f"⚠️  Warning: {remaining} checkmarks still remaining")
