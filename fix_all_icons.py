#!/usr/bin/env python3
# Fix all corrupted icons throughout the file

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

fixes = []

# World color icons
replacements = [
    # World icons
    ("'Aurora': { text: 'text-green-400', icon: 'âi¸' },", "'Aurora': { text: 'text-green-400', icon: '🌌' },"),
    ("'Omega': { text: 'text-red-600', icon: '📱' },", "'Omega': { text: 'text-red-600', icon: '❤️' },"),
    ("'Cosmic': { text: 'text-purple-500', icon: '📱' },", "'Cosmic': { text: 'text-purple-500', icon: '⭐' },"),
    ("'Steel': { text: 'text-slate-400', icon: 'âi¸' },", "'Steel': { text: 'text-slate-400', icon: '⚙️' },"),
    ("'Wind': { text: 'text-cyan-400', icon: '📱¨' },", "'Wind': { text: 'text-cyan-400', icon: '💨' },"),
    ("'Lunar': { text: 'text-indigo-300', icon: '📱' },", "'Lunar': { text: 'text-indigo-300', icon: '🌙' },"),
    ("'Ocean': { text: 'text-blue-500', icon: '📱' },", "'Ocean': { text: 'text-blue-500', icon: '🌊' },"),
    ("'Flame': { text: 'text-orange-500', icon: '📱¥' },", "'Flame': { text: 'text-orange-500', icon: '🔥' },"),
    ("'Rainbow': { text: 'text-pink-400', icon: '📱' },", "'Rainbow': { text: 'text-pink-400', icon: '🌈' },"),
    ("'Emerald': { text: 'text-emerald-400', icon: '📱' },", "'Emerald': { text: 'text-emerald-400', icon: '💎' },"),
    
    # Clan icons
    ('volcanic: { name: "Volcanic", color: "bg-red-600", icon: "📱", border: "border-red-500", text: "text-red-400" },',
     'volcanic: { name: "Volcanic", color: "bg-red-600", icon: "🔴", border: "border-red-500", text: "text-red-400" },'),
    
    ('seavell: { name: "Seavell", color: "bg-blue-600", icon: "📱", border: "border-blue-500", text: "text-blue-400" },',
     'seavell: { name: "Seavell", color: "bg-blue-600", icon: "🌊", border: "border-blue-500", text: "text-blue-400" },'),
    
    ('orebound: { name: "Orebound", color: "bg-amber-800", icon: "âi¸", border: "border-amber-700", text: "text-amber-500" },',
     'orebound: { name: "Orebound", color: "bg-amber-800", icon: "⛏️", border: "border-amber-700", text: "text-amber-500" },'),
    
    ('wingeon: { name: "Wingeon", color: "bg-sky-400", icon: "📱", border: "border-sky-300", text: "text-sky-300" },',
     'wingeon: { name: "Wingeon", color: "bg-sky-400", icon: "🌪️", border: "border-sky-300", text: "text-sky-300" },'),
    
    ('naturia: { name: "Naturia", color: "bg-green-600", icon: "📱?", border: "border-green-500", text: "text-green-400" },',
     'naturia: { name: "Naturia", color: "bg-green-600", icon: "🌿", border: "border-green-500", text: "text-green-400" },'),
    
    ('malefic: { name: "Malefic", color: "bg-purple-700", icon: "📱", border: "border-purple-500", text: "text-purple-400" },',
     'malefic: { name: "Malefic", color: "bg-purple-700", icon: "☠️", border: "border-purple-500", text: "text-purple-400" },'),
    
    ('psycraft: { name: "Psycraft", color: "bg-pink-500", icon: "📱§ ", border: "border-pink-400", text: "text-pink-400" },',
     'psycraft: { name: "Psycraft", color: "bg-pink-500", icon: "🔮", border: "border-pink-400", text: "text-pink-400" },'),
    
    ('ironhard: { name: "Ironhard", color: "bg-slate-500", icon: "âi¸", border: "border-slate-400", text: "text-slate-300" }',
     'ironhard: { name: "Ironhard", color: "bg-slate-500", icon: "⚙️", border: "border-slate-400", text: "text-slate-300" }'),
    
    # Boss icons
    ("'Sunflora': { key: 'boss12', storageKey: 'boss12', emoji: '📱»', icon: '📱»', danger: '⚡ CrÁ­tico', energy: 'AMARELA' },",
     "'Sunflora': { key: 'boss12', storageKey: 'boss12', emoji: '☀️', icon: '☀️', danger: '⚡ Crítico', energy: 'AMARELA' },"),
    
    ("'Magcargo': { key: 'boss16', storageKey: 'boss16', emoji: '📱¥', icon: '📱¥', danger: '⚡ CrÁ­tico', energy: 'VERMELHA' },",
     "'Magcargo': { key: 'boss16', storageKey: 'boss16', emoji: '🌋', icon: '🌋', danger: '⚡ Crítico', energy: 'VERMELHA' },"),
    
    ("'Tyranitar': { key: 'boss20', storageKey: 'boss20', emoji: '📱¨', icon: '📱¨', danger: '📱¥ EXTREMO', energy: 'ROXA' },",
     "'Tyranitar': { key: 'boss20', storageKey: 'boss20', emoji: '🪨', icon: '🪨', danger: '⚡ EXTREMO', energy: 'ROXA' },"),
    
    ("'Dragonair': { key: 'boss12', storageKey: 'boss12', emoji: '📱', icon: '📱', danger: '⚡ ALTO', energy: 'AZUL' },",
     "'Dragonair': { key: 'boss12', storageKey: 'boss12', emoji: '🐉', icon: '🐉', danger: '⚡ ALTO', energy: 'AZUL' },"),
    
    ("'Mamoswine': { key: 'boss23', storageKey: 'boss23', emoji: 'âi¸', icon: 'âi¸', danger: '⚡ CrÁ­tico', energy: 'BRANCA' }",
     "'Mamoswine': { key: 'boss23', storageKey: 'boss23', emoji: '❄️', icon: '❄️', danger: '⚡ Crítico', energy: 'BRANCA' }"),
    
    # Banner icon that spins
    ('el.innerHTML = `<span class="pokeball-banner-icon">📱</span>${bannerText}`;',
     'el.innerHTML = `<span class="pokeball-banner-icon">🔴</span>${bannerText}`;'),
    
    # Form labels
    ('📱£ NÁ­vel de Pesca', '🎣 Nível de Pesca'),
    ('📱¯ Pokémon Capturados', '🎪 Pokémon Capturados'),
    ('Cl✓</label>', 'Clã</label>'),
    
    # Clan current icon
    ('<span class="bg-red-600 clan-badge-small" id="current-clan-icon">📱</span>',
     '<span class="bg-red-600 clan-badge-small" id="current-clan-icon">🔴</span>'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes.append(f"✅ Fixed: {old[:50]}...")
    else:
        fixes.append(f"⚠️ Not found: {old[:50]}...")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=== ICON FIXES SUMMARY ===\n")
for fix in fixes:
    print(fix)

total_fixed = len([f for f in fixes if f.startswith("✅")])
print(f"\n🎉 Total icons fixed: {total_fixed}/{len(fixes)}")
