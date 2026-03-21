#!/usr/bin/env python3
"""Check if any encoding replacements broke JS code by looking at accent chars in code context"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'rb') as f:
    data = f.read()

text = data.decode('utf-8')
lines = text.split('\n')

# We're inside <script type="module"> from around line 6637 to ~15120
# Check for any C1 control characters (U+0080-U+009F) in script sections
in_script = False
issues = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if '<script' in stripped.lower():
        in_script = True
    if '</script>' in stripped.lower():
        in_script = False
    
    if in_script:
        # Check for C1 control chars (U+0080-U+009F) which are suspicious
        for j, c in enumerate(line):
            if 0x80 <= ord(c) <= 0x9F:
                ctx_start = max(0, j-30)
                ctx_end = min(len(line), j+30)
                issues.append((i, f'U+{ord(c):04X}', line[ctx_start:ctx_end].strip()))

if issues:
    print(f'=== C1 control chars in script blocks: {len(issues)} ===')
    for line_num, char_code, ctx in issues:
        print(f'  Line {line_num}: {char_code} ... {ctx[:80]}')
else:
    print('No C1 control chars in script blocks')

# Also check if the file has any unclosed template literals or strings
print('\n=== Checking for potential JS errors ===')

# Count backticks - should be even
in_module = False
backtick_count = 0
module_start = None
module_end = None
for i, line in enumerate(lines, 1):
    if '<script type="module">' in line:
        in_module = True
        module_start = i
    if in_module and '</script>' in line and i > (module_start or 0):
        module_end = i
        break
    if in_module:
        backtick_count += line.count('`')

print(f'Module script: lines {module_start}-{module_end}')
print(f'Backtick count: {backtick_count} ({"even - OK" if backtick_count % 2 == 0 else "ODD - PROBLEM!"})')

# Check for missing 'finance' safety 
finance_lines = []
for i, line in enumerate(lines, 1):
    if 'char.finance.' in line and '?' not in line[line.index('char.finance.'):line.index('char.finance.')+20]:
        finance_lines.append((i, line.strip()[:100]))

print(f'\nUnsafe char.finance. accesses (no optional chaining):')
for ln, ctx in finance_lines:
    print(f'  Line {ln}: {ctx}')
