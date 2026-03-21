#!/usr/bin/env python3
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = {
    'Phone emoji': text.count('\U0001f4f1'),
    'Latin-1 c-cedilla': text.count('Á§'),
    'Latin-1 a-tilde': text.count('Á£'),
    'Latin-1 a-acute': text.count('Á¡'),
    'Latin-1 i-acute': text.count('Á\u00ad'),
    'Latin-1 o-tilde': text.count('Áµ'),
    'Latin-1 a-circumflex': text.count('Á¢'),
    'Checkmarks': text.count('\u2713'),
    'POKAPARK': text.count('POKÁPARK'),
    'COMEAANDO': text.count('COMEÁANDO'),
    'eCritico': text.count('eCrítico'),
    'Gestao o': text.count('Gestão o'),
}

print('=== FINAL VERIFICATION ===')
for label, count in checks.items():
    ok = count == 0 or (label == 'Checkmarks' and count <= 21)
    print(f"{'OK' if ok else 'FAIL'} {label}: {count}")

double_enc = re.findall(r'[A-Za-z]+\u00c1[\u00a7\u00a3\u00a1\u00ad\u00b5\u00a2\u00a9][A-Za-z]*', text)
if double_enc:
    print(f"\nFAIL Remaining: {double_enc[:20]}")
else:
    print(f"\nOK No double-encoded words found")

print(f"\nFile size: {len(text):,} chars")
