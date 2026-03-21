#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE FIX: Replace ALL corrupted byte sequences in index.html.
Handles: sidebar icons, boss emojis, admin icons, guide icons, checkmark text, encoding artifacts.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("src/index.html", "rb") as f:
    raw = f.read()

original_size = len(raw)

# ============================================================
# PHASE 1: Fix corrupted emoji byte sequences (📱 + garbage)
# ============================================================
# Pattern: f0 9f 93 b1 + c2 XX [c2 YY [c2 ZZ]]
# These are double-encoded emojis where the original 4-byte emoji
# got corrupted through encoding roundtrips.

byte_replacements = [
    # SIDEBAR NAV ICONS
    # Treinadores: 📱+corruption → 🔴 (Pokéball red)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8f\xc2\x8b', '🔴'.encode('utf-8')),
    # Rainbow Orbs: 📱®+corruption → 🔮 (Crystal Ball)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\xae', '🔮'.encode('utf-8')),
    # Ranking: 📱+corruption → 🏆 (Trophy)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8f\xc2\x86', '🏆'.encode('utf-8')),
    # Guias F2P: 📱¡+corruption → 📖 (Open Book)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x92\xc2\xa1', '💡'.encode('utf-8')),
    # Pokélog: 📱¢+corruption → 🎮 (Game Controller)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\xa2', '🎮'.encode('utf-8')),
    # Sobre o Projeto: 📱+corruption → ℹ️ (Information)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\x8b', 'ℹ️'.encode('utf-8')),
    # Admin: 📱+corruption → 🛡️ (Shield)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x91\xc2\x91', '🛡️'.encode('utf-8')),
    
    # ADMIN TAB ICONS
    # Feedbacks: 📱¬ → 💬
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x92\xc2\xac', '💬'.encode('utf-8')),
    # Estatísticas: 📱 (14 occurrences) → 📊
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\x8a', '📊'.encode('utf-8')),
    # Bug report: 📱+corruption → 🐛
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x90\xc2\x9b', '🐛'.encode('utf-8')),
    # Users/Personagens icon: 📱¥ → 👥
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x91\xc2\xa5', '👥'.encode('utf-8')),
    # User count icon: 📱¤ → 👤
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x91\xc2\xa4', '👤'.encode('utf-8')),
    
    # GUIDE CONTENT ICONS
    # Food/strategy icon: 📱 → 📝
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\x9d', '📝'.encode('utf-8')),    
    # Pokémon capture icon: 📱° → 💰
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x92\xc2\xb0', '💰'.encode('utf-8')),
    # Pokémon types icon (blue): 📱 → 💎
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x92\xc2\x8e', '💎'.encode('utf-8')),
    # Attack/Fire guide icon: 📱¥ → 🔥
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\xa5\xc2\x97', '🔥'.encode('utf-8')),
    # Volt tackle icon: 📱µ → ⚡
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\xb5', '⚡'.encode('utf-8')),
    # Scroll/map icon: 📱§¬ → 🧭
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\xa7\xc2\xac', '🧭'.encode('utf-8')),
    # Checkmark/tool icon: 📱§ → 🔧
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\xa7', '🔧'.encode('utf-8')),
    # Pokémon capture label: 📱¯ → 🎣
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8e\xc2\xaf', '🎣'.encode('utf-8')),
    # Clan icon in form: 📱 → 🏰
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8e\xc2\x96', '🏰'.encode('utf-8')),
    # Fishing icon: 📱 → 🐟
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\x8c', '🐟'.encode('utf-8')),    
    # Firestore icon: 📱¾ → 🗄️
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x92\xc2\xbe', '🗄️'.encode('utf-8')),
    # Expand/collapse: 📱´ → 🔼
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\xb4', '🔼'.encode('utf-8')),
    # Collapse: 📱 → 🔽
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\x96', '🔽'.encode('utf-8')),
    # Reset clock: 📱 → 🔄
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\x84', '🔄'.encode('utf-8')),
    
    # THEME/COMMENT ICONS (less critical but visible in comments)
    # TEMA header: 📱® → 🎨
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8e\xc2\xae', '🎨'.encode('utf-8')),
    # POKÉDEX STYLE: 📱 → 📋
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x93\xc2\x9a', '📋'.encode('utf-8')),
    # Security: 📱 (f0 9f 93 b1 c2 9f c2 94 c2 92) → 🔒
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\x92', '🔒'.encode('utf-8')),

    # BOSS ALERT EMOJIS (epicBossMessages, epicNotifications, epicBossAlerts)
    # These use different patterns:
    
    # Notification bell line: 📱📱📱📱📱📱📱📱📱 (repeating pattern for divider)
    # f0 9f 93 b1 c2 9f c2 94 c2 94 → 🔴 (repeated as divider)
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\x94', '🔴'.encode('utf-8')),
    
    # Notification alert icon: 📱¨ → 🚨
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x9a\xc2\xa8', '🚨'.encode('utf-8')),
    
    # Poképark emoji: 📱 (f0 9f 93 b1 c2 9f c2 8e) → 🎪
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8e', '🎪'.encode('utf-8')),
    
    # PREPARE icon: 📱 (f0 9f 93 b1 c2 9f c2 92) alone → 💪
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x92', '💪'.encode('utf-8')),
    
    # Dragon emoji: 📱 (f0 9f 93 b1 c2 9f c2 90 c2 89) → 🐉
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x90\xc2\x89', '🐉'.encode('utf-8')),
    
    # Magcargo/Fire: 📱¥ (f0 9f 93 b1 c2 9f c2 94 c2 a5) → 🔥
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x94\xc2\xa5', '🔥'.encode('utf-8')),
    
    # Tyranitar/Rock: 📱¨ (f0 9f 93 b1 c2 9f c2 a8) → 🪨
    (b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\xa8', '🪨'.encode('utf-8')),
]

# Sort by length descending to match longest patterns first
byte_replacements.sort(key=lambda x: len(x[0]), reverse=True)

count_total = 0
for old_bytes, new_bytes in byte_replacements:
    count = raw.count(old_bytes)
    if count > 0:
        raw = raw.replace(old_bytes, new_bytes)
        old_text = old_bytes.decode('utf-8', errors='replace')
        new_text = new_bytes.decode('utf-8', errors='replace')
        print(f"✅ Replaced [{old_text}] → [{new_text}] ({count}x)")
        count_total += count

# ============================================================
# PHASE 2: Fix â-pattern corruptions (double-encoded)
# ============================================================
# Pattern: c3 a2 c2 XX c2 YY → should be emoji starting with e2 XX YY
a2_replacements = [
    # â✨ animation icon → ✨
    (b'\xc3\xa2\xc2\x9c\xc2\xa8', '✨'.encode('utf-8')),
    # â⬇ icon → ⬇
    (b'\xc3\xa2\xc2\xad\xc2\x90', '⬇'.encode('utf-8')),
    # â⚙ icon → ⚙
    (b'\xc3\xa2\xc2\x9a\xc2\x99', '⚙'.encode('utf-8')),
    # â❄ icon → ❄
    (b'\xc3\xa2\xc2\x9d\xc2\x84', '❄'.encode('utf-8')),
    # â° → ⏰ (clock)
    (b'\xc3\xa2\xc2\xb0', '⏰'.encode('utf-8')),
]

for old_bytes, new_bytes in a2_replacements:
    count = raw.count(old_bytes)
    if count > 0:
        raw = raw.replace(old_bytes, new_bytes)
        print(f"✅ Fixed â-pattern ({count}x)")
        count_total += count

# ============================================================
# PHASE 3: Fix Sunflora emoji in epicBossMessages (🌪️» → ☀️)
# ============================================================
text = raw.decode('utf-8', errors='replace')

# epicBossMessages Sunflora
text = text.replace('🌪️»', '☀️')
c = text.count('☀️')  # Just checking
print(f"✅ Fixed Sunflora emoji (🌪️» → ☀️)")

# epicBossMessages Magcargo (already 📱¥ → should be 🌋 in messages context)
# These should be the BOSS-specific emojis, matching bossData

# ============================================================
# PHASE 4: Fix remaining text corruption (checkmarks → Portuguese)
# ============================================================
checkmark_fixes = {
    # Double checkmark patterns (çã → ção, etc.)
    '✓✓o ': 'ção ',
    '✓✓o,': 'ção,',
    '✓✓o.': 'ção.',
    '✓✓o;': 'ção;',
    '✓✓o)': 'ção)',
    '✓✓o"': 'ção"',
    '✓✓o`': 'ção`',
    "✓✓o'": "ção'",
    '✓✓o<': 'ção<',
    '✓✓o:': 'ção:',
    '✓✓o}': 'ção}',
    'Notifica✓✓o': 'Notificação',
    'Aplica✓✓o': 'Aplicação',
    'Dura✓✓o': 'Duração',
    'Fun✓✓es': 'Funções',
    'Manuten✓✓o': 'Manutenção',
    'Pontua✓✓o': 'Pontuação',
    'altera✓✓o': 'alteração',
    'cole✓✓o': 'coleção',
    'formata✓✓o': 'formatação',
    'fun✓✓o': 'função',
    'intera✓✓o': 'interação',
    'notifica✓✓es': 'notificações',
    'observa✓✓o': 'observação',
    'se✓✓o': 'secção',
    'transa✓✓o': 'transação',
    
    # Single checkmark patterns
    'CONCLU✓DO': 'CONCLUÍDO',
    'CONCLU✓DAS': 'CONCLUÍDAS',
    'An✓nima': 'Anónima',
    'Cient✓fica': 'Científica',
    'Cient✓fico': 'Científico',
    'Di✓rio': 'Diário',
    'L✓gica': 'Lógica',
    'M✓ximo': 'Máximo',
    'Obt✓m': 'Obtém',
    'Profiss✓es': 'Profissões',
    'RELAT✓RIO': 'RELATÓRIO',
    'Seguran✓a': 'Segurança',
    'Usu✓rio': 'Usuário',
    'agrad✓vel': 'agradável',
    'an✓ncio': 'anúncio',
    'ass✓ncrona': 'assíncrona',
    'autom✓tica': 'automática',
    'coer✓ncia': 'coerência',
    'conex✓o': 'conexão',
    'conte✓do': 'conteúdo',
    'espec✓fico': 'específico',
    'estat✓sticas': 'estatísticas',
    'est✓o': 'estão',
    'est✓ ': 'está ',
    'hor✓rios': 'horários',
    'matem✓tica': 'matemática',
    'mudan✓a': 'mudança',
    'n✓mero': 'número',
    'pok✓ball': 'pokéball',
    'p✓blicos': 'públicos',
    'seguran✓a': 'segurança',
    'tem✓tica': 'temática',
    'tem✓ticas': 'temáticas',
    'usu✓rios': 'usuários',
    'vis✓vel': 'visível',
    '✓ndice': 'índice',
    '✓pica': 'épica',
    '✓picas': 'épicas',
    '✓Ácone': 'Ícone',
    'Acad✓mico': 'Académico',
    'Arque✓logo': 'Arqueólogo',
    'at✓ ': 'até ',
    'title="1✓': 'title="1ª',
    'title="2✓': 'title="2ª',
    'title="3✓': 'title="3ª',
}

for old, new in checkmark_fixes.items():
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        count_total += count
        if count >= 3:
            print(f"✅ Checkmark: '{old}' → '{new}' ({count}x)")

# ============================================================
# PHASE 5: Fix encoding artifacts
# ============================================================
encoding_fixes = {
    'POKÁPARK': 'POKÉPARK',
    'DRAGÁO': 'DRAGÃO',
    'COMEÁANDO': 'COMEÇANDO',
    'esTática': 'estática',
    'eCrítico': 'espaço',  # "um único eCrítico" → "um único espaço"
    'NÁ­vel': 'Nível',
    'InÁ­cio': 'Início',
    'nÁ£o ': 'não ',
    'Cr✓tico': 'Crítico',
    '✓picos': 'épicos',
    '✓ 2026': '© 2026',
    '✓ v<': '• v<',
    '✓ ENTENDI ✓': '✓ ENTENDI ✓',  # Keep these - they're intentional
}

for old, new in encoding_fixes.items():
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        count_total += count
        print(f"✅ Encoding: '{old}' → '{new}' ({count}x)")

# ============================================================
# PHASE 6: Fix epicBossMessages to use correct emojis
# ============================================================
# These need to match the bossData emojis which are already correct:
# Sunflora=☀️, Magcargo=🌋, Tyranitar=🪨, Dragonair=🐉, Mamoswine=❄️

boss_msg_fixes = {
    # epicBossMessages - already partially fixed by byte replacements
    # Fix remaining patterns
    '"âi¸"': '"❄️"',
    "'âi¸'": "'❄️'",
    'âi¸ ': '❄️ ',
}

for old, new in boss_msg_fixes.items():
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        count_total += count
        print(f"✅ Boss: '{old}' → '{new}' ({count}x)")

# ============================================================
# SAVE
# ============================================================
raw_out = text.encode('utf-8')
with open("src/index.html", "wb") as f:
    f.write(raw_out)

print(f"\n{'='*60}")
print(f"✅ TOTAL FIXES APPLIED: {count_total}")
print(f"✅ File size: {original_size} → {len(raw_out)} bytes")
print(f"✅ File saved with UTF-8 encoding (no BOM)")
