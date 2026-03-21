#!/usr/bin/env python3
# Analyze and fix the remaining corrupted patterns

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

print("=== ANALYZING REMAINING PATTERNS ===\n")

# Pattern 1: Find "boss-threat" context and see what's before it
boss_threat_idx = content.find(b'id="boss-threat"')
if boss_threat_idx != -1:
    # Get 100 bytes before it
    start = max(0, boss_threat_idx - 100)
    snippet = content[start:boss_threat_idx]
    
    print(f"Bytes before 'boss-threat':\n  HEX: {snippet.hex()}")
    print(f"  REPR: {repr(snippet)}\n")
    print(f"  TEXT: {snippet.decode('utf-8', errors='replace')}\n")
    
    # Now let's find the specific corrupted pattern before this
    # It should be something like "â i¸"
    pattern_to_find = snippet[max(0, len(snippet) - 50):]
    print(f"Last 50 bytes: {repr(pattern_to_find)}\n")

# Pattern 2: Find and analyze "PREPARE-SE SEMPRE"
prepare_idx = content.find(b'PREPARE-SE SEMPRE')
if prepare_idx != -1:
    # Get 100 bytes before it
    start = max(0, prepare_idx - 100)
    snippet = content[start:prepare_idx]
    
    print(f"Bytes before 'PREPARE-SE SEMPRE':\n  HEX: {snippet[-50:].hex()}")
    print(f"  REPR: {repr(snippet[-50:])}\n")
    print(f"  TEXT: {snippet[-50:].decode('utf-8', errors='replace')}\n")

print("\n=== SEARCHING FOR EXACT PATTERN STRINGS ===\n")

# Try to find variations
variations = [
    b'\xc3\xa2 i\xc2\xb8\xc2\x8f',  # â i¸¯
    b'\xc3\xa2\xc2\x9a\xc2\xa0i\xc2\xb8\xc2\x8f',  # â (with extra complexity) i¸¯
    b'i\xc2\xb8\xc2\x8f',  # Just i¸¯
    b'\xc2\xb8\xc2\x8f',  # Just ¸¯
]

for var in variations:
    count = content.count(var)
    if count > 0:
        print(f"Found {repr(var)}: {count}x")
        idx = content.find(var)
        snippet = content[max(0, idx-30):min(len(content), idx+60)]
        print(f"  Context: {snippet.decode('utf-8', errors='replace')}\n")

# Look for 📱ª pattern
mobile_apple = '📱'.encode('utf-8') + b'\xc2\xaa'  # 📱ª
count = content.count(mobile_apple)
print(f"\nFound 📱ª pattern: {count}x")

mobile_only = '📱'.encode('utf-8')
count2 = content.count(mobile_only)
print(f"Found 📱 pattern only: {count2}x")
