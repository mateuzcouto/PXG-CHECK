#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substituição FINAL em nível de bytes UTF-8
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

# Ler arquivo como bytes
with open(filepath, 'rb') as f:
    content_bytes = f.read()

# Mostrar alguns bytes para debug
print(f"Conteúdo antes (primeiros 100 bytes): {content_bytes[:100]}")

# Fazer a substituição em nível de bytes UTF-8
# "Á s" = C381 (UTF-8 para Á) + 20 (espaço) + 73 (s)
# Vamos substituir por "às " = C3A0 (UTF-8 para à) + 73 (s) + 20 (espaço)

# Primeiro tenta encontrar o padrão "Á s"
bad_bytes = b'\xc3\x81 s'  # "Á s" em UTF-8
good_bytes = b'\xc3\xa0s '  # "às " em UTF-8

print(f"\nProcurando por: {bad_bytes}")
print(f"Encontrados: {content_bytes.count(bad_bytes)} ocorrências")

if bad_bytes in content_bytes:
    content_bytes = content_bytes.replace(bad_bytes, good_bytes)
    print(f"Substituído para: {good_bytes}")

# Re-salvar como bytes
with open(filepath, 'wb') as f:
    f.write(content_bytes)

print("\n✅ Arquivo corrigido em nível de bytes UTF-8!")
