#!/usr/bin/env python3
# Fix Wingeon with more precision

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find Wingeon section
wingeon_idx = content.find('wingeon: { name: "Wingeon"')
if wingeon_idx != -1:
    # Find the next closing brace
    close_idx = content.find('},', wingeon_idx)
    wingeon_def = content[wingeon_idx:close_idx+2]
    
    # Check if it has the 📱 icon
    if 'icon: "📱"' in wingeon_def:
        new_def = wingeon_def.replace('icon: "📱"', 'icon: "🌪️"')
        content = content[:wingeon_idx] + new_def + content[close_idx+2:]
        print("✅ Wingeon icon fixed successfully")
    else:
        print("ℹ️ Wingeon already has correct icon or pattern not found")
        print(f"Current: {wingeon_def}")
else:
    print("❌ Wingeon definition not found")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
