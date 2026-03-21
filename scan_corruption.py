#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan index.html for all emoji/icon corruption patterns.
Finds corrupted bytes, mojibake, and encoding artifacts.
"""

import re

with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()
    lines = text.split('\n')

print("=" * 80)
print("SCAN 1: Remaining checkmarks (✓) that look like corruption")
print("=" * 80)
for i, line in enumerate(lines, 1):
    if '✓' in line:
        # Skip lines where ✓ is clearly intentional
        stripped = line.strip()
        # Gather context around each ✓
        for m in re.finditer('✓', line):
            start = max(0, m.start() - 15)
            end = min(len(line), m.end() + 15)
            ctx = line[start:end].strip()
            print(f"  Line {i}: ...{ctx}...")

print("\n" + "=" * 80)
print("SCAN 2: Corrupted encoding patterns (Á, Ã, etc.)")
print("=" * 80)
# Look for Latin-1 double-encoding patterns
patterns = [
    (r'Á£', 'ã'), (r'Á§', 'ç'), (r'Á©', 'é'), (r'Á­', 'í'),
    (r'Á¡', 'á'), (r'Ã£', 'ã'), (r'Ã§', 'ç'), (r'Ã©', 'é'),
    (r'Ã­', 'í'), (r'Ã¡', 'á'), (r'Ã³', 'ó'), (r'Ãº', 'ú'),
    (r'Ã¢', 'â'), (r'Ãµ', 'õ'), (r'Ã¼', 'ü'),
]
for pat, correct in patterns:
    count = text.count(pat)
    if count > 0:
        print(f"  Found '{pat}' (should be '{correct}'): {count} occurrences")
        for i, line in enumerate(lines, 1):
            if pat in line:
                idx = line.index(pat)
                start = max(0, idx - 20)
                end = min(len(line), idx + len(pat) + 20)
                print(f"    Line {i}: ...{line[start:end].strip()}...")
                if count > 3:
                    break  # Just show first for common ones

print("\n" + "=" * 80)
print("SCAN 3: Corrupted emoji patterns (📱 followed by unexpected chars)")
print("=" * 80)
for i, line in enumerate(lines, 1):
    if '📱' in line:
        for m in re.finditer('📱', line):
            start = max(0, m.start() - 5)
            end = min(len(line), m.end() + 10)
            ctx = line[start:end].strip()
            print(f"  Line {i}: ...{ctx}...")

print("\n" + "=" * 80)
print("SCAN 4: Sidebar/Nav icon definitions")
print("=" * 80)
for i, line in enumerate(lines, 1):
    if 'nav-icon' in line.lower() or ('switchTab' in line and 'icon' in line.lower()):
        print(f"  Line {i}: {line.strip()[:120]}...")

print("\n" + "=" * 80)
print("SCAN 5: Tab button icons (sidebar buttons)")  
print("=" * 80)
in_nav = False
for i, line in enumerate(lines, 1):
    if 'switchTab' in line:
        in_nav = True
    if in_nav:
        stripped = line.strip()
        if stripped:
            print(f"  Line {i}: {stripped[:120]}")
        if '</button>' in line:
            in_nav = False
            print()

print("\n" + "=" * 80)
print("SCAN 6: Icon/emoji definitions in data objects")
print("=" * 80)
for i, line in enumerate(lines, 1):
    if re.search(r"icon:\s*['\"]", line) or re.search(r"emoji:\s*['\"]", line):
        print(f"  Line {i}: {line.strip()[:120]}")

print("\n" + "=" * 80)
print("SCAN 7: Tilde (~) that may be corrupted ternary operators")
print("=" * 80)
tilde_count = 0
for i, line in enumerate(lines, 1):
    if '~' in line:
        stripped = line.strip()
        # Skip comments and strings that naturally have ~
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        # Check for ~ used as operator replacement
        for m in re.finditer(r'[^~]~[^~]', line):
            ctx_start = max(0, m.start() - 10)
            ctx_end = min(len(line), m.end() + 10)
            ctx = line[ctx_start:ctx_end].strip()
            if '~~' not in ctx and 'http' not in ctx:
                tilde_count += 1
                if tilde_count <= 20:
                    print(f"  Line {i}: ...{ctx}...")

if tilde_count > 20:
    print(f"  ... and {tilde_count - 20} more")

print(f"\nTotal tilde occurrences in non-comment code: {tilde_count}")

print("\n" + "=" * 80)
print("SCAN 8: 'eCrítico' pattern (corrupted text)")
print("=" * 80)
for i, line in enumerate(lines, 1):
    if 'eCrítico' in line:
        idx = line.index('eCrítico')
        start = max(0, idx - 30)
        end = min(len(line), idx + 40)
        print(f"  Line {i}: ...{line[start:end].strip()}...")

print("\n" + "=" * 80)
print("SCAN 9: nÁ£o pattern (corrupted nao)")
print("=" * 80)
for i, line in enumerate(lines, 1):
    if 'nÁ£o' in line:
        idx = line.index('nÁ£o')
        start = max(0, idx - 20)
        end = min(len(line), idx + 30)
        print(f"  Line {i}: ...{line[start:end].strip()}...")
