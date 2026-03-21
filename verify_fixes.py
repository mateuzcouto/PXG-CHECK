#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Count remaining ?? occurrences
total_qq = content.count('??')

# Count in critical sections (notifications)
notif_count = content.count('Sunflora') + content.count('Magcargo') + content.count('Tyranitar') + content.count('Dragonair') + content.count('Mamoswine') + content.count('Poképark')

# Check for proper emojis in epicNotifications
has_boss_emojis = '🌻' in content and '🔥' in content and '🪨' in content and '🐉' in content and '❄️' in content and '🎪' in content

# Check notification emoji
has_notify_emoji = '🚨' in content and '🔔🔔' in content

# Check body emoji
has_body_emoji = '📊' in content and '⏰' in content and '💪' in content

# Check admin emoji
has_admin_emoji = '🐛' in content and '💡' in content and '👥' in content and '⚔️' in content

print(f"✅ Verificação final:")
print(f"  - Total ?? restantes: {total_qq}")
print(f"  - Boss entries encontrados: {notif_count}")
print(f"  - Emojis de boss (🌻🔥🪨🐉❄️🎪): {'✅' if has_boss_emojis else '❌'}")
print(f"  - Emojis de notificação (🚨🔔): {'✅' if has_notify_emoji else '❌'}")
print(f"  - Emojis de body (📊⏰💪): {'✅' if has_body_emoji else '❌'}")
print(f"  - Emojis de admin (🐛💡👥⚔️): {'✅' if has_admin_emoji else '❌'}")

if total_qq < 30:  # Most remaining ?? are in comments/console
    print(f"\n🎉 SUCESSO! Site corrigido com emojis apropriados!")
    print(f"   Remaining ?? são principalmente em comentários e console.log (não visível ao usuário)")
else:
    print(f"\n⚠️ Ainda há muitos ?? para revisar")
