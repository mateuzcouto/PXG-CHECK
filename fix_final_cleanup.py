#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL CLEANUP: Fix ALL remaining encoding artifacts.
Latin-1 double-encoding: Á§=ç, Á£=ã, Á¡=á, Á­=í, Áµ=õ, Á¢=â, Á©=é
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("src/index.html", "r", encoding='utf-8') as f:
    text = f.read()

# ============================================================
# PHASE 1: Fix Latin-1 double-encoded characters
# ============================================================
# These are character pairs where the original accented char
# was double-encoded through Latin-1 → UTF-8 conversion
latin1_fixes = {
    # Multi-char patterns (fix first to avoid partial matches)
    'Á§Áµes': 'ções',      # e.g. descrições, notificações
    'Á§Á£o': 'ção',        # e.g. Gestão, sugestão  
    'Á§a ': 'ça ',         # e.g. começa
    'Á§a,': 'ça,',
    'Á§as ': 'ças ',
    'Á§as.': 'ças.',
    'Á§Áµ': 'çõ',          # generic pattern
    'Á§': 'ç',             # generic ç
    'Á£o ': 'ão ',         # e.g. Gestão
    'Á£o,': 'ão,',
    'Á£o.': 'ão.',
    'Á£o"': 'ão"',
    "Á£o'": "ão'",
    'Á£o<': 'ão<',
    'Á£o)': 'ão)',
    'Á£o;': 'ão;',
    'Á£o:': 'ão:',
    'Á£': 'ã',             # generic ã
    'Á¡': 'á',             # e.g. Básico, máximo
    'Á­': 'í',             # e.g. possível
    'Áµ': 'õ',             # e.g. descrições
    'Á¢': 'â',             # e.g. Dinâmico
    'Á©': 'é',             # e.g. Poképark
}

count_total = 0
for old, new in latin1_fixes.items():
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        count_total += count
        if count >= 2:
            print(f"✅ '{old}' → '{new}' ({count}x)")

# ============================================================
# PHASE 2: Fix remaining specific corrupted words/phrases
# ============================================================
specific_fixes = {
    # Fix "GestÃ£o o" pattern (extra space+o from previous fixes)
    'Gestão o de': 'Gestão de',
    'Gestão o do': 'Gestão do',
    'Gestão o Integral': 'Gestão Integral',
    'SuGestão es': 'Sugestões',
    'SuGestão o': 'Sugestão',
    'comeÁ§a': 'começa',  # if not caught by generic
    
    # Fix Poképark and related
    'POKÁPARK': 'POKÉPARK',
    'COMEÁANDO': 'COMEÇANDO',
    'DRAGÁO': 'DRAGÃO',
    
    # Fix remaining é/ê corruption
    'esTática': 'estática',
    'espaço,': 'ecrã,',  # Fix the eCrítico→espaço that was wrong
    
    # Fix comment checkmarks
    '✓Ácone': 'Ícone',
    
    # Fix code corruption
    "não ✓ admin": "não é admin",
    "O JSON ✓ uma lista": "O JSON é uma lista",
    
    # Fix ✓picos ✓ticas in comments
    '✓picos': 'épicos',
    '✓ticas': 'éticas',
    '✓picas tem✓ticas': 'épicas temáticas',
    'est✓ EM': 'está EM',
}

for old, new in specific_fixes.items():
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        count_total += count
        print(f"✅ '{old}' → '{new}' ({count}x)")

# ============================================================
# PHASE 3: Fix remaining â→ patterns in guide text
# ============================================================
arrow_fixes = {
    ' â ': ' → ',  # Arrow separator in boss sequence
}
for old, new in arrow_fixes.items():
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        count_total += count
        print(f"✅ Arrow fix: '{old}' → '{new}' ({count}x)")

# ============================================================
# SAVE
# ============================================================
with open("src/index.html", "w", encoding='utf-8') as f:
    f.write(text)

print(f"\n{'='*60}")
print(f"✅ TOTAL ADDITIONAL FIXES: {count_total}")
print(f"✅ File saved with UTF-8 encoding")

# Verify remaining issues
remaining_checkmarks = text.count('✓')
remaining_phone = text.count('📱')
remaining_latin1 = sum(text.count(p) for p in ['Á§', 'Á£', 'Á¡', 'Á­', 'Áµ', 'Á¢'])
print(f"\n--- VERIFICATION ---")
print(f"Remaining ✓: {remaining_checkmarks} (should be only intentional ones)")
print(f"Remaining 📱: {remaining_phone}")
print(f"Remaining Latin-1 artifacts: {remaining_latin1}")
