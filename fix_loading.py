#!/usr/bin/env python3
"""Fix the infinite loading issue:
1. Add try/catch around render/renderRanking so hideLoader always runs
2. Add optional chaining for char.finance access
3. Fix remaining double-encoding (Á+control char patterns)
4. Fix misc corrupted text
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('src/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

fixes = 0

# ============================================
# FIX 1: Wrap render/renderRanking in try/catch so hideLoader always runs
# ============================================
old = """            render();\r\n\r\n\r\n\r\n            renderRanking();\r\n\r\n\r\n\r\n            // Orbs agora são atualizadas por uma função de fetch assíncrona\r\n\r\n\r\n\r\n            hideLoader();\r\n\r\n\r\n\r\n        });"""
new = """            try {\r\n                render();\r\n                renderRanking();\r\n            } catch(e) {\r\n                console.error('Erro ao renderizar:', e);\r\n            }\r\n\r\n            hideLoader();\r\n\r\n        });"""

if old in text:
    text = text.replace(old, new)
    fixes += 1
    print("FIX 1: Wrapped render/renderRanking in try/catch + hideLoader always runs")
else:
    print("SKIP 1: Pattern not found for render/hideLoader wrapper")

# ============================================
# FIX 2: Safe char.finance access (optional chaining)
# ============================================
finance_fixes = [
    ('char.finance.transactions', 'char.finance?.transactions'),
    ('char.finance.currentCash', 'char.finance?.currentCash'),
]
for old_f, new_f in finance_fixes:
    count = text.count(old_f)
    if count > 0:
        text = text.replace(old_f, new_f)
        fixes += count
        print(f"FIX 2: {old_f} -> {new_f} ({count}x)")

# ============================================
# FIX 3: Fix Á+control char double-encoding (uppercase accents)
# The pattern is Á (U+00C1) followed by U+0080-U+00BF control char
# The intended char is chr(control_char_code + 0x40)
# ============================================
double_enc_map = {
    '\u00c1\u0081': 'Á',   # TEMÁTICAS
    '\u00c1\u0083': 'Ã',   # DRAGÃO
    '\u00c1\u0087': 'Ç',   # COMEÇANDO, ANIMAÇÕES
    '\u00c1\u0089': 'É',   # POKÉPARK, ÉPICAS, POKÉDEX
    '\u00c1\u0095': 'Õ',   # ANIMAÇÕES (ÕES)
    '\u00c1\u00b4': 'ô',   # Robô
}

for old_c, new_c in double_enc_map.items():
    count = text.count(old_c)
    if count > 0:
        text = text.replace(old_c, new_c)
        fixes += count
        print(f"FIX 3: U+00C1 U+{ord(old_c[1]):04X} -> {new_c} ({count}x)")

# ============================================
# FIX 4: Fix remaining corrupted text
# ============================================
text_fixes = {
    'mÁs': 'Mês',         # finMonth: "mÁs" -> "Mês"
    'Este mÁs': 'Este Mês',  # ranking display
    'SuGestão': 'Sugestão',   # Fix capitalization
}
for old_t, new_t in text_fixes.items():
    count = text.count(old_t)
    if count > 0:
        text = text.replace(old_t, new_t)
        fixes += count
        print(f"FIX 4: '{old_t}' -> '{new_t}' ({count}x)")

# ============================================
# FIX 5: Add onSnapshot error handler for initData
# ============================================
old_init = 'onSnapshot(q, (snapshot) => {'
# Count occurrences to find the right one (should be in initData)
# Actually there may be multiple onSnapshot calls; let's check context
# We want the one in initData function - look for the one after the characters query
old_init_ctx = "const q = query(collection(db, 'artifacts', DB_COLLECTION, 'users', uid, 'characters'));"
idx = text.find(old_init_ctx)
if idx >= 0:
    next_on_snapshot = text.find('onSnapshot(q, (snapshot) => {', idx)
    if next_on_snapshot >= 0:
        # Find the closing }); for this onSnapshot callback
        # We need to add an error handler callback
        # The closing pattern should be the one after hideLoader()
        after_hide = text.find('hideLoader();', next_on_snapshot)
        if after_hide >= 0:
            # Find the closing }); after hideLoader
            close_idx = text.find('});', after_hide)
            if close_idx >= 0:
                old_close = text[close_idx:close_idx+4]  # '});\r' or '});'
                new_close = '}, (error) => {\r\n            console.error("Erro Firestore snapshot:", error);\r\n            hideLoader();\r\n        });'
                # Only replace this specific occurrence
                text = text[:close_idx] + new_close + text[close_idx+3:]
                fixes += 1
                print("FIX 5: Added Firestore onSnapshot error handler with hideLoader fallback")

# ============================================
# SAVE
# ============================================
with open('src/index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print(f"\n{'='*60}")
print(f"TOTAL FIXES: {fixes}")

# Verify
remaining_c1 = sum(1 for m in re.finditer('[\u00c1][\u0080-\u00bf]', text))
print(f"Remaining Á+control patterns: {remaining_c1}")
print(f"char.finance. (unsafe): {text.count('char.finance.') - text.count('char.finance?.')}")
