#!/usr/bin/env python3
# Remove the remaining ª character

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Simply remove all ª characters (they shouldn't exist in properly formed text)
# But be careful - check context first
lines = content.split('\n')
changes = 0
for i, line in enumerate(lines):
    if 'PREPARE-SE' in line and 'ª' in line:
        old_line = line
        new_line = line.replace('ª', '')  # Remove all ª
        if old_line != new_line:
            lines[i] = new_line
            changes += 1
            print(f"Line {i}: Removed ª")

if changes > 0:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ Removed {changes} instances of ª")
else:
    print("No ª characters found in PREPARE-SE lines")
