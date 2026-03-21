#!/usr/bin/env python3
# Detailed byte analysis for remaining patterns

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

print("=== DETAILED ANALYSIS OF REMAINING CORRUPTED PATTERNS ===\n")

# Find specific line contexts
patterns_to_find = [
    (b"boss-threat", "Threat pattern location"),
    (b"TIPO:", "Type indicator location"),
    (b"COMBATE INICIA", "Combat text location"),
    (b"PREPARE-SE", "Prepare text location"),
]

for pattern, desc in patterns_to_find:
    idx = content.find(pattern)
    if idx != -1:
        print(f"Found '{desc}' (pattern: {pattern.decode('utf-8', errors='ignore')}) at {idx}")
        start = max(0, idx - 100)
        end = min(len(content), idx + 150)
        
        snippet = content[start:end]
        print(f"  HEX: {snippet.hex()}")
        print(f"  DECODED: {snippet.decode('utf-8', errors='replace')}\n")

# Look for â pattern (UTF-8: \xc3\xa2)
print("=== SEARCHING FOR 'â' SEQUENCES ===\n")
a_circumflex = b'\xc3\xa2'  # â in UTF-8

# Find all occurrences
index = 0
occurrences = []
while True:
    idx = content.find(a_circumflex, index)
    if idx == -1:
        break
    
    # Get context
    start = max(0, idx - 50)
    end = min(len(content), idx + 100)
    context = content[start:end]
    
    context_str = context.decode('utf-8', errors='replace')
    occurrences.append((idx, context_str))
    index = idx + 1

print(f"Found {len(occurrences)} occurrences of 'â' (\xc3\xa2):")
for i, (idx, context) in enumerate(occurrences[:10]):  # Show first 10
    print(f"\n  Occurrence {i+1} at byte {idx}:")
    print(f"    Context: {context.strip()[:80]}")

# Look for specific byte patterns after â
print("\n\n=== ANALYZING BYTES AFTER 'â' ===\n")

for i in range(len(occurrences[:5])):
    idx = occurrences[i][0]
    # Skip the â bytes (2 bytes) and look at what comes next
    next_bytes = content[idx+2:idx+10]
    print(f"After 'â' (byte {idx}): {next_bytes.hex()} = {repr(next_bytes)}")
    print(f"  As text: {next_bytes.decode('utf-8', errors='replace')}")
