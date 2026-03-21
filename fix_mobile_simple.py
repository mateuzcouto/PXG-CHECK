#!/usr/bin/env python3
# Try to find and fix using regex with error handling

import re

file_path = "src/index.html"

# Read as text
with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find lines with PREPARE-SE
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'PREPARE-SE SEMPRE' in line and '>' in line:
        print(f"Line {i}: {repr(line)}\n")
        
        # Check if it contains problematic chars
        if 'ª' in line in line:
            new_line = line.replace('ª', '')  # Remove ª
            print(f"Removing ª from line {i}")
            lines[i] = new_line
        
        # Also check for stray bytes
        # Replace 📱 with 💪 in this line specifically if it has corrupted
        if '📱' in line and ' PREPARE' in line:
            # This line needs fixing
            new_line = line.replace('📱', '💪', 1)  # Replace only the first emoji instance
            print(f"Replacing 📱 with 💪 in line {i}")
            lines[i] = new_line

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("✅ File updated")
