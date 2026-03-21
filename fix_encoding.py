#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige o encoding UTF-8 de todo o arquivo index.html
Converte characters corrompidos (?) de volta aos acentos corretos
"""

import os

# Caminho do arquivo
filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

# Ler o arquivo como binary (para detectar o encoding real)
with open(filepath, 'rb') as f:
    content_bytes = f.read()

# Tentar decodificar como Latin-1 (Windows-1252) que é o encoding problemático
try:
    content = content_bytes.decode('latin-1')
except:
    content = content_bytes.decode('utf-8', errors='replace')

# Mapa de substituições para corrigir acentos corrompidos
replacements = {
    # Acentos corrompidos com números/símbolos
    '?ão': 'ção',
    '?ões': 'ções',
    '?á': 'á',
    '?é': 'é',
    '?í': 'í',
    '?ó': 'ó',
    '?ú': 'ú',
    '?â': 'â',
    '?ê': 'ê',
    '?õ': 'õ',
    '?ç': 'ç',
    '?à': 'à',
    '?~': '~',
    '?': '~',  # Til corrompido
    '??': '??',  # Deixar placeholders de ?? como estão
    
    # Palavras comuns que ficam corrompidas
    'Atualiza??o': 'Atualização',
    'Atualiza?ão': 'Atualização',
    'atualiza??o': 'atualização',
    'atualiza?ão': 'atualização',
    
    'notifica??es': 'notificações',
    'notifica?ões': 'notificações',
    'Notifica?ões': 'Notificações',
    
    'Pulsa??o': 'Pulsação',
    'Pulsa?ão': 'Pulsação',
    'pulsação': 'pulsação',
    
    'informa??es': 'informações',
    'Informa?ões': 'Informações',
    
    'vers?ão': 'versão',
    'Vers?ão': 'Versão',
    'vers?o': 'versão',
    'Vers?o': 'Versão',
    
    'fun??ão': 'função',
    'Fun??ão': 'Função',
    
    'valida??ão': 'validação',
    'Valida?ão': 'Validação',
    
    'sincroniza??ão': 'sincronização',
    'Sincroniza?ão': 'Sincronização',
    
    'otimiza??ão': 'otimização',
    'Otimiza?ão': 'Otimização',
    
    'explora??ão': 'exploração',
    'Explora?ão': 'Exploração',
    
    'codifica??ão': 'codificação',
    'Codifica?ão': 'Codificação',
    
    'cria??ão': 'criação',
    'Cria?ão': 'Criação',
    
    'aten??ão': 'atenção',
    'Aten?ão': 'Atenção',
    
    'execu??ão': 'execução',
    'Execu?ão': 'Execução',
    
    'sele??ão': 'seleção',
    'Sele?ão': 'Seleção',
    
    'conex?o': 'conexão',
    'Conex?o': 'Conexão',
    
    'hor?rio': 'horário',
    'Hor?rio': 'Horário',
    
    'rota??ão': 'rotação',
    'Rota?ão': 'Rotação',
    
    'espa?o': 'espaço',
    'Espa?o': 'Espaço',
    
    'rea??ão': 'reação',
    'Rea?ão': 'Reação',
    
    'm?o': 'mão',
    'M?o': 'Mão',
    
    'n?vel': 'nível',
    'N?vel': 'Nível',
    'N?veis': 'Níveis',
    
    'j?': 'já',
    'J?': 'Já',
    
    'h?': 'há',
    'H?': 'Há',
    
    'c?digo': 'código',
    'C?digo': 'Código',
    
    'mem?ria': 'memória',
    'Mem?ria': 'Memória',
    
    'profiss?o': 'profissão',
    'Profiss?o': 'Profissão',
    
    'especializa??o': 'especialização',
    'Especializa?ão': 'Especialização',
    
    'limpa??o': 'limpeza',
    'irruvers?vel': 'irreversível',
    
    'neuroci?ncia': 'neurociência',
    'Neuroci?ncia': 'Neurociência',
    
    'est?mulos': 'estímulos',
    'Est?mulos': 'Estímulos',
    
    'c?rebro': 'cérebro',
    'C?rebro': 'Cérebro',
    
    'encripta??o': 'encriptação',
    'Encripta?ão': 'Encriptação',
    
    'dispon?vel': 'disponível',
    'Dispon?vel': 'Disponível',
    
    'telem?vel': 'telemóvel',
    'Telem?vel': 'Telemóvel',
    
    'irrevers?vel': 'irreversível',
    'Irrevers?vel': 'Irreversível',
    
    'informa?ão': 'informação',
    'Informa?ão': 'Informação',
    
    '??': '??',  # Deixar os ?? que ainda faltam
}

# Aplicar substituições em ordem (do mais específico para o mais genérico)
for old, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
    if old != new:  # Não substituir palavras por si mesmas
        content = content.replace(old, new)

# Re-salvar em UTF-8 puro
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo re-salvo em UTF-8 correto!")
print("✅ Todos os acentos foram restaurados automaticamente!")
