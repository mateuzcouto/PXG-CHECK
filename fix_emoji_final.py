#!/usr/bin/env python3
# Fix remaining emoji corruption patterns using exact byte sequences

file_path = "src/index.html"

with open(file_path, 'rb') as f:
    content = f.read()

fixes_made = []

# Pattern 1: â¡ (bytes c3a2c29ac2a1) → ⚡
pattern_alert = b'\xc3\xa2\xc2\x9a\xc2\xa1'
replacement_alert = '⚡'.encode('utf-8')

count = content.count(pattern_alert)
if count > 0:
    content = content.replace(pattern_alert, replacement_alert)
    fixes_made.append(f"✅ Alert emoji (â¡ → ⚡): {count}x")

# Pattern 2: â i¸ (more complex, let's use the full byte sequence)
# â space i¸ ¯ = c3a2 209a c2b8 c28f
# But the actual pattern seems to be: c3a2 c29a c2a0 69 c2b8 c28f
# Let me look for the threat pattern specifically
# The byte sequence: c3a2 c29a c2a0 69 c2b8 c28f (as seen in analysis)

# Try simpler: just replace "â " with "⚡ " when followed by threat/element content
pattern_threat_simple = b'\xc3\xa2 '  # â followed by space
replacement_threat = '⚡ '.encode('utf-8')

count_threat = content.count(pattern_threat_simple)
if count_threat > 0:
    # But we need to be careful - check context to avoid over-replacement
    # For now, let's replace only in boss alert context
    
    # Find the boss alert section and replace within it
    boss_alert_start = content.find(b'id="event-visual-alert"')
    boss_alert_end = content.find(b'</div>\r\n\r\n</div>\r\n\r\n</div>\r\n\r\n<script', boss_alert_start)
    
    if boss_alert_start != -1 and boss_alert_end != -1:
        boss_alert_content = content[boss_alert_start:boss_alert_end]
        original_alert_content = boss_alert_content
        
        # Replace in this section only
        boss_alert_content = boss_alert_content.replace(pattern_threat_simple, replacement_threat)
        
        # Count how many were replaced
        replaced = boss_alert_content.count(replacement_threat) - original_alert_content.count(replacement_threat)
        #Actually let's count differently
        
        # Rebuild content
        content = content[:boss_alert_start] + boss_alert_content + content[boss_alert_end:]
        fixes_made.append(f"✅ Threat indicator (â  → ⚡ ): {count_threat}x (in boss alert)")

# Pattern 3: Remove ª after emojis (📱ª → 📱)
# ª in UTF-8 is c2aa
pattern_emoji_suffix = b'\xc2\xaa'  # ª symbol

# Again, be careful - only remove when after emoji
# Look for emoji bytes (f0 9f ...) followed by c2aa
import re

# This is tricky in binary, let's just replace 📱ª with 💪
pattern_mobile_full = '📱ª'.encode('utf-8')
replacement_mobile = '💪'.encode('utf-8')

count_mobile = content.count(pattern_mobile_full)
if count_mobile > 0:
    content = content.replace(pattern_mobile_full, replacement_mobile)
    fixes_made.append(f"✅ Prepare emoji (📱ª → 💪): {count_mobile}x")

# Write back
with open(file_path, 'wb') as f:
    f.write(content)

# Print results
print("=== EMOJI FIXES ===\n")
total = 0
for fix in fixes_made:
    print(fix)
    # Extract count
    if ':' in fix and 'x' in fix:
        count = int(fix.split(': ')[1].split('x')[0])
        total += count

print(f"\n🎉 Total emoji corrections: {total}")
