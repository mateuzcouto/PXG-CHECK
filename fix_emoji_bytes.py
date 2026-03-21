#!/usr/bin/env python3
# Fix emoji corruption using exact byte sequences

file_path = "src/index.html"

# Read as binary
with open(file_path, 'rb') as f:
    content = f.read()

fixes_made = []

# Boss emoji corruption: âi¸ = bytes \xc3\xa2\xc2\x9a\xc2\x94i\xc2\xb8\xc2\x8f
# This is a corrupted UTF-8 sequence that should be an emoji like 🎪
boss_corrupt = b'\xc3\xa2\xc2\x9a\xc2\x94i\xc2\xb8\xc2\x8f'
boss_emoji = '🎪'.encode('utf-8')

count = content.count(boss_corrupt)
if count > 0:
    content = content.replace(boss_corrupt, boss_emoji)
    fixes_made.append(f"✅ Boss emoji (âi¸ → 🎪): {count}x")

# Alternative pattern without 'i': â j¸ ¯
# Risk: â is actually \xc3\xa2 (UTF-8 for â)
# When decoded as UTF-8 and shown as text, it shows as "â"
threat_corrupt = b'\xc3\xa2 '  # Just the 'â ' part
if threat_corrupt in content:
    count_threat = content.count(threat_corrupt)
    # Replace with ⚡
    content = content.replace(threat_corrupt, '⚡'.encode('utf-8'))
    fixes_made.append(f"✅ Threat emoji (â → ⚡): {count_threat}x")

# Look for 📱ª pattern
# 📱 encodes to its UTF-8 bytes, ª encodes to \xc2\xaa
mobile_emoji_bytes = '📱'.encode('utf-8')
emoji_a_bytes = b'\xc2\xaa'  # ª symbol in UTF-8

# Search for the pattern around line 3250
pattern_to_find = b'\xf0\x9f\x93\xb1\xc2\xaa'  # 📱ª in UTF-8
if pattern_to_find in content:
    count_mobile = content.count(pattern_to_find)
    content = content.replace(pattern_to_find, '💪'.encode('utf-8'))
    fixes_made.append(f"✅ Mobile emoji (📱ª → 💪): {count_mobile}x")

# Also try alternate: ðª pattern (ð = U+00F0 in Latin-1 = \xf0, rendered)
# When this is displayed, it might show as "ð"
# Let's look for \xc3\xb0 (Å¿ - UTF-8 encoded ð)
data_corrupt = b'\xc3\xb0\xc2\xaa'  # ðª in mixed encoding
if data_corrupt in content:
    count_data = content.count(data_corrupt)
    content = content.replace(data_corrupt, '💪'.encode('utf-8'))
    fixes_made.append(f"✅ Data emoji (ðª → 💪): {count_data}x")

# Simple replacements for â¡ pattern
alt_corrupt = b'\xc3\xa2\xc2\xa1'  # â¡ in UTF-8
if alt_corrupt in content:
    count_alt = content.count(alt_corrupt)
    content = content.replace(alt_corrupt, '⚡'.encode('utf-8'))
    fixes_made.append(f"✅ Lightning emoji (â¡ → ⚡): {count_alt}x")

# Write back
with open(file_path, 'wb') as f:
    f.write(content)

# Print results
total = sum(int(line.split(': ')[1].split('x')[0]) for line in fixes_made if 'x' in line)
for fix in fixes_made:
    print(fix)

print(f"\n🎉 Total emoji corrections: {total}")
