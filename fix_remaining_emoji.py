#!/usr/bin/env python3
# Final emoji corruption fixes using exact byte sequences found

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

fixes_made = []

# Pattern 1: â i¸¯ = \xc3\xa2\xc2\x9a\xc2\xa0i\xc2\xb8\xc2\x8f (17x)
pattern1 = b'\xc3\xa2\xc2\x9a\xc2\xa0i\xc2\xb8\xc2\x8f'
replacement1 = '⚡'.encode('utf-8')
count1 = content.count(pattern1)
if count1 > 0:
    content = content.replace(pattern1, replacement1)
    fixes_made.append(f"✅ Threat warning (â i¸¯ → ⚡): {count1}x")

# Pattern 2: i¸¯ = \xc2\xb8\xc2\x8f alone (37x)
# But we need to be careful - this appears after emojis like 📱i¸¯
# Context shows: "📱i¸</span>" should become "📱</span>" ONLY
# But also elsewhere like "ObservaÁ§Á£o" which shouldn't be touched
# 
# Let's be surgical: Only replace when it follows emoji bytes
# Emoji pattern: \xf0\x9f (start of UTF-8 emoji)

pattern2_long = b'\xf0\x9f' # Any emoji start
pattern2_suffix = b'i\xc2\xb8\xc2\x8f'

# Find and replace safely
import re

# Actually, let's look for the specific context: >\xf0\x9f...\xc2\xb8\xc2\x8f<
# Which means: >emoji...i¸¯<

# Let's do this more carefully with a regex-like approach
# Find all occurrences of the suffix and check what's before
pos = 0
count2_safe = 0
while True:
    pos = content.find(pattern2_suffix, pos)
    if pos == -1:
        break
    
    # Check what's before (look back for emoji or ">" which closes a tag or text content)
    # If 10+ bytes back we find emoji bytes, it's probably our target
    check_back = content[max(0, pos-30):pos]
    
    # If there's an emoji (f0 9f) or text content (not inside HTML attributes), replace it
    if b'\xf0\x9f' in check_back or (b'>' in check_back and b'=' not in check_back[-10:]):
        # This looks like it's in content, not in an attribute
        # Replace just this suffix
        content = content[:pos] + content[pos+len(pattern2_suffix):]
        count2_safe += 1
    else:
        pos += 1

if count2_safe > 0:
    fixes_made.append(f"✅ Icon suffix cleanup (i¸¯ removed): {count2_safe}x")

# Write back
with open(file_path, 'wb') as f:
    f.write(content)

# Print results
print("=== FINAL EMOJI CORRUPTION FIXES ===\n")
for fix in fixes_made:
    print(fix)

total = sum(int(line.split(': ')[1].split('x')[0]) for line in fixes_made)
print(f"\n🎉 Total fixes applied: {total}")
