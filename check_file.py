#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'rb') as f:
    data = f.read()

nul_count = data.count(b'\x00')
bom = data[:3] == b'\xef\xbb\xbf'
soft_hyphen = data.count(b'\xc2\xad')
zero_width = data.count(b'\xe2\x80\x8b')

issues = []
try:
    data.decode('utf-8')
except UnicodeDecodeError as e:
    issues.append(str(e))

print(f'File size: {len(data)} bytes')
print(f'NUL bytes: {nul_count}')
print(f'BOM: {bom}')
print(f'UTF-8 issues: {issues if issues else "None"}')
print(f'Soft hyphens: {soft_hyphen}')
print(f'Zero-width spaces: {zero_width}')

# Check for remaining Á + C2 patterns (double-encoding remnants)
import re
text = data.decode('utf-8')

# Find lines with Á followed by unusual chars
pattern = re.compile(r'.{0,30}\u00c1[\u0080-\u00bf].{0,30}')
matches = pattern.findall(text)
if matches:
    print(f'\nRemaining double-encoding patterns ({len(matches)}):')
    for m in matches[:10]:
        print(f'  {repr(m.strip())}')
else:
    print('\nNo double-encoding remnants found')

# Now check for JS issues - look for accented chars in places they shouldn't be
# (outside of string literals)
# Check if any function/var names got corrupted
corrupted_ids = re.findall(r'(?:function|var|let|const|class)\s+\w*[àáâãäåèéêëìíîïòóôõöùúûüç]\w*', text, re.IGNORECASE)
if corrupted_ids:
    print(f'\nAccented identifiers in code ({len(corrupted_ids)}):')
    for c in corrupted_ids[:10]:
        print(f'  {c}')

# Check if there are broken template literals
broken_templates = re.findall(r'\$\{[^}]*[àáâãäåèéêëìíîïòóôõöùúûüç][^}]*\}', text)
if broken_templates:
    print(f'\nAccented chars in template expressions ({len(broken_templates)}):')
    for b in broken_templates[:5]:
        print(f'  {repr(b)}')
