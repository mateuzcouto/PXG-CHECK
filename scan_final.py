#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find ALL remaining unique checkmark-containing words and display context."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# Find all unique checkmark-containing words with context
words = set()
for m in re.finditer(r'(\S*\u2713\S*)', text):
    w = m.group(1)
    if len(w) < 50:
        words.add(w)

print(f"=== REMAINING {len(words)} unique checkmark words ===")
for w in sorted(words):
    print(f"  {w}")

# Also check for 'nÁ£o' pattern
print(f"\n=== nÁ£o count: {text.count('nÁ£o')} ===")
print(f"=== eCrítico count: {text.count('eCrítico')} ===")
print(f"=== esTática count: {text.count('esTática')} ===")

# Check for POKÁPARK, DRAGÁO, COMEÁANDO patterns
for pat in ['POKÁPARK', 'DRAGÁO', 'COMEÁ', 'esTá']:
    c = text.count(pat)
    if c > 0:
        print(f"  '{pat}': {c}")
        
# Check for 📱 followed by garbage
phone_positions = [(m.start(), m.end()) for m in re.finditer('\U0001f4f1', text)]
print(f"\n=== Phone emoji (📱) occurrences: {len(phone_positions)} ===")
for pos_start, pos_end in phone_positions[:20]:
    after = text[pos_end:pos_end+5] if pos_end+5 <= len(text) else text[pos_end:]
    before = text[max(0,pos_start-20):pos_start]
    ctx = text[max(0,pos_start-10):min(len(text),pos_end+10)]
    line_num = text[:pos_start].count('\n') + 1
    print(f"  Line {line_num}: ...{ctx}...")

# Check for âi¸ pattern
print(f"\n=== 'âi¸' count: {text.count('âi¸')} ===")

# Check for remaining ~ that might be corrupted ? 
print(f"\n=== Tilde as ternary check ===")
for m in re.finditer(r"(\?\s*'[^']*')\s*~\s*('[^']*')", text):
    line = text[:m.start()].count('\n') + 1
    print(f"  Line {line}: {m.group()[:60]}...")
