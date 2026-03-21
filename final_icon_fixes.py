#!/usr/bin/env python3
# Fix remaining issues

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

fixes = []

# Check for remaining 📱 in clan/world definitions
fixes_dict = {
    'wingeon: { name: "Wingeon", color: "bg-sky-400", icon: "📱"': 
        'wingeon: { name: "Wingeon", color: "bg-sky-400", icon: "🌪️"',
    'icon: "📱", border: "border-sky-300", text: "text-sky-300"':
        'icon: "🌪️", border: "border-sky-300", text: "text-sky-300"',
}

for old, new in fixes_dict.items():
    if old in content:
        content = content.replace(old, new)
        fixes.append(f"✅ Fixed: {old[:40]}...")

# Also check UI remaining issues  
ui_fixes = {
    '📱 Pokémon': '🎪 Pokémon',
    '📱 Pesca': '🎣 Pesca',
    'span class="bg-red-600 clan-badge-small" id="current-clan-icon">📱<': 'span class="bg-red-600 clan-badge-small" id="current-clan-icon">🔴<',
}

for old, new in ui_fixes.items():
    if old in content:
        content = content.replace(old, new)
        fixes.append(f"✅ Fixed UI: {old[:40]}...")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=== FINAL ICON FIXES ===\n")
for fix in fixes:
    print(fix)

if len(fixes) == 0:
    print("✅ All icons are correct!")
else:
    print(f"\n🎉 Total fixes: {len(fixes)}")
