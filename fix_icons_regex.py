#!/usr/bin/env python3
# Direct Python fix for all icons using regex

import re

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== FIXING ALL ICONS ===\n")

fixes = []

# 1. World color icons
# Replace within color definitions - let's use regex

# Aurora pattern - find 'Aurora': {... icon: '... } and replace the icon
content_new = re.sub(
    r"('Aurora':\s*\{\s*text:\s*'text-green-400',\s*icon:\s*')[^']+(')",
    r"\1🌌\2",
    content
)
if content_new != content:
    fixes.append("✅ Aurora icon fixed")
    content = content_new

# Omega icon 
content_new = re.sub(
    r"('Omega':\s*\{\s*text:\s*'text-red-600',\s*icon:\s*')[^']+(')",
    r"\1❤️\2",
    content
)
if content_new != content:
    fixes.append("✅ O mega icon fixed")
    content = content_new

# Emerald icon
content_new = re.sub(
    r"('Emerald':\s*\{\s*text:\s*'text-emerald-400',\s*icon:\s*')[^']+(')",
    r"\1💎\2",
    content
)
if content_new != content:
    fixes.append("✅ Emerald icon fixed")
    content = content_new

# Cosmic icon
content_new = re.sub(
    r"('Cosmic':\s*\{\s*text:\s*'text-purple-500',\s*icon:\s*')[^']+(')",
    r"\1⭐\2",
    content
)
if content_new != content:
    fixes.append("✅ Cosmic icon fixed")
    content = content_new

# Steel icon
content_new = re.sub(
    r"('Steel':\s*\{\s*text:\s*'text-slate-400',\s*icon:\s*')[^']+(')",
    r"\1⚙️\2",
    content
)
if content_new != content:
    fixes.append("✅ Steel icon fixed")
    content = content_new

# Wind icon
content_new = re.sub(
    r"('Wind':\s*\{\s*text:\s*'text-cyan-400',\s*icon:\s*')[^']+(')",
    r"\1💨\2",
    content
)
if content_new != content:
    fixes.append("✅ Wind icon fixed")
    content = content_new

# Lunar icon
content_new = re.sub(
    r"('Lunar':\s*\{\s*text:\s*'text-indigo-300',\s*icon:\s*')[^']+(')",
    r"\1🌙\2",
    content
)
if content_new != content:
    fixes.append("✅ Lunar icon fixed")
    content = content_new

# Ocean icon
content_new = re.sub(
    r"('Ocean':\s*\{\s*text:\s*'text-blue-500',\s*icon:\s*')[^']+(')",
    r"\1🌊\2",
    content
)
if content_new != content:
    fixes.append("✅ Ocean icon fixed")
    content = content_new

# Flame icon
content_new = re.sub(
    r"('Flame':\s*\{\s*text:\s*'text-orange-500',\s*icon:\s*')[^']+(')",
    r"\1🔥\2",
    content
)
if content_new != content:
    fixes.append("✅ Flame icon fixed")
    content = content_new

# Rainbow icon
content_new = re.sub(
    r"('Rainbow':\s*\{\s*text:\s*'text-pink-400',\s*icon:\s*')[^']+(')",
    r"\1🌈\2",
    content
)
if content_new != content:
    fixes.append("✅ Rainbow icon fixed")
    content = content_new

# 2. Clan icons

# Volcanic
content_new = re.sub(
    r'(volcanic:\s*\{\s*name:\s*"Volcanic",\s*color:\s*"bg-red-600",\s*icon:\s*")[^"]*(")',
    r'\1🔴\2',
    content
)
if content_new != content:
    fixes.append("✅ Volcanic clan icon fixed")
    content = content_new

# Seavell
content_new = re.sub(
    r'(seavell:\s*\{\s*name:\s*"Seavell",\s*color:\s*"bg-blue-600",\s*icon:\s*")[^"]*(")',
    r'\1🌊\2',
    content  
)
if content_new != content:
    fixes.append("✅ Seavell clan icon fixed")
    content = content_new

# Or ebound
content_new = re.sub(
    r'(orebound:\s*\{\s*name:\s*"Orebound",\s*color:\s*"bg-amber-800",\s*icon:\s*")[^"]*(")',
    r'\1⛏️\2',
    content
)
if content_new != content:
    fixes.append("✅ Orebound clan icon fixed")
    content = content_new

# Wingeon
content_new = re.sub(
    r'(wingeon:\s*\{\s*name:\s*"Wingeon",\s*color:\s*"bg-sky-4 00",\s*icon:\s*")[^"]*(")',
    r'\1🌪️\2',
    content
)
if content_new != content:
    fixes.append("✅ Wingeon clan icon fixed")
    content = content_new

# Naturia
content_new = re.sub(
    r'(naturia:\s*\{\s*name:\s*"Naturia",\s*color:\s*"bg-green-600",\s*icon:\s*")[^"]*(")',
    r'\1🌿\2',
    content
)
if content_new != content:
    fixes.append("✅ Naturia clan icon fixed")
    content = content_new

# Malefic
content_new = re.sub(
    r'(malefic:\s*\{\s*name:\s*"Malefic",\s*color:\s*"bg-purple-700",\s*icon:\s*")[^"]*(")',
    r'\1☠️\2',
    content
)
if content_new != content:
    fixes.append("✅ Malefic clan icon fixed")
    content = content_new

# Psycraft
content_new = re.sub(
    r'(psycraft:\s*\{\s*name:\s*"Psycraft",\s*color:\s*"bg-pink-500",\s*icon:\s*")[^"]*(")',
    r'\1🔮\2',
    content
)
if content_new != content:
    fixes.append("✅ Psycraft clan icon fixed")
    content = content_new

# Ironhard
content_new = re.sub(
    r'(ironhard:\s*\{\s*name:\s*"Ironhard",\s*color:\s*"bg-slate-500",\s*icon:\s*")[^"]*(")',
    r'\1⚙️\2',
    content
)
if content_new != content:
    fixes.append("✅ Ironhard clan icon fixed")
    content = content_new

# 3. Boss icons - using emoji patterns
content_new = re.sub(
    r"('Sunflora':\s*\{\s*key:\s*'boss12',\s*storageKey:\s*'boss12',\s*emoji:\s*')[^']*(')",
    r"\1☀️\2",
    content
)
if content_new != content:
    fixes.append("✅ Sunflora emoji fixed")
    content = content_new

content_new = re.sub(
    r"(icon:\s*')[^']*(',\s*danger:\s*'⚡ CrÁ­tico',\s*energy:\s*'AMARELA')",
    r"\1☀️\2",
    content
)
if content_new != content:
    fixes.append("✅ Sunflora icon fixed")
    content = content_new

# Written file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

for fix in fixes:
    print(fix)

print(f"\n🎉 Total fixes applied: {len(fixes)}")
