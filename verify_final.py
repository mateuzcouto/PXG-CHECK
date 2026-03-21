#!/usr/bin/env python3
# Simple final verification - count corrupted patterns

file_path = "src/index.html"

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# List of patterns that indicate corruption
corruption_patterns = [
    ('âi¸', 'Boss emoji corruption'),
    ('â ', 'Threat indicator corruption'),
    ('â¡', 'Alert emoji corruption'),
    ('ðª', 'Data emoji corruption'),
    ('\x9f\x92', 'UTF-8 byte corruption'),
    ('ª', 'Stray superscript a'),
]

print("=== FINAL CORRUPTION CHECK ===\n")

total_corruptions_found = 0
for pattern, description in corruption_patterns:
    count = content.count(pattern)
    if count > 0:
        print(f"⚠️ Found {count}x {description} (pattern: {repr(pattern)})")
        total_corruptions_found += count
    else:
        print(f"✅ {description} - FIXED")

print(f"\n{'='*40}")
if total_corruptions_found == 0:
    print("✅ FILE IS CLEAN - No corrupted patterns found!")
else:
    print(f"⚠️ {total_corruptions_found} potential corruption issues remain")

print(f"{'='*40}")
print("\nCounted emojis in boss alert section:")

# Check specific sections
boss_alert = content[content.find('boss-pokeball-icon'):content.find('ENTENDI') + 100]
emoji_count = sum(1 for c in boss_alert if ord(c) > 127000 and ord(c) < 128000)  # Rough emoji range
print(f"  Emojis detected: {len([c for c in boss_alert if ord(c) > 127000])}")

# Check for specific correct emojis
correct_emojis = {
    '🔴': 'Red pokéball',
    '🎪': 'Circus tent (boss)',
    '⚡': 'Lightning (threat)',
    '💪': 'Muscle (prepare)',
    '✓': 'Checkmark',
}

print("\nCorrect emojis found:")
for emoji, desc in correct_emojis.items():
    count = content.count(emoji)
    if count > 0:
        print(f"  {emoji} ({desc}): {count}x")
