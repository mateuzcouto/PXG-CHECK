#!/usr/bin/env python3
# Fix the corrupted emoji sequence 📱\x9f\x92ª

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

# The pattern is: 📱 (f0 9f 93 b1 in UTF-8) + \x9f\x92 + ª (c2 aa in UTF-8)
# Which is: f0 9f 93 b1 9f 92 c2 aa

mobile_emoji_full = b'\xf0\x9f\x93\xb1\x9f\x92\xc2\xaa'  # 📱\x9f\x92ª
replacement = '💪'.encode('utf-8')

count = content.count(mobile_emoji_full)
if count > 0:
    content = content.replace(mobile_emoji_full, replacement)
    print(f"✅ Fixed corrupted emoji (📱\\x9f\\x92ª → 💪): {count}x")
else:
    # Try without the ª part
    mobile_emoji_partial = b'\xf0\x9f\x93\xb1\x9f\x92'  # 📱\x9f\x92
    count2 = content.count(mobile_emoji_partial)
    if count2 > 0:
        content = content.replace(mobile_emoji_partial, replacement)
        print(f"✅ Fixed partial corrupted emoji (📱\\x9f\\x92 → 💪): {count2}x")
    else:
        print("❌ Pattern not found")

with open(file_path, 'wb') as f:
    f.write(content)

print("✅ File saved with corrections")
