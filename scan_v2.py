#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan index.html for all corruption patterns.
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()
    lines = text.split('\n')

# SCAN 1: find all unique words containing checkmark
print("=" * 70)
print("SCAN 1: Words containing checkmark")
print("=" * 70)
checkmark_words = set()
for i, line in enumerate(lines, 1):
    for m in re.finditer(r'\S*\u2713\S*', line):
        word = m.group()
        if len(word) < 40:
            checkmark_words.add(word)
for w in sorted(checkmark_words):
    print(f"  {w}")
print(f"\nTotal unique checkmark words: {len(checkmark_words)}")

# SCAN 2: Latin-1 double encoding patterns
print("\n" + "=" * 70)
print("SCAN 2: Latin-1 double-encoding patterns")
print("=" * 70)
latin_patterns = [
    ('n\u00c1\u00a3o', 'nao/nao'), 
]
for pat, desc in latin_patterns:
    c = text.count(pat)
    if c > 0:
        print(f"  '{pat}' ({desc}): {c}")

# SCAN 3: Icon/emoji in data structures
print("\n" + "=" * 70)
print("SCAN 3: Icon/emoji definitions")
print("=" * 70)
for i, line in enumerate(lines, 1):
    if re.search(r"icon:\s*['\"]", line) or re.search(r"emoji:\s*['\"]", line):
        print(f"  Line {i}: {line.strip()[:120]}")

# SCAN 4: Sidebar nav buttons
print("\n" + "=" * 70)
print("SCAN 4: Sidebar nav button content")
print("=" * 70)
in_nav = False
for i, line in enumerate(lines, 1):
    if 'switchTab' in line:
        in_nav = True
    if in_nav:
        stripped = line.strip()
        if stripped:
            print(f"  Line {i}: {stripped[:140]}")
        if '</button>' in line:
            in_nav = False
            print()

# SCAN 5: 📱 emoji (often corrupted)
print("\n" + "=" * 70)
print("SCAN 5: Mobile phone emoji (often corruption marker)")
print("=" * 70)
phone_count = text.count('\U0001f4f1')
print(f"  Phone emoji count: {phone_count}")
for i, line in enumerate(lines, 1):
    if '\U0001f4f1' in line:
        idx = line.index('\U0001f4f1')
        start = max(0, idx - 10)
        end = min(len(line), idx + 15)
        ctx = line[start:end] 
        print(f"  Line {i}: ...{ctx}...")

# SCAN 6: eCritico pattern
print("\n" + "=" * 70)
print("SCAN 6: eCritico corruption")
print("=" * 70)
for i, line in enumerate(lines, 1):
    if 'eCr' in line and 'tico' in line:
        for m in re.finditer(r'eCr.{0,5}tico', line):
            start = max(0, m.start() - 30)
            end = min(len(line), m.end() + 10)
            print(f"  Line {i}: ...{line[start:end].strip()}...")

# SCAN 7: Tilde as possible ternary replacement
print("\n" + "=" * 70)
print("SCAN 7: Suspicious tildes in code")  
print("=" * 70)
tilde_in_code = 0
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*') or stripped.startswith('<!--'):
        continue
    # Find ~ not in strings or comments
    if '~' in line and '<script' not in line:
        # Check for ternary-like contexts
        for m in re.finditer(r'(\w)\s*~\s*(\w)', line):
            ctx_start = max(0, m.start() - 15)
            ctx_end = min(len(line), m.end() + 15)
            tilde_in_code += 1
            if tilde_in_code <= 15:
                print(f"  Line {i}: ...{line[ctx_start:ctx_end].strip()}...")

if tilde_in_code > 15:
    print(f"  ... and {tilde_in_code - 15} more")
print(f"  Total: {tilde_in_code}")

# SCAN 8: getWorldColor
print("\n" + "=" * 70)
print("SCAN 8: getWorldColor data")
print("=" * 70)
in_world = False
for i, line in enumerate(lines, 1):
    if 'getWorldColor' in line or 'worldColor' in line.lower():
        in_world = True
    if in_world:
        print(f"  Line {i}: {line.strip()[:120]}")
        if '}' in line and 'return' not in line and 'function' not in line:
            # Check if block is ending
            if line.strip() == '}' or line.strip() == '};':
                in_world = False
    if i > 10000:
        break

# SCAN 9: clanData
print("\n" + "=" * 70)
print("SCAN 9: clanData definitions")
print("=" * 70)
in_clan = False
for i, line in enumerate(lines, 1):
    if 'clanData' in line and ('{' in line or '=' in line):
        in_clan = True
    if in_clan:
        print(f"  Line {i}: {line.strip()[:120]}")
        if line.strip() == '};' or (line.strip() == '}' and in_clan):
            in_clan = False

# SCAN 10: bossData
print("\n" + "=" * 70) 
print("SCAN 10: bossData definitions")
print("=" * 70)
in_boss = False
for i, line in enumerate(lines, 1):
    if 'bossData' in line and ('{' in line or '=' in line):
        in_boss = True
    if in_boss:
        print(f"  Line {i}: {line.strip()[:120]}")
        if line.strip() == '};':
            in_boss = False
