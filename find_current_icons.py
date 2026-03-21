#!/usr/bin/env python3
# Fix icons using byte-level replacements

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

fixes_made = []

# World icons - use byte patterns
# Aurora: c3a2c298c28169c2b8c28f = 'âi¸' complex form
aurora_bad = b'\xc3\xa2\xc2\x98\xc2\x81i\xc2\xb8\xc2\x8f'
aurora_good = '🌌'.encode('utf-8')

if aurora_bad in content:
    content = content.replace(aurora_bad, aurora_good)
    fixes_made.append("✅ Aurora icon fixed (complex) (1x)")

# Check for simpler aurora pattern: just 'âi¸'
aurora_simple = b'\xc3\xa2i\xc2\xb8\xc2\x8f'
if aurora_simple in content:
    content = content.replace(aurora_simple, aurora_good)
    fixes_made.append("✅ Aurora icon fixed (simple)")

# Steel icon - same bad pattern as Aurora
steel_bad = b'\xc3\xa2i\xc2\xb8\xc2\x8f'
steel_good = '⚙️'.encode('utf-8')

count_steel = content.count(steel_bad)
if count_steel > 0:
    # Replace only first 2 occurrences (Aurora and Steel)
    # Actually, let's replace in context - if it's in a color definition
    # Split by line and replace in specific lines
    lines = content.split(b'\n')
    new_lines = []
    line_counter = 0
    for line in lines:
        if bg_pattern in line and line_counter >= 1:  #  Steel comes after Aurora
            if steel_bad in line:
                line = line.replace(steel_bad, steel_good)
                fixes_made.append("✅ Steel icon fixed")
                line_counter += 1
        new_lines.append(line)
    content = b'\n'.join(new_lines)

# Simpler approach: do string-based replace on decoded content:
with open(file_path, 'r', encoding='utf-8') as f:
    text_content = f.read()

text_fixes = [
    # Omega - has strange emoji bytes, let's just look for 'Omega': { ... icon:'
    # and replace the icon pattern
    
    # For now let's find and fix by searching the actual text patterns
]

# Replace using text mode
replacements = [
    # Check if these strings exist first, then replace
]

# Actually, let me just try to find what's in the file now
print("=== CURRENT ICON STATUS ===\n")

# World icons
if "'Aurora':" in text_content and "'text-green-400'" in text_content:
    aurora_start = text_content.find("'Aurora': {")
    aurora_end = text_content.find("},", aurora_start)
    print(f"Aurora line: {text_content[aurora_start:aurora_end+2]}")

if "'Steel':" in text_content:
    steel_start = text_content.find("'Steel': {")
    steel_end = text_content.find("},", steel_start)
    print(f"Steel line: {text_content[steel_start:steel_end+2]}")

# Clan icons
if "volcanic:" in text_content:
    volcanic_start = text_content.find("volcanic: {")
    volcanic_end = text_content.find("},", volcanic_start)
    print(f"Volcanic line: {text_content[volcanic_start:volcanic_end+2]}")

print("\nFile is ready for targeted fixes")
