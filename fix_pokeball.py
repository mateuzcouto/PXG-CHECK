#!/usr/bin/env python3
# Fix the pokeball icon

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0
for i, line in enumerate(lines):
    if 'boss-pokeball-icon' in line and '📱' in line:
        # Replace with red pokéball emoji
        if '📱' in line:
            lines[i] = line.replace('📱', '🔴')
            changes += 1
            print(f"Line {i}: Fixed pokeball icon (📱 → 🔴)")
        
        # Also remove stray characters like ´
        lines[i] = lines[i].replace('´', '')

if changes > 0:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"✅ Updated {changes} lines")
else:
    print("No pokeball icon lines found")
