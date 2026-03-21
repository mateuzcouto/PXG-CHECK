#!/usr/bin/env python3
# Final fix for 📱ª pattern

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the emoji combination
original_count = content.count('📱ª')
content = content.replace('📱ª', '💪')
new_count = content.count('📱ª')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Fixed 📱ª → 💪: {original_count - new_count}x")
print(f"✅ File saved with UTF-8 encoding")
