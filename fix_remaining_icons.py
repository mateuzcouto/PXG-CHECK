#!/usr/bin/env python3
# Fix remaining icons - boss icons and UI labels

import re

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== FIXING REMAINING ICONS ===\n")

fixes = []

# 1. Boss icons - Magcargo
content_new = re.sub(
    r"('Magcargo':\s*\{\s*key:\s*'boss16',\s*storageKey:\s*'boss16',\s*emoji:\s*')[^']*(')",
    r"\1🌋\2",
    content
)
if content_new != content:
    fixes.append("✅ Magcargo emoji fixed")
    content = content_new

content_new = re.sub(
    r"(icon:\s*')[^']*(',\s*danger:\s*'⚡ CrÁ­tico',\s*energy:\s*'VERMELHA')",
    r"\1🌋\2",
    content
)
if content_new != content:
    fixes.append("✅ Magcargo icon fixed") 
    content = content_new

# Tyranitar
content_new = re.sub(
    r"('Tyranitar':\s*\{\s*key:\s*'boss20',\s*storageKey:\s*'boss20',\s*emoji:\s*')[^']*(')",
    r"\1🪨\2",
    content
)
if content_new != content:
    fixes.append("✅ Tyranitar emoji fixed")
    content = content_new

# Dragonair
content_new = re.sub(
    r"('Dragonair':\s*\{\s*key:\s*'boss12',\s*storageKey:\s*'boss12',\s*emoji:\s*')[^']*(')",
    r"\1🐉\2",
    content
)
if content_new != content:
    fixes.append("✅ Dragonair emoji fixed")
    content = content_new

# Mamoswine
content_new = re.sub(
    r"('Mamoswine':\s*\{\s*key:\s*'boss23',\s*storageKey:\s*'boss23',\s*emoji:\s*')[^']*(')",
    r"\1❄️\2",
    content
)
if content_new != content:
    fixes.append("✅ Mamoswine emoji fixed")
    content = content_new

# 2. UI icons - Fishing label
content_new = re.sub(
    r"(<label[^>]*>)📱[^<]*NÁ­vel de Pesca",
    r"\1🎣 Nível de Pesca",
    content
)
if content_new != content:
    fixes.append("✅ Fishing level label fixed")
    content = content_new

# Also try other variations
content_new = re.sub(
    r"📱£\s*(?:NÁ­vel|Nível)",
    "🎣 Nível",
    content
)
if content_new != content:
    fixes.append("✅ Fishing alt pattern fixed")
    content = content_new

# Pokémon Caught label
content_new = re.sub(
    r"📱¯\s*Pokémon",
    "🎪 Pokémon",
    content
)
if content_new != content:
    fixes.append("✅ Pokémon caught label fixed")
    content = content_new

# Clan label - Clã
content_new = re.sub(
    r"Cl✓",
    "🏰 Clã",
    content
)
if content_new != content:
    fixes.append("✅ Clan label fixed")
    content = content_new

# Clan icon in dropdown (current-clan-icon)
content_new = re.sub(
    r'(<span[^>]*id="current-clan-icon"[^>]*>)📱(<\/span>)',
    r'\1🔴\2',
    content
)
if content_new != content:
    fixes.append("✅ Current clan icon fixed")
    content = content_new

# 3. Banner spinning icon
content_new = re.sub(
    r'(<span class="pokeball-banner-icon">)📱(<\/span>)',
    r'\1🔴\2',
    content
)
if content_new != content:
    fixes.append("✅ Banner spinning icon fixed")
    content = content_new

# Write file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

for fix in fixes:
    print(fix)

print(f"\n🎉 Total remaining fixes: {len(fixes)}")
