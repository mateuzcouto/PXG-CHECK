#!/usr/bin/env python3
# -*- coding: utf-8 -*-

filepath = r"c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# First, let's fix the structure by improving header styling and adding chevron icon
# We need to refactor the header section to be clickable with proper chevron rotation

# Replace the current header structure with an improved one
old_header = '''                <div class="flex justify-between items-center text-left">
                    <div class="flex items-center gap-3">
                        <div class="${clan.color} clan-badge text-white font-black shadow-lg" title="${clan.name}">${clan.icon}</div>
                        <div>
                            <h3 id="name-${char.id}" class="text-base font-black italic uppercase text-white leading-none">${char.name}</h3>'''

new_header = '''                <div onclick="window.actions.toggleCollapse('${char.id}')" class="flex items-center justify-between cursor-pointer group/char -mx-4 -mt-4 px-4 pt-4 pb-3 hover:bg-slate-800/30 transition-colors rounded-t-[1.5rem]">
                    <div class="flex items-center gap-3">
                        <div class="${clan.color} clan-badge text-white font-black shadow-lg" title="${clan.name}">${clan.icon}</div>
                        <div>
                            <h3 id="name-${char.id}" class="text-base font-black italic uppercase text-white leading-none">${char.name}</h3>'''

content = content.replace(old_header, new_header)

# Now replace the closing part of the header that had the buttons with chevron structure
old_buttons = '''                    </div>
                    <div class="flex gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 shrink-0 ml-2 transition-all">
                        <button onclick="window.actions.toggleCollapse('${char.id}')" class="text-red-400 hover:text-red-300 font-bold p-1.5 transition-colors text-xl" title="${isCollapsed ? 'Maximizar Personagem' : 'Minimizar Personagem'}">
                            ${isCollapsed ? '⬆️' : '⬇️'}
                        </button>
                        <div class="w-px h-4 bg-slate-800 my-auto ${isCollapsed ? 'hidden' : 'block'}"></div>
                        <button onclick="window.actions.exportData('${char.id}')" class="text-slate-500 hover:text-emerald-400 font-bold p-1.5 transition-colors ${isCollapsed ? 'hidden' : 'block'}" title="Exportar Dados">💾</button>
                        <button onclick="ui.openModal('${char.id}')" class="text-slate-500 hover:text-blue-400 font-bold p-1.5 transition-colors ${isCollapsed ? 'hidden' : 'block'}" title="Editar Configurações">✏️</button>
                        <button onclick="window.actions.askDelete('${char.id}')" class="text-slate-600 hover:text-red-500 font-bold p-1.5 transition-colors ${isCollapsed ? 'hidden' : 'block'}" title="Apagar Personagem">&times;</button>
                    </div>
                </div>'''

new_buttons = '''                    </div>
                    <div class="flex items-center gap-3">
                        <svg class="chevron w-5 h-5 text-slate-500 transition-transform ${isCollapsed ? 'rotate-90' : 'rotate-180'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </div>
                </div>

                <div class="flex gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 shrink-0 ml-2 transition-all ${isCollapsed ? 'hidden' : 'flex'} mx-4 mb-3">
                    <button onclick="window.actions.exportData('${char.id}')" class="text-slate-500 hover:text-emerald-400 font-bold p-1.5 transition-colors" title="Exportar Dados">💾</button>
                    <div class="w-px h-4 bg-slate-800 my-auto"></div>
                    <button onclick="ui.openModal('${char.id}')" class="text-slate-500 hover:text-blue-400 font-bold p-1.5 transition-colors" title="Editar Configurações">✏️</button>
                    <button onclick="window.actions.askDelete('${char.id}')" class="text-slate-600 hover:text-red-500 font-bold p-1.5 transition-colors" title="Apagar Personagem">&times;</button>
                </div>'''

content = content.replace(old_buttons, new_buttons)

# Update the content div to have proper styling for collapsed state
content = content.replace(
    f'''<div id="content-${{char.id}}" class="${{isCollapsed ? 'hidden' : 'block'}} transition-all duration-300">
                    <div class="flex items-center justify-center gap-6 py-2 border-y border-slate-800/50 mt-2">''',
    f'''<div id="content-${{char.id}}" class="char-content ${{isCollapsed ? 'hidden' : 'block'}} transition-all duration-300">
                    <div class="flex items-center justify-center gap-6 py-2 border-t border-slate-800/50 mt-0">'''
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Trainer card header improved with chevron system!")
