#!/usr/bin/env python3
# Remove all stray ª characters from the file since they shouldn't be there

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

original_count = content.count('ª')
print(f"⚠️ Found {original_count} instances of 'ª'")

# Remove all ª
content = content.replace('ª', '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

new_count = content.count('ª')
removed = original_count - new_count

print(f"✅ Removed {removed} instances of 'ª'")
print(f"✅ File saved")
