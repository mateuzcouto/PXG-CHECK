#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze the encoding corruption by reading raw bytes."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("src/index.html", "rb") as f:
    raw = f.read()

text = raw.decode('utf-8', errors='replace')
lines = text.split('\n')

# Check key lines for icon byte values
key_lines = [1737, 1757, 1777, 1797, 1813, 1825, 7129, 7133, 7137, 7141, 7145, 7149, 
             7153, 7157, 7161, 7165, 7169, 7173, 7177, 7353, 7357, 7361, 7365, 7369,
             7373, 7377, 7381, 7385, 8705, 8709, 8713, 8717, 8721]

for ln in key_lines:
    if ln <= len(lines):
        line = lines[ln - 1]
        enc = line.encode('utf-8')
        # Extract icon/emoji values
        m = re.search(rb'''(?:icon|emoji):\s*['"]([^'"]+)['"]''', enc)
        if m:
            val = m.group(1)
            hex_str = ' '.join(f'{b:02x}' for b in val)
            print(f"Line {ln}: icon/emoji bytes = [{hex_str}]  text='{val.decode('utf-8', errors='replace')}'")
        
        # Also check for <span> content
        m = re.search(rb'text-base">(.*?)</span>', enc)
        if m:
            val = m.group(1)
            hex_str = ' '.join(f'{b:02x}' for b in val)
            print(f"Line {ln}: span bytes = [{hex_str}]  text='{val.decode('utf-8', errors='replace')}'")
