#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open("src/index.html", "r", encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find lines with checkmarks
checkmark_lines = []
for i, line in enumerate(lines, 1):
    if '✓' in line:
        count = line.count('✓')
        # Extract a snippet around the checkmark
        if len(line) > 100:
            snippet = line[:120] + "..."
        else:
            snippet = line
        checkmark_lines.append((i, count, snippet))

print(f"Total lines with checkmarks: {len(checkmark_lines)}")
print(f"Total checkmarks: {sum(x[1] for x in checkmark_lines)}")
print(f"\nFirst 30 lines with checkmarks:")
for line_num, count, snippet in checkmark_lines[:30]:
    print(f"Line {line_num}: ({count}x) {snippet}")
