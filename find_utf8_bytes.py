#!/usr/bin/env python3
# Find and analyze the \x9f\x92 bytes

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

pattern = b'\x9f\x92'
count = content.count(pattern)

print(f"Found {count} instances of \\x9f\\x92\n")

# Find each occurrence and show context
index = 0
for occurrence in range(min(count, 10)):  # Show first 10
    index = content.find(pattern, index)
    if index == -1:
        break
    
    start = max(0, index - 40)
    end = min(len(content), index + 40)
    
    snippet = content[start:end]
    print(f"Occurrence {occurrence + 1} at byte {index}:")
    print(f"  Bytes: {snippet.hex()}")
    print(f"  Context: {snippet.decode('utf-8', errors='replace')}\n")
    
    index += 1

# These bytes appear to be UTF-8 artifacts
# \x9f\x92 is part of the sequence \xf0\x9f\x92 which is one of the emoji prefix bytes
# If these are standalone, they're corruption
print("=" * 50)
print("These appear to be leftover emoji UTF-8 bytes")
print("They should be removed or replaced with proper emojis")
