#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar o padrão EXATO de "Á s"
"""

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Procurar a linha com "Próx. Evento" e "s"
for i, line in enumerate(lines, 1):
    if 'Próx. Evento' in line and 's' in line:
        print(f"Linha {i}: {repr(line)}")
        print(f"Conteúdo (visível): {line.strip()}")
        
        # Encontrar a posição do problema
        if 'Á s' in line:
            print("ENCONTRADO: Padrão 'Á s'")
            print("Códigos de caractere:")
            for char in line.strip():
                print(f"  '{char}' = U+{ord(char):04X} ({ord(char.encode('utf-8', errors='replace').hex())})")
        else:
            print("NÃO ENCONTRADO: Padrão 'Á s'")
            print("\nMostrando caracteres individuais perto de 'Próx':")
            idx = line.find('Próx')
            if idx != -1:
                section = line[idx:idx+50]
                for j, char in enumerate(section):
                    print(f"  Pos {j}: '{char}' = U+{ord(char):04X}")
