#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find EXACT byte sequences for all phone emoji occurrences to build replacement map.
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("src/index.html", "rb") as f:
    raw = f.read()

text = raw.decode('utf-8', errors='replace')

# Find all 📱 (f0 9f 93 b1) occurrences with surrounding context
phone_bytes = b'\xf0\x9f\x93\xb1'
pos = 0
unique_seqs = {}
while True:
    idx = raw.find(phone_bytes, pos)
    if idx == -1:
        break
    
    # Get 20 bytes after the phone emoji
    after = raw[idx+4:idx+20]
    line_num = raw[:idx].count(b'\n') + 1
    
    # Get the full corrupted emoji sequence (phone + continuation bytes)
    seq_end = idx + 4
    # Read continuation bytes that look like part of the corruption
    while seq_end < len(raw) and seq_end < idx + 20:
        b = raw[seq_end]
        # C2 xx patterns are part of double-encoding
        if b == 0xc2:
            seq_end += 2
        elif b == 0xef and seq_end + 2 < len(raw) and raw[seq_end+1] == 0xb8 and raw[seq_end+2] == 0x8f:
            seq_end += 3  # variation selector
        else:
            break
    
    seq = raw[idx:seq_end]
    hex_seq = ' '.join(f'{b:02x}' for b in seq)
    
    # Get text context
    ctx_start = max(0, idx - 30)
    ctx_end = min(len(raw), idx + 40)
    ctx_text = raw[ctx_start:ctx_end].decode('utf-8', errors='replace')
    ctx_text = ctx_text.replace('\n', ' ').strip()
    
    key = hex_seq
    if key not in unique_seqs:
        unique_seqs[key] = {'count': 0, 'lines': [], 'ctx': ctx_text}
    unique_seqs[key]['count'] += 1
    unique_seqs[key]['lines'].append(line_num)
    
    pos = idx + 4

print("=== UNIQUE 📱 BYTE SEQUENCES ===")
for hex_seq, info in sorted(unique_seqs.items(), key=lambda x: -x[1]['count']):
    lines_str = str(info['lines'][:5])
    if len(info['lines']) > 5:
        lines_str += "..."
    print(f"\n  Hex: [{hex_seq}]")
    print(f"  Count: {info['count']}")
    print(f"  Lines: {lines_str}")
    print(f"  Context: {info['ctx'][:80]}")

# Also check for remaining 'âi¸' patterns (ê bytes)
print("\n\n=== Looking for corruption marker bytes ===")
# Check for â followed by non-standard  
for pat_name, pat_bytes in [
    ('â pattern', b'\xc3\xa2'),
]:
    positions = []
    p = 0
    while True:
        idx = raw.find(pat_bytes, p)
        if idx == -1:
            break
        line_num = raw[:idx].count(b'\n') + 1
        after_hex = ' '.join(f'{b:02x}' for b in raw[idx:idx+10])
        positions.append((line_num, after_hex))
        p = idx + 2
    print(f"\n{pat_name}: {len(positions)} occurrences")
    for ln, hx in positions[:10]:
        print(f"  Line {ln}: {hx}")
