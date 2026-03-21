#!/usr/bin/env python3
# Fix Wingeon using exact byte replacement

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

# Wingeon icon pattern: 📱 followed by corrupted bytes
# Hex: f0 9f 93 b1 c2 9f c2 8c
bad_pattern = b'\xf0\x9f\x93\xb1\xc2\x9f\xc2\x8c'
good_emoji = '🌪️'.encode('utf-8')  # f0 9f 8c aa

count = content.count(bad_pattern)
if count > 0:
    content = content.replace(bad_pattern, good_emoji)
    print(f"✅ Fixed Wingeon icon: Found and replaced {count}x")
else:
    print("ℹ️ Pattern not found")
    # Try alternative - just find the icon line
    if b'wingeon: { name: "Wingeon"' in content:
        print("ℹ️ Wingeon definition found, trying direct replacement...")
        # Find and replace in the wingeon section
        idx = content.find(b'wingeon: { name: "Wingeon"')
        end_idx = content.find(b'},', idx)
        wingeon_section = content[idx:end_idx+2]
        
        # Replace any mobile emoji in this section
        newwingeon_section = wingeon_section.replace(b'\xf0\x9f\x93\xb1', good_emoji)
        content = content[:idx] + newwingeon_section + content[end_idx+2:]
        print("✅ Wingeon icon replaced using section replacement")

with open(file_path, 'wb') as f:
    f.write(content)

print("✅ File saved")
