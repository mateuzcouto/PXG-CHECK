#!/usr/bin/env python3
# Debug the exact pattern in the file

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find the line with PREPARE-SE
for i, line in enumerate(lines[3240:3260], start=3240):
    if 'PREPARE-SE' in line:
        print(f"Line {i}: {repr(line)}\n")
        
        # Show the exact bytes and characters
        for j, char in enumerate(line):
            if ord(char) < 127 or char in 'ªâ⚡💪📱':
                print(f"  [{j}] = {repr(char)} (ord: {ord(char)})")
            elif j > 50 and j < 120:  # Focus on the emoji area
                print(f"  [{j}] = {repr(char)} (ord: {ord(char)})")
