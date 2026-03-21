#!/usr/bin/env python3
"""Find ALL remaining corrupted characters by byte-level scan."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'rb') as f:
    data = f.read()

text = data.decode('utf-8')
lines = text.split('\n')

# Find all instances of C3 81 C2 XX (double-encoded uppercase accents) in the file
# C3 81 = U+00C1 (Á) and C2 XX are continuation bytes
import struct

# Search for Á followed by chars 0x80-0xBF (which are C2 80 - C2 BF in UTF-8)
# These are the patterns we need to fix
pattern = re.compile('[\u00c0-\u00c5][\u0080-\u00bf]')
matches = []
for i, line in enumerate(lines, 1):
    for m in pattern.finditer(line):
        ctx_start = max(0, m.start()-20)
        ctx_end = min(len(line), m.end()+20)
        char_pair = m.group()
        hex_pair = ' '.join(f'{ord(c):04x}' for c in char_pair)
        matches.append((i, hex_pair, char_pair, line[ctx_start:ctx_end].strip()))

print(f'=== Double-encoded chars found: {len(matches)} ===\n')
for line_num, hex_p, chars, ctx in matches:
    print(f'Line {line_num}: [{hex_p}] = "{chars}" ... {ctx}')

# Also: search for other common corruption patterns
print('\n=== Other corruption patterns ===')

# Check for Ã followed by common Latin-1 mishaps
pattern2 = re.compile('Ã[\u0080-\u009f]')
matches2 = []
for i, line in enumerate(lines, 1):
    for m in pattern2.finditer(line):
        ctx_start = max(0, m.start()-15)
        ctx_end = min(len(line), m.end()+15)
        matches2.append((i, repr(m.group()), line[ctx_start:ctx_end].strip()))

for line_num, chars, ctx in matches2:
    print(f'Line {line_num}: {chars} ... {ctx}')

# Check for the specific template expressions the check found
print('\n=== Specific corrupted words search ===')
searches = ['Sugestão', 'anúncio', 'Anônimo', 'Profissão', 'POKÉDEX', 'ÉPICAS', 'COMEÇANDO', 'DRAGÃO', 'Robô']
for word in searches:
    # Also search for corrupted version
    count = text.count(word) 
    print(f'  "{word}": {count} occurrences (should be > 0)')
