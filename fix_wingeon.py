#!/usr/bin/env python3
# Final fix for Wingeon

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Simply replace the Wingeon icon
content = content.replace(
    'icon: "📱", border: "border-sky-300"',
    'icon: "🌪️", border: "border-sky-300"'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Wingeon icon fixed (🌪️)")
