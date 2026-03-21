#!/usr/bin/env python3
"""Find and fix remaining corrupted emojis (â-prefix patterns)."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'rb') as f:
    data = f.read()

text = data.decode('utf-8')
lines = text.split('\n')

# Find all instances of â followed by control/special chars in script blocks
# These are partially-decoded 3-byte UTF-8 emojis
# â = E2 in first byte, followed by 2 continuation bytes that got separated

in_script = False
emoji_issues = []
for i, line in enumerate(lines, 1):
    if '<script' in line.lower():
        in_script = True
    if '</script>' in line.lower():
        in_script = False
    
    if in_script or True:  # check everywhere
        # Look for â followed by unusual chars (potential broken 3-byte UTF-8)
        for m in re.finditer(r'â[\u0080-\u00bf][\u0080-\u00bf]?|â[°¬]', line):
            ctx_start = max(0, m.start()-30)
            ctx_end = min(len(line), m.end()+30)
            chars = m.group()
            hex_repr = ' '.join(f'{ord(c):04x}' for c in chars)
            # Try to reconstruct the original 3-byte UTF-8 sequence
            if len(chars) >= 2:
                try:
                    # The original bytes were E2 XX YY
                    b1 = 0xE2  # â
                    b2 = ord(chars[1])
                    b3 = ord(chars[2]) if len(chars) > 2 else None
                    if b3:
                        original = bytes([b1, b2, b3]).decode('utf-8')
                        emoji_issues.append((i, hex_repr, original, chars, line[ctx_start:ctx_end].strip()))
                    else:
                        emoji_issues.append((i, hex_repr, '?', chars, line[ctx_start:ctx_end].strip()))
                except:
                    emoji_issues.append((i, hex_repr, '?', chars, line[ctx_start:ctx_end].strip()))

print(f"=== Corrupted emoji patterns found: {len(emoji_issues)} ===\n")
for ln, hex_r, orig, chars, ctx in emoji_issues[:30]:
    print(f"Line {ln}: [{hex_r}] -> {orig} ({repr(orig)}) ... {ctx[:80]}")

# Also find ❄i¸ pattern
ice_count = text.count('❄i¸')
print(f"\n❄i¸ occurrences: {ice_count}")

# Also look for specific corrupted text patterns  
patterns = ['â ', 'â°', 'â¬', 'â']
for p in patterns:
    count = text.count(p)
    if count > 0:
        # Find lines
        for i, line in enumerate(lines, 1):
            if p in line:
                idx = line.index(p)
                ctx = line[max(0,idx-20):idx+len(p)+20].strip()
                print(f"  '{p}' at line {i}: ...{ctx[:80]}")
