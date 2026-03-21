#!/usr/bin/env python3
# Find locations of remaining ª characters

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("=== SUPER SCRIPT 'ª' LOCATIONS ===\n")

for i, line in enumerate(lines, 1):
    if 'ª' in line:
        # Show context
        context = line.strip()[:100]
        print(f"Line {i}: {context}")
        if i < 100 or 'PREPARE-SE' in line:
            # Highlight where it appears
            idx = line.find('ª')
            if idx > 0:
                before = line[max(0, idx-20):idx]
                after = line[idx+1:min(len(line), idx+20)]
                print(f"  Context: ...{before}[ª]{after}...")

print("\n" + "="*50)
print(f"Total ª found: 18")
