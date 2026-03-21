
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
    import { getFirestore, collection, addDoc, onSnapshot, doc, updateDoc, deleteDoc, query } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
    import { getAuth, signInAnonymously, onAuthStateChanged, GoogleAuthProvider, linkWithPopup, signInWithPopup, signOut } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

    // =========================================================================
    // 🌟 SISTEMA DE AUTO-ATUALIZAÇÃO (DNA BUILD)
    // =========================================================================
    const APP_VERSION = "1.3.16"; 

    function checkForUpdates() {
        const checkUrl = window.location.pathname + '?nocache=' + new Date().getTime();
        
        fetch(checkUrl, {
            cache: 'no-store',
            headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' }
        })
        .then(res => res.text())
        .then(html => {
            const match = html.match(/const APP_VERSION = ["']([^"']+)["']/);
            if (match && match[1] && match[1] !== APP_VERSION) {
                const banner = document.getElementById('update-banner');
                if(banner) {
                    banner.classList.remove('hidden');
                    banner.classList.add('flex');
                }
            }
        }).catch(() => {});
    }

    setTimeout(checkForUpdates, 3000); 
    setInterval(checkForUpdates, 300000);

    window.forceUpdate = () => {
        window.location.href = window.location.pathname + '?v=' + new Date().getTime();
    };
    // =========================================================================

    const config = {
        apiKey: "AIzaSyCqSjQVu5krTBo0FOjEm4o3exiBrkaW_Q8",
        authDomain: "pxg-check.firebaseapp.com",
        projectId: "pxg-check",
        storageBucket: "pxg-check.firebasestorage.app",
        messagingSenderId: "887959385568",
        appId: "1:887959385568:web:7e230fd4f707a409a26785"
    };

    const fbApp = initializeApp(config);
    const db = getFirestore(fbApp);
    const auth = getAuth(fbApp);
    const DB_COLLECTION = "pxg-prod-v1";

    const safeJSONParse = (raw, fallback) => {
        try {
            if (raw === null || raw === undefined || raw === '') return fallback;
            return JSON.parse(raw);
        } catch {
            return fallback;
        }
    };

    const safeGetLocalStorage = (key, fallback = null) => {
        try {
            const value = localStorage.getItem(key);
            return value === null ? fallback : value;
        } catch {
            return fallback;
        }
    };

    const safeSetLocalStorage = (key, value) => {
        try {
            localStorage.setItem(key, value);
        } catch {
            // Ignora falhas de quota ou modo privado sem quebrar o fluxo.
        }
    };

    const escapeHtml = (value) => String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');

    const escapeAttr = (value) => escapeHtml(value).replace(/`/g, '&#96;');

    const debounce = (fn, delay = 220) => {
        let timer = null;
        return (...args) => {
            if (timer) clearTimeout(timer);
            timer = setTimeout(() => fn(...args), delay);
        };
    };

    let characters = [];
    let characterToDelete = null;
    let pendingUncheckToggle = null;
    let currentLang = safeGetLocalStorage('pxg_lang', 'pt') || 'pt';
    let collapsedChars = safeJSONParse(safeGetLocalStorage('pxg_collapsed_chars', '[]'), []);

    // =========================================================================
    // 🔐 SEGURANÇA E ADMINISTRAÇÃO MESTRA
    // =========================================================================
    let isAdmin = false;
    const ADMIN_EMAIL = "mateuscouto27@gmail.com"; 
    let notificationsEnabled = safeGetLocalStorage('pxg_notifications', 'false') === 'true';
    let lastNotifiedEvent = null;
    let visualAlertHideTimer = null;

    const translations = {
        pt: {
            add: "Adicionar", subtitle: "Gestão do Personagem", loading: "A carregar...", none: "Bem-vindo ao seu Check Point Diário!", noneDesc: "Registre o seu primeiro personagem.", 
            reset: "Reset Geral",
            events: "Eventos Globais", dungeons: "Dungeons", dailies: "Diárias", johto: "Ginásios", clones: "Mensais", specials: "Semanais", quests: "QUESTS",
            doneAt: "Feito em", resetAt: "Próx. Reset", permanent: "Permanente", save: "Salvar Treinador", newName: "Novo Treinador", labelName: "Nickname",
            finToday: "Hoje", finWeek: "Semana", finMonth: "Mês", finCurrent: "Saldo Atual", finSet: "Definir Saldo", finReason: "Motivo (Opcional)",
            taskNames: {
                boss12: "Boss Global (12:00)", boss16: "Boss Global (16:00)", boss20: "Boss Global (20:00)", boss23: "Boss Global (23:00)",
                park11: "Poképark (11:00)", park15: "Poképark (15:00)", park21: "Poképark (21:00)",
                blue: "Dungeon Azul", red: "Mystery Vermelha", catch1: "Daily Catch #1", catch2: "Daily Catch #2", task: "Daily KILL",
                dl_bro12: "NPC BH", dl_bro6_nw: "NPC BH NW", dl_falkner_nw: "Falkner Nightmare", dl_yellow_nw: "Yellow Parachute Nightmare", dl_jenny_nw: "Officer Jenny Nightmare", dl_raven_nw: "Raven Nightmare", dl_lance_nw: "Lance Nightmare", dl_bruno_nw: "Bruno Nightmare", dl_blanca_nw: "Blanca Nightmare", dl_sidis: "Sidis S-3 Ultra Lab", dl_mite_nw: "Mite Nightmare",
                silver: "Silver Rival", dog: "Cães Lendários", ghost: "Fantasma de Lavender", violet: "Gym Violet", azalea: "Gym Azalea", goldenrod: "Gym Goldenrod",
                ecruteak: "Gym Ecruteak", cianwood: "Gym Cianwood", olivine: "Gym Olivine", mahogany: "Gym Mahogany", blackthorn: "Gym Blackthorn",
                clones: "Clone Task (30 dias)", m_secret_lab: "Secret LAB", m_clones_nw: "CLONES NW 5/6", qCyber: "Cyber Quest", qMewtwo: "Mewtwo Quest",
                dzChristmas: "DZ Christmas", sp_tower: "Embedded Tower", sp_terror_nw: "Nightmare Terror", sp_eleanor: "Eleanor Outland", sp_fawkes: "Fawkes Orre", sp_factory: "Battle Factory", sp_misty_nw: "Misty Nightmare", sp_lorelei_nw: "Lorelei Nightmare", sp_subj14: "Subject #14 NW", sp_barry_nw: "Barry Mecha Nightmare", qTimeTravel: "Time Travel Quest", qTrevo: "Trevo", qOrbs: "245 Rainbow Orbs", qSarkies: "Sarkies", qTransporteNW: "Transporte NW", qKoga: "Koga Quest", qLabNW: "LAB NW"
            }
        },
        en: {
            add: "Add Char", subtitle: "Character Management", loading: "Loading...", none: "Welcome to your Tracker!", noneDesc: "Register your first character.", 
            reset: "Global Reset",
            events: "Global Events", dungeons: "Dungeons", dailies: "Dailies", johto: "Gyms", clones: "Monthly", specials: "Weekly", quests: "QUESTS",
            doneAt: "Done at", resetAt: "Next Reset", permanent: "Permanent", save: "Save Trainer", newName: "New Trainer", labelName: "Nickname",
            finToday: "Today", finWeek: "Week", finMonth: "Month", finCurrent: "Current Balance", finSet: "Set Balance", finReason: "Reason (Optional)",
            taskNames: {
                boss12: "Global Boss (12:00)", boss16: "Global Boss (16:00)", boss20: "Global Boss (20:00)", boss23: "Global Boss (23:00)",
                park11: "Poképark (11:00)", park15: "Poképark (15:00)", park21: "Poképark (21:00)",
                blue: "Blue Dungeon", red: "Red Mystery", catch1: "Daily Catch #1", catch2: "Daily Catch #2", task: "Daily KILL",
                dl_bro12: "NPC BH", dl_bro6_nw: "NPC BH NW", dl_falkner_nw: "Falkner Nightmare", dl_yellow_nw: "Yellow Parachute Nightmare", dl_jenny_nw: "Officer Jenny Nightmare", dl_raven_nw: "Raven Nightmare", dl_lance_nw: "Lance Nightmare", dl_bruno_nw: "Bruno Nightmare", dl_blanca_nw: "Blanca Nightmare", dl_sidis: "Sidis S-3 Ultra Lab", dl_mite_nw: "Mite Nightmare",
                silver: "Silver Rival", dog: "Legendary Dogs", ghost: "Lavender Ghost", violet: "Violet Gym", azalea: "Azalea Gym", goldenrod: "Goldenrod Gym",
                ecruteak: "Ecruteak Gym", cianwood: "Cianwood Gym", olivine: "Olivine Gym", mahogany: "Mahogany Gym", blackthorn: "Blackthorn Gym",
                clones: "Clone Task (30 days)", m_secret_lab: "Secret LAB", m_clones_nw: "CLONES NW 5/6", qCyber: "Cyber Quest", qMewtwo: "Mewtwo Quest",
                dzChristmas: "DZ Christmas", sp_tower: "Embedded Tower", sp_terror_nw: "Nightmare Terror", sp_eleanor: "Eleanor Outland", sp_fawkes: "Fawkes Orre", sp_factory: "Battle Factory", sp_misty_nw: "Misty Nightmare", sp_lorelei_nw: "Lorelei Nightmare", sp_subj14: "Subject #14 NW", sp_barry_nw: "Barry Mecha Nightmare", qTimeTravel: "Time Travel Quest", qTrevo: "Trevo", qOrbs: "245 Rainbow Orbs", qSarkies: "Sarkies", qTransporteNW: "Transporte NW", qKoga: "Koga Quest", qLabNW: "LAB NW"
            }
        }
    };

    const clanData = {
        volcanic: { name: "Volcanic", color: "bg-red-700", icon: "🐉", border: "border-red-600", text: "text-red-400", desc: "Dragão de chamas surgindo de um vulcão" },
        seavell: { name: "Seavell", color: "bg-blue-700", icon: "🧊", border: "border-blue-600", text: "text-blue-300", desc: "Criatura serpentina moldada em água gelada" },
        orebound: { name: "Orebound", color: "bg-amber-700", icon: "✊", border: "border-amber-600", text: "text-amber-400", desc: "Punho de pedra blindado integrando-se à montanha" },
        wingeon: { name: "Wingeon", color: "bg-sky-500", icon: "🦅", border: "border-sky-400", text: "text-sky-200", desc: "Águia imponente envolta em redemoinho de vento" },
        naturia: { name: "Naturia", color: "bg-green-700", icon: "🪷", border: "border-green-600", text: "text-green-300", desc: "Flor de lótus envolta por vinhas e energia natural" },
        malefic: { name: "Malefic", color: "bg-purple-800", icon: "☠️", border: "border-purple-600", text: "text-purple-300", desc: "Crânio sombrio sob a lua cheia com névoa venenosa" },
        gardestrike: { name: "Gardestrike", color: "bg-orange-600", icon: "🥊", border: "border-orange-500", text: "text-orange-400", desc: "Luva de combate blindada em ação defensiva e ofensiva" },
        raibolt: { name: "Raibolt", color: "bg-yellow-500", icon: "⚡", border: "border-yellow-400", text: "text-yellow-300", desc: "Raio clássico rompendo nuvens de tempestade" },
        psycraft: { name: "Psycraft", color: "bg-pink-600", icon: "👁️", border: "border-pink-500", text: "text-pink-300", desc: "Olho cósmico e místico com espirais de energia psíquica" },
        ironhard: { name: "Ironhard", color: "bg-slate-600", icon: "🛡️", border: "border-slate-500", text: "text-slate-200", desc: "Guerreiro com armadura pesada de metal" }
    };

    // =========================================================
    // SISTEMA RAINBOW ORBS (BANCO DE DADOS EXTERNO GITHUB)
    // =========================================================
    let userOrbsProgress = safeJSONParse(safeGetLocalStorage('pxg_rainbow_orbs', '[]'), []);
    let openOrbGroups = safeJSONParse(safeGetLocalStorage('pxg_open_orb_groups', '[]'), []);

    let rainbowOrbs = [];

    // Fallback científico: Converte texto CSV/TSV/TXT automaticamente, ignorando formato quebrado
    function parseCSVtoOrbs(csvText) {
        const lines = csvText.trim().split('\n');
        const orbsArray = [];
        
        // Deteta automaticamente qual separador foi usado no ficheiro (Vírgula, Ponto-e-vírgula ou Tab)
        let separator = ',';
        const sampleLine = lines.length > 1 ? lines[1] : lines[0];
        if (!sampleLine) return [];
        
        if (sampleLine.includes(';')) separator = ';';
        else if (sampleLine.includes('\t')) separator = '\t';
        
        const regex = new RegExp(`${separator}(?=(?:(?:[^"]*"){2})*[^"]*$)`);
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            // Pula as linhas de cabeçalho que só contêm títulos
            if (!line || (line.toLowerCase().includes('coords') && line.toLowerCase().includes('region'))) continue; 
            
            const cols = line.split(regex);
            
            if (cols.length >= 3) {
                const idStr = cols[0].replace(/["']/g, '').trim();
                const id = parseInt(idStr) || (orbsArray.length + 1);
                const coords = cols[1].replace(/["']/g, '').trim();
                const region = cols[2].replace(/["']/g, '').trim();
                let comment = cols[3] ? cols[3].replace(/["']/g, '').trim() : '';
                
                let desc = `Coords: [${coords}]`;
                if (comment && comment !== 'undefined' && comment !== 'null') desc += ` • ${comment}`; 
                
                orbsArray.push({ id: id, location: region || 'Desconhecido', desc: desc, rawCoords: coords });
            }
        }
        return orbsArray;
    }

    async function carregarBancoDeOrbs() {
        try {
            const urlGitHubRaw = 'https://raw.githubusercontent.com/mateuzcouto/orbs.json/main/orbs.json';
            const resposta = await fetch(urlGitHubRaw);
            
            if (!resposta.ok) throw new Error("Não foi possível aceder ao GitHub.");
            
            const textoDoArquivo = await resposta.text();
            
            try {
                // Tenta ler como JSON estrito
                const jsonLido = JSON.parse(textoDoArquivo);
                if (Array.isArray(jsonLido) && jsonLido.length > 0) {
                    
                    // Mapeamento Dinâmico: Extrai os valores por POSIÇÃO (0, 1, 2) resolvendo o erro de 'undefined'
                    rainbowOrbs = jsonLido.map((item, index) => {
                        
                        // Cenário A: O JSON é uma lista de listas Ex: [1, "coord", "cidade", "obs"]
                        if (Array.isArray(item)) {
                            const c = item[1] || "";
                            const obs = item[3] || "";
                            return {
                                id: parseInt(item[0]) || index + 1,
                                location: item[2] || "Desconhecido",
                                rawCoords: c,
                                desc: `Coords: [${c}]` + (obs && obs !== 'undefined' ? ` • ${obs}` : '')
                            };
                        }
                        
                        // Cenário B: O JSON é uma lista de objetos Ex: {"Coluna1": 1, "Coluna2": "coord"...}
                        if (typeof item === 'object') {
                            const vals = Object.values(item); 
                            const id = parseInt(item.id) || parseInt(vals[0]) || index + 1;
                            const coords = item.coords || item.coordenadas || item.rawCoords || vals[1] || "";
                            const region = item.location || item.region || item.regiao || item.cidade || vals[2] || "Desconhecido";
                            const obs = item.desc || item.obs || item.observacao || item.comment || vals[3] || "";
                            
                            let finalDesc = obs;
                            if (!obs.includes('Coords:')) {
                                finalDesc = `Coords: [${coords}]` + (obs && obs !== 'undefined' ? ` • ${obs}` : '');
                            }
                            
                            return { id: id, location: region, rawCoords: coords, desc: finalDesc };
                        }
                        return item;
                    }).filter(orb => orb && orb.location); // Limpeza final de segurança
                } else {
                    rainbowOrbs = parseCSVtoOrbs(textoDoArquivo);
                }
            } catch (erroJson) {
                // Se falhar a leitura JSON (porque colou texto bruto), aciona o Fallback Científico
                rainbowOrbs = parseCSVtoOrbs(textoDoArquivo);
            }
            
            renderOrbsList(document.getElementById('orb-search')?.value || '');
            
        } catch (error) {
            console.error("Erro Crítico no Banco de Orbs:", error);
            const container = document.getElementById('orbs-container');
            if(container) {
                container.innerHTML = '<p class="text-xs text-red-500 text-center italic mt-4 font-bold">Erro de conexão ao Banco de Orbs do GitHub.</p>';
            }
        }
    }

    let orbsLoaded = false;
    function ensureOrbsLoaded() {
        if (orbsLoaded) return;
        orbsLoaded = true;
        carregarBancoDeOrbs();
    }

    function renderOrbsList(filterText = '') {
        const container = document.getElementById('orbs-container');
        if (!container) return;
        container.innerHTML = '';

        const term = filterText.toLowerCase();
        let total = 0;
        let done = 0;

        const grouped = {};
        rainbowOrbs.forEach(orb => {
            total++;
            const isDone = userOrbsProgress.includes(orb.id);
            if (isDone) done++;

            if (term && !orb.location.toLowerCase().includes(term) && !orb.desc.toLowerCase().includes(term)) return;

            if (!grouped[orb.location]) grouped[orb.location] = [];
            grouped[orb.location].push({ ...orb, isDone });
        });

        const counterText = document.getElementById('orbs-counter-text');
        const progressBar = document.getElementById('orbs-progress-bar');
        if (counterText) counterText.innerText = `${done} / 245`; 
        if (progressBar) progressBar.style.width = `${total > 0 ? (done / total) * 100 : 0}%`;

        if (Object.keys(grouped).length === 0) {
            container.innerHTML = '<p class="text-xs text-slate-500 text-center italic mt-4">Nenhuma orb encontrada.</p>';
            return;
        }

        Object.keys(grouped).sort().forEach(loc => {
            const groupOrbs = grouped[loc];
            const groupDone = groupOrbs.filter(o => o.isDone).length;
            const isGroupComplete = groupDone === groupOrbs.length && groupOrbs.length > 0;

            const groupDiv = document.createElement('div');
            groupDiv.className = `bg-slate-900 border ${isGroupComplete ? 'border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.15)]' : 'border-slate-800'} rounded-2xl overflow-hidden mb-3 transition-all duration-500`;
            
            const safeLocId = loc.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9-]/g, '');
            const isOpen = openOrbGroups.includes(safeLocId) || term !== ''; 

            const header = document.createElement('div');
            header.className = `p-4 flex items-center justify-between cursor-pointer hover:bg-slate-800 transition-colors ${isGroupComplete ? 'bg-purple-900/20' : 'bg-slate-950/80'} select-none`;
            header.onclick = (e) => {
                if(e.target.tagName.toLowerCase() === 'button' || e.target.closest('button')) return; // Evita abrir/fechar ao clicar no Marcar Tudo
                const content = document.getElementById(`orb-group-${safeLocId}`);
                const chevron = document.getElementById(`chevron-${safeLocId}`);
                const markAllBtn = document.getElementById(`mark-all-${safeLocId}`);
                const index = openOrbGroups.indexOf(safeLocId);
                
                if (content.classList.contains('hidden')) {
                    content.classList.remove('hidden');
                    chevron.style.transform = 'rotate(180deg)';
                    if(markAllBtn) markAllBtn.classList.remove('hidden');
                    if (index === -1) openOrbGroups.push(safeLocId);
                } else {
                    content.classList.add('hidden');
                    chevron.style.transform = 'rotate(0deg)';
                    if(markAllBtn) markAllBtn.classList.add('hidden');
                    if (index > -1) openOrbGroups.splice(index, 1);
                }
                safeSetLocalStorage('pxg_open_orb_groups', JSON.stringify(openOrbGroups));
            };

            const safeLocText = escapeHtml(loc);
            const safeLocArg = encodeURIComponent(String(loc ?? ''));

            header.innerHTML = `
                <div class="flex flex-col text-left">
                    <span class="text-xs font-black uppercase tracking-widest ${isGroupComplete ? 'text-purple-400' : 'text-slate-200'}">
                        ${isGroupComplete ? '🏆 ' : ''}${safeLocText}
                    </span>
                    <span class="text-[9px] font-bold ${isGroupComplete ? 'text-emerald-400' : 'text-purple-400'} mt-1 uppercase">${isGroupComplete ? 'CONCLUÍDO' : `${groupDone} / ${groupOrbs.length} CONCLUÍDAS`}</span>
                </div>
                <div class="flex items-center gap-3">
                    ${!isGroupComplete ? `
                    <button id="mark-all-${safeLocId}" data-action="mark-all-orbs" data-region="${safeLocArg}" class="${isOpen ? '' : 'hidden'} bg-purple-600/20 hover:bg-purple-500 text-purple-400 hover:text-white border border-purple-500/30 px-2 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all active:scale-95 shadow-sm" title="Marcar todas as Orbs desta região como concluídas">
                        Marcar Tudo
                    </button>
                    ` : ''}
                    <svg id="chevron-${safeLocId}" style="transform: rotate(${isOpen ? '180deg' : '0deg'})" class="w-5 h-5 ${isGroupComplete ? 'text-purple-400' : 'text-slate-500'} transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
            `;

            const contentDiv = document.createElement('div');
            contentDiv.id = `orb-group-${safeLocId}`;
            contentDiv.className = `${isOpen ? '' : 'hidden'} border-t border-slate-800/50 bg-slate-950/30 p-2 space-y-1`;

            groupOrbs.forEach(orb => {
                const safeDesc = escapeHtml(orb.desc);
                const safeCoordsArg = encodeURIComponent(String(orb.rawCoords ?? ''));
                contentDiv.innerHTML += `
                    <div data-action="toggle-orb" data-orb-id="${orb.id}" class="flex items-center justify-between p-3 rounded-xl hover:bg-slate-800/50 transition-colors cursor-pointer group">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-slate-900 flex items-center justify-center border ${orb.isDone ? 'border-purple-500 text-purple-400 shadow-[0_0_10px_rgba(168,85,247,0.3)]' : 'border-slate-700 text-slate-500'} shrink-0">
                                <span class="text-[10px] font-black">${orb.id}</span>
                            </div>
                            <div class="flex flex-col text-left">
                                <div class="flex items-center gap-2 flex-wrap">
                                    <span class="text-[10px] font-bold ${orb.isDone ? 'text-slate-500 line-through' : 'text-slate-200'}">${safeDesc}</span>
                                    <button data-action="copy-orb-coords" data-coords="${safeCoordsArg}" class="bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white p-1 rounded-md transition-colors border border-slate-700 shadow-sm" title="Copiar Coordenadas">
                                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="custom-check ${orb.isDone ? 'active !bg-purple-600 !border-purple-600' : ''} shrink-0 ml-3"></div>
                    </div>
                `;
            });

            groupDiv.appendChild(header);
            groupDiv.appendChild(contentDiv);
            container.appendChild(groupDiv);
        });
    }

    // Funções de Auth e UI de Perfil
    function updateAuthUI(user) {
        const authContainer = document.getElementById('auth-container');
        if (!authContainer) return;

        if (user && !user.isAnonymous) {
            const userName = escapeHtml(user.displayName ? user.displayName.split(' ')[0] : 'Jogador');
            const photoSrcRaw = user.photoURL || 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png';
            const photoSrc = /^https:\/\//i.test(photoSrcRaw) ? photoSrcRaw : 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png';
            
            authContainer.innerHTML = `
                <div class="flex items-center gap-1.5 sm:gap-2 bg-slate-800/80 rounded-full pl-1.5 pr-2 py-1 sm:pl-2 sm:pr-3 sm:py-1.5 border border-slate-700 shadow-sm shrink-0">
                    <img src="${photoSrc}" referrerpolicy="no-referrer" class="w-5 h-5 sm:w-6 sm:h-6 rounded-full border border-slate-600 object-cover bg-slate-900 shrink-0 auth-avatar">
                    <span class="hidden sm:inline text-[9px] font-black text-white uppercase tracking-widest">${userName}</span>
                    <div class="hidden sm:block w-px h-3 bg-slate-600 mx-1"></div>
                    <button data-action="logout" class="text-[8px] text-red-400 hover:text-red-300 uppercase font-black tracking-widest transition-colors" title="Sair da Conta">Sair</button>
                </div>
            `;
        } else {
            authContainer.innerHTML = `
                <button data-action="open-login-modal" class="flex items-center justify-center gap-1.5 w-8 h-8 sm:w-auto sm:h-auto sm:px-3 sm:py-2.5 rounded-full text-[9px] font-black uppercase transition-all bg-blue-600/20 text-blue-400 hover:text-blue-300 hover:bg-blue-600/30 border border-blue-500/30 shadow-sm shrink-0" title="Salvar na Nuvem">
                    <svg class="w-4 h-4 sm:w-3.5 sm:h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>
                    <span class="hidden sm:inline">Nuvem</span>
                </button>
            `;
        }
    }

    onAuthStateChanged(auth, (user) => {
        if (!user) {
            signInAnonymously(auth);
        } else {
            if (user.email && user.email.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
                isAdmin = true;
                const adminMenu = document.getElementById('admin-menu-container');
                if (adminMenu) adminMenu.classList.remove('hidden');
                // Sincroniza a caixa de entrada de feedbacks se for o Administrador
                initAdminData();
            }
            updateAuthUI(user);
            initData(user.uid);
        }
    });

    document.addEventListener('click', (e) => {
        const dropdown = document.getElementById('nav-dropdown-wrapper');
        const list = document.getElementById('nav-dropdown-list');
        const chevron = document.getElementById('nav-chevron');
        if (dropdown && list && !dropdown.contains(e.target)) {
            if (!list.classList.contains('hidden')) {
                list.classList.add('hidden');
                if(chevron) chevron.style.transform = 'rotate(0deg)';
            }
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        const versionEl = document.getElementById('app-version-display');
        if (versionEl) versionEl.innerText = APP_VERSION;
        window.ui.updateNotificationIcon();
    });

    setInterval(() => {
        const now = new Date();
        const elClock = document.getElementById('global-clock');
        if (elClock) elClock.innerText = now.toLocaleString(currentLang === 'pt' ? 'pt-PT' : 'en-US');

        const day = now.getDay();
        const isParkDay = [0, 2, 4, 6].includes(day);
        
        // Adicionada Duração Estimada (em minutos) para o sistema saber quando desativar a animação
        const events = [
            { name: 'Boss Global', h: 12, m: 0, duration: 15 },
            { name: 'Boss Global', h: 16, m: 0, duration: 15 },
            { name: 'Boss Global', h: 20, m: 0, duration: 15 },
            { name: 'Boss Global', h: 23, m: 0, duration: 15 }
        ];
        
        if (isParkDay) {
            events.push({ name: 'Poképark', h: 11, m: 0, duration: 30 });
            events.push({ name: 'Poképark', h: 15, m: 0, duration: 30 });
            events.push({ name: 'Poképark', h: 21, m: 0, duration: 30 });
        }
        
        const currentMins = now.getHours() * 60 + now.getMinutes();
        let nextEvent = null;
        let activeEvent = null;
        let minDiff = Infinity;
        
        for (let ev of events) {
            const evStart = ev.h * 60 + ev.m;
            const evEnd = evStart + (ev.duration || 15);
            
            // Lógica: Verifica se o momento atual está DENTRO da janela do evento
            if (currentMins >= evStart && currentMins < evEnd) {
                activeEvent = ev;
            } else if (evStart > currentMins) {
                if (evStart - currentMins < minDiff) {
                    minDiff = evStart - currentMins;
                    nextEvent = ev;
                }
            }
        }
        
        let bannerText = "Sem mais eventos hoje";
        let bannerHtml = "Sem mais eventos hoje";
        let isLive = false;
        let isBossLive = false;
        
        if (activeEvent) {
            bannerText = `🔴 ${activeEvent.name.toUpperCase()} AGORA!`;
            isLive = true;
            isBossLive = activeEvent.name === 'Boss Global';
            if (isBossLive) {
                bannerHtml = `<span class="boss-live-name">🔴 ${activeEvent.name.toUpperCase()} AGORA!</span>`;
            } else {
                bannerHtml = `🟢 ${activeEvent.name.toUpperCase()} AGORA!`;
            }
        } else if (nextEvent) {
            const hh = nextEvent.h.toString().padStart(2, '0');
            const mm = nextEvent.m.toString().padStart(2, '0');
            bannerText = `Próx. Evento: ${nextEvent.name} às ${hh}:${mm}`;
            const eventPrefix = nextEvent.name === 'Boss Global' ? '🔴' : '🔔';
            bannerHtml = `${eventPrefix} Próx. Evento: ${nextEvent.name} às ${hh}:${mm}`;

            // Lógica Científica de Notificação: Alerta 5 min antes
            if (notificationsEnabled && minDiff === 5 && lastNotifiedEvent !== (nextEvent.name + nextEvent.h)) {
                
                // 1. Feedback Auditivo Matemático (Garante que toca mesmo no modo Não Incomodar)
                try {
                    const ctx = new (window.AudioContext || window.webkitAudioContext)();
                    const osc = ctx.createOscillator();
                    const gainNode = ctx.createGain();
                    
                    osc.type = 'sine'; // Onda suave e agradável
                    osc.frequency.setValueAtTime(880, ctx.currentTime); // Nota Musical A5
                    osc.frequency.exponentialRampToValueAtTime(1318.51, ctx.currentTime + 0.1); // Sobe para E6 (Efeito de "Subida/Aviso")
                    
                    gainNode.gain.setValueAtTime(0.3, ctx.currentTime); // Volume a 30%
                    gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5); // Desvanece suavemente
                    
                    osc.connect(gainNode);
                    gainNode.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.5);
                } catch (e) {
                    console.log("Áudio bloqueado pelo navegador até interação do utilizador.");
                }

                // 2. Feedback Visual (Notificação Push do Sistema Operativo)
                if (Notification.permission === "granted") {
                    new Notification("PXG Check - Evento a Caminho!", {
                        body: `Prepare-se! O evento ${nextEvent.name} começa em exatamente 5 minutos!`,
                        icon: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
                    });
                }
                
                // 3. Feedback Visual Gamer (Ecrã a piscar)
                const visualAlert = document.getElementById('event-visual-alert');
                const visualName = document.getElementById('event-alert-name');
                if (visualAlert && visualName) {
                    visualName.innerText = nextEvent.name;
                    visualAlert.classList.remove('hidden');
                    visualAlert.classList.add('flex');
                    if (visualAlertHideTimer) clearTimeout(visualAlertHideTimer);
                    
                    // Oculta o alerta gigante após 10 segundos para não prender o rato do utilizador
                    visualAlertHideTimer = setTimeout(() => {
                        visualAlert.classList.remove('flex');
                        visualAlert.classList.add('hidden');
                    }, 10000);
                }

                lastNotifiedEvent = nextEvent.name + nextEvent.h;
            }
        }
        
        const desktopBanner = document.getElementById('next-event-banner');
        const mobileBanner = document.getElementById('next-event-banner-mobile');
        
        // Aplicação automática de Estado (Ativa/Desativa o modo CHAMATIVO)
        const applyBannerState = (el) => {
            if(!el) return;
            if(el.innerText !== bannerText) el.innerHTML = bannerHtml;
            
            if (isLive) {
                el.classList.add('banner-live-active');
            } else {
                el.classList.remove('banner-live-active');
            }

            if (isBossLive) {
                el.classList.add('banner-boss-active');
            } else {
                el.classList.remove('banner-boss-active');
            }
        };

        applyBannerState(desktopBanner);
        applyBannerState(mobileBanner);

    }, 1000);

    function isTaskExpired(cat, task) {
        if (!task || !task.done || !task.at) return false;
        const d = parseDateSafe(task.at);
        if (!d) return false;

        const now = new Date();
        let nextReset = new Date(d);

        if (cat === 'monthly') {
            nextReset.setDate(nextReset.getDate() + 30);
            return now >= nextReset;
        } 
        if (cat === 'dailies' || cat === 'events' || cat === 'johtoWeekly' || cat === 'specials') {
            nextReset.setHours(7, 40, 0, 0); 
            if (d.getTime() >= nextReset.getTime()) nextReset.setDate(nextReset.getDate() + 1);
            if (cat === 'johtoWeekly' || cat === 'specials') {
                while (nextReset.getDay() !== 1) nextReset.setDate(nextReset.getDate() + 1);
            }
            return now >= nextReset;
        }
        return false;
    }

    setInterval(() => {
        if (!auth || !auth.currentUser || characters.length === 0) return;
        const currentMonthStr = `${new Date().getFullYear()}-${new Date().getMonth() + 1}`;

        characters.forEach(char => {
            let needsUpdate = false;
            const tasks = char.tasks;

            let monthlyScore = char.monthlyScore || 0;
            let scoreMonth = char.scoreMonth || currentMonthStr;
            if (scoreMonth !== currentMonthStr) {
                monthlyScore = 0; scoreMonth = currentMonthStr; needsUpdate = true;
            }

            if (tasks) {
                Object.keys(tasks).forEach(cat => {
                    if (cat === 'quests') return;
                    Object.keys(tasks[cat]).forEach(k => {
                        if (isTaskExpired(cat, tasks[cat][k])) {
                            tasks[cat][k] = { done: false, at: null }; needsUpdate = true;
                        }
                    });
                });
            }
            if (needsUpdate) {
                updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', char.id), { tasks, monthlyScore, scoreMonth });
            }
        });
    }, 60000);

    function initData(uid) {
        const q = query(collection(db, 'artifacts', DB_COLLECTION, 'users', uid, 'characters'));
        onSnapshot(q, (snapshot) => {
            characters = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
            
            const currentMonthStr = `${new Date().getFullYear()}-${new Date().getMonth() + 1}`;
            characters.forEach(char => {
                let needsUpdate = false;
                const tasks = char.tasks;

                if (char.scoreMonth !== currentMonthStr) {
                    char.monthlyScore = 0; char.scoreMonth = currentMonthStr; needsUpdate = true;
                }

                if(tasks) {
                    Object.keys(tasks).forEach(cat => {
                        if(cat === 'quests') return;
                        Object.keys(tasks[cat]).forEach(k => {
                            if (isTaskExpired(cat, tasks[cat][k])) {
                                tasks[cat][k] = { done: false, at: null }; needsUpdate = true;
                            }
                        });
                    });
                }
                if(needsUpdate) updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', uid, 'characters', char.id), { tasks: char.tasks, monthlyScore: char.monthlyScore, scoreMonth: char.scoreMonth });
            });

            render();
            renderRanking();
            // Orbs agora são atualizadas por uma função de fetch assíncrona
            hideLoader();
        });
    }

    // =========================================================
    // 👑 SISTEMA DE ADMINISTRAÇÃO (FEEDBACKS)
    // =========================================================
    function initAdminData() {
        if (!isAdmin) return;
        // Escuta a coleção de tickets conforme Regra 1 e Regra 3
        const q = query(collection(db, 'artifacts', DB_COLLECTION, 'public', 'data', 'feedbacks'));
        onSnapshot(q, (snapshot) => {
            const feedbacks = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
            renderAdminPanel(feedbacks);
        }, (err) => console.error("Admin Access Error:", err));
    }

    function renderAdminPanel(feedbacks) {
        const container = document.getElementById('admin-container');
        if (!container) return;
        
        if (feedbacks.length === 0) {
            container.innerHTML = '<p class="text-xs text-slate-500 italic text-center">Nenhum feedback ou bug reportado até ao momento.</p>';
            return;
        }

        // Ordenação em memória (conforme Regra 2) para garantir que os mais novos fiquem no topo
        container.innerHTML = `
            <div class="flex items-center justify-between mb-4 border-b border-slate-800 pb-2">
                <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest italic">Tickets em Aberto (${feedbacks.length})</span>
            </div>
            <div class="space-y-4">
                ${feedbacks.sort((a,b) => new Date(b.date) - new Date(a.date)).map(fb => {
                    const safeId = escapeAttr(fb.id || '');
                    const safeText = escapeHtml(fb.text || '');
                    const safeDate = escapeHtml(fb.dataLeituraFacil || 'Data Desconhecida');
                    const safeUid = escapeHtml(fb.uid || 'anon');
                    return `
                    <div class="bg-slate-950 p-4 rounded-xl border ${fb.type === 'bug' ? 'border-red-900/40 shadow-[0_0_15px_rgba(239,68,68,0.05)]' : 'border-blue-900/40 shadow-[0_0_15px_rgba(59,130,246,0.05)]'} relative animate-fade">
                        <div class="flex justify-between items-start mb-3">
                            <span class="px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-widest ${fb.type === 'bug' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'}">
                                ${fb.type === 'bug' ? '🐛 Bug' : '💡 Sugestão'}
                            </span>
                            <button data-action="delete-feedback" data-feedback-id="${safeId}" class="text-slate-600 hover:text-red-500 transition-colors p-1" title="Arquivar Ticket">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                            </button>
                        </div>
                        <p class="text-xs text-slate-200 font-medium leading-relaxed mb-4">${safeText}</p>
                        <div class="pt-2 border-t border-slate-800/50 flex justify-between items-center">
                            <span class="text-[8px] font-bold text-slate-500 uppercase tracking-widest">${safeDate}</span>
                            <span class="text-[7px] text-slate-700 font-mono">UID: ${safeUid}</span>
                        </div>
                    </div>
                `;
                }).join('')}
            </div>
        `;
    }

    function parseDateSafe(dateStr) {
        if (!dateStr) return null;
        let d = new Date(dateStr);
        if (!isNaN(d)) return d;
        const parts = dateStr.split(', ');
        if (parts.length === 2) {
            const dateParts = parts[0].split('/');
            if (dateParts.length === 3) {
                d = new Date(`${dateParts[2]}-${dateParts[1]}-${dateParts[0]}T${parts[1]}`);
                if (!isNaN(d)) return d;
            }
        }
        return null;
    }

    function formatDateTime(d) {
        const date = d instanceof Date ? d : parseDateSafe(d);
        if (!date) return '--';
        return date.toLocaleString(currentLang === 'pt' ? 'pt-PT' : 'en-US', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    }

    function getNextAvailableText(cat, dateStr) {
        const d = parseDateSafe(dateStr);
        if (!d) return '--';
        let nextDate = new Date(d);

        if (cat === 'monthly') {
            nextDate.setDate(nextDate.getDate() + 30);
        } else if (cat === 'dailies' || cat === 'events') {
            nextDate.setHours(7, 40, 0, 0); 
            if (d.getTime() >= nextDate.getTime()) nextDate.setDate(nextDate.getDate() + 1);
        } else if (cat === 'johtoWeekly' || cat === 'specials') {
            nextDate.setHours(7, 40, 0, 0);
            if (d.getTime() >= nextDate.getTime()) nextDate.setDate(nextDate.getDate() + 1);
            while (nextDate.getDay() !== 1) nextDate.setDate(nextDate.getDate() + 1);
        }
        return formatDateTime(nextDate);
    }

    function getFinanceStats(transactions) {
        if (!transactions) return { d: 0, w: 0, m: 0 };
        const now = new Date();
        const dailyT = new Date(now); dailyT.setHours(7, 40, 0, 0);
        if (now < dailyT) dailyT.setDate(dailyT.getDate() - 1);

        const weeklyT = new Date(dailyT);
        while (weeklyT.getDay() !== 1) weeklyT.setDate(weeklyT.getDate() - 1);

        const monthlyT = new Date(now.getFullYear(), now.getMonth(), 1, 7, 40, 0, 0);
        if (now < monthlyT && now.getDate() === 1) monthlyT.setMonth(monthlyT.getMonth() - 1);

        let d = 0, w = 0, m = 0;
        transactions.forEach(t => {
            if (t.type === 'set') return; 
            const dt = new Date(t.date);
            if (dt >= dailyT) d += t.val;
            if (dt >= weeklyT) w += t.val;
            if (dt >= monthlyT) m += t.val;
        });
        return { d, w, m };
    }

    function formatK(val) {
        if (!val) return '<span class="text-slate-500">0K</span>';
        const isNeg = val < 0; const abs = Math.abs(val);
        let str = '';
        if (abs >= 1000) str = (abs / 1000).toFixed(abs % 1000 === 0 ? 0 : 1) + 'KK'; else str = abs + 'K';
        return `<span class="${isNeg ? 'text-red-400' : 'text-emerald-400'}">${isNeg ? '-' : '+'}${str}</span>`;
    }

    function renderRanking() {
        const container = document.getElementById('ranking-container');
        if (!container) return;
        container.innerHTML = '';
        
        if (characters.length === 0) {
            container.innerHTML = '<p class="text-xs text-slate-500 text-center italic mt-4">Nenhum personagem registado para o Ranking.</p>';
            return;
        }

        const sortedChars = [...characters].sort((a, b) => (b.monthlyScore || 0) - (a.monthlyScore || 0));

        sortedChars.forEach((char, index) => {
            let medal = `<span class="text-lg font-black text-slate-500">#${index + 1}</span>`;
            if (index === 0) medal = `<span class="text-xl" title="1º Lugar">🥇</span>`;
            else if (index === 1) medal = `<span class="text-xl" title="2º Lugar">🥈</span>`;
            else if (index === 2) medal = `<span class="text-xl" title="3º Lugar">🥉</span>`;

            const safeCharName = escapeHtml(char.name);
            const safeCharWorld = escapeHtml(char.world);
            container.innerHTML += `
                <div class="flex items-center justify-between p-4 rounded-2xl bg-slate-900 border ${index === 0 ? 'border-amber-500/50 shadow-[0_0_15px_rgba(245,158,11,0.1)]' : 'border-slate-800'} transition-all hover:scale-[1.01]">
                    <div class="flex items-center gap-4">
                        <div class="w-10 text-center">${medal}</div>
                        <div class="flex flex-col">
                            <span class="text-sm font-black text-white italic uppercase">${safeCharName}</span>
                            <span class="text-[9px] font-bold text-slate-500 uppercase">Lv ${char.level} • ${safeCharWorld}</span>
                        </div>
                    </div>
                    <div class="flex flex-col items-end">
                        <span class="text-sm font-black text-amber-500">${char.monthlyScore || 0} pts</span>
                        <span class="text-[7px] uppercase font-bold text-slate-600">Este mês</span>
                    </div>
                </div>
            `;
        });
    }

    function render() {
        const grid = document.getElementById('main-grid');
        const btnTop = document.getElementById('btn-add-top');
        if (!grid) return;
        grid.innerHTML = '';
        updateUITexts();
        const tStrings = translations[currentLang];

        if (characters.length === 0) {
            btnTop.classList.add('btn-pulse');
            grid.innerHTML = `
                <div class="col-span-full py-20 px-6 flex flex-col items-center justify-center text-center animate-fade">
                    <div class="w-24 h-24 bg-blue-600/10 rounded-full flex items-center justify-center mb-8 border border-blue-500/20 shadow-2xl">
                        <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                    </div>
                    <h3 class="text-3xl font-black italic uppercase text-white tracking-tighter mb-4">${tStrings.none}</h3>
                    <p class="text-slate-400 text-sm max-w-md mb-8 leading-relaxed font-medium uppercase tracking-tight">${tStrings.noneDesc}</p>
                    <button data-action="open-modal-new" class="bg-blue-600 hover:bg-blue-500 text-white font-black px-10 py-5 rounded-2xl flex items-center gap-3 transition-all shadow-xl shadow-blue-600/20 active:scale-95 text-xs uppercase tracking-widest">
                        Criar Primeiro Personagem
                    </button>
                </div>
            `;
            return;
        }

        btnTop.classList.remove('btn-pulse');
        const todayDay = new Date().getDay();
        const isPokeparkDay = [0, 2, 4, 6].includes(todayDay);

        characters.forEach(char => {
            const safeName = escapeHtml(char.name);
            const safeWorld = escapeHtml(char.world);
            const safeProfession = escapeHtml(char.profession || 'Sem Profissão');
            const safeSpecialization = char.specialization ? escapeHtml(char.specialization) : '';
            const isCollapsed = collapsedChars.includes(char.id);
            const clanKey = char.clan ? char.clan.toLowerCase() : 'volcanic';
            const clan = clanData[clanKey] || clanData.volcanic;
            
            const tasks = char.tasks || {};
            const events = tasks.events || {};
            const dailies = tasks.dailies || {};
            const weeklies = tasks.johtoWeekly || {};
            const monthly = tasks.monthly || {};
            const specials = tasks.specials || {};
            
            let evKeys = [];
            if (char.config?.enabledEvents?.boss) evKeys.push('boss12', 'boss16', 'boss20', 'boss23');
            if (char.config?.enabledEvents?.park && isPokeparkDay) evKeys.push('park11', 'park15', 'park21');

            const dgKeys = ['blue', 'red'].filter(k => char.config?.enabledDungeons?.[k]);
            const dlKeys = ['catch1', 'catch2', 'task', 'dl_bro12'].filter(k => char.config?.enabledDailies?.[k]);
            const gymKeys = ['violet', 'azalea', 'goldenrod', 'ecruteak', 'cianwood', 'olivine', 'mahogany', 'blackthorn'].filter(k => char.config?.enabledGyms?.[k]);
            const spKeys = ['dog', 'ghost', 'dzChristmas', 'sp_tower', 'sp_eleanor', 'sp_fawkes', 'sp_factory'].filter(k => char.config?.enabledSpecials?.[k]);
            const mKeys = ['clones'].filter(k => char.config?.enabledMonthly ? char.config.enabledMonthly[k] : (k === 'clones' && char.config?.clones));

            const dlNWKeys = ['dl_bro6_nw', 'dl_falkner_nw', 'dl_yellow_nw', 'dl_jenny_nw', 'dl_raven_nw', 'dl_lance_nw', 'dl_bruno_nw', 'dl_blanca_nw', 'dl_sidis', 'dl_mite_nw'].filter(k => char.config?.enabledDailies?.[k]);
            const spNWKeys = ['sp_terror_nw', 'sp_misty_nw', 'sp_lorelei_nw', 'sp_barry_nw', 'sp_subj14'].filter(k => char.config?.enabledSpecials?.[k]);
            const mnNWKeys = ['m_clones_nw', 'm_secret_lab'].filter(k => char.config?.enabledMonthly?.[k]);

            const allTasks = [...evKeys.map(k=>events[k]), ...dgKeys.map(k=>dailies[k]), ...dlKeys.map(k=>dailies[k]), ...gymKeys.map(k=>weeklies[k]), weeklies.silver, ...spKeys.map(k=>specials[k]), ...mKeys.map(k=>monthly[k]), ...dlNWKeys.map(k=>dailies[k]), ...spNWKeys.map(k=>specials[k]), ...mnNWKeys.map(k=>monthly[k])].filter(Boolean);
            
            const doneCount = allTasks.filter(t => t?.done).length;
            const pct = allTasks.length > 0 ? Math.round((doneCount / allTasks.length) * 100) : 0;
            const finStats = getFinanceStats(char.finance?.transactions);

            const card = document.createElement('div');
            card.className = "bg-slate-900 border border-slate-800 rounded-[1.5rem] p-4 flex flex-col gap-3 task-card animate-fade shadow-xl";
            card.innerHTML = `
                <div class="flex justify-between items-center text-left">
                    <div class="flex items-center gap-3">
                        <div class="${clan.color} clan-badge text-white font-black shadow-lg" title="${clan.name}">${clan.icon}</div>
                        <div>
                            <h3 id="name-${char.id}" class="text-base font-black italic uppercase text-white leading-none">${safeName}</h3>
                            <div class="flex items-center gap-1.5 mt-1 flex-wrap">
                                <span class="text-[8px] font-black px-1.5 py-0.5 rounded flex items-center gap-1 ${clan.color} bg-opacity-20 ${clan.text} ${clan.border} border border-opacity-30 shadow-sm" title="Clã ${clan.name}">${clan.icon} ${clan.name}</span>
                                <p class="text-[8px] font-bold text-slate-500 uppercase">${safeWorld} • LV <span id="lvl-${char.id}">${char.level}</span></p>
                                <button data-action="level-up" data-char-id="${char.id}" data-level="${char.level}" class="bg-blue-600/20 hover:bg-blue-500/40 text-blue-400 rounded px-1.5 py-0.5 text-[8px] font-black transition-all" title="Subir de Nível">↑</button>
                            </div>
                            <p class="text-[8px] font-bold text-amber-500/80 uppercase mt-0.5">${safeProfession} (Lv ${char.profLevel || 0})${safeSpecialization ? ` • ${safeSpecialization}` : ''} ${char.nwLevel ? `• NW Lv ${char.nwLevel}` : ''}</p>
                        </div>
                    </div>
                    <div class="flex gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 shrink-0 ml-2 transition-all">
                        <button data-action="toggle-collapse" data-char-id="${char.id}" class="text-slate-500 hover:text-white font-bold p-1.5 transition-colors" title="${isCollapsed ? 'Maximizar Personagem' : 'Minimizar Personagem'}">
                            <svg class="w-4 h-4 transform transition-transform ${isCollapsed ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg>
                        </button>
                        <div class="w-px h-4 bg-slate-800 my-auto ${isCollapsed ? 'hidden' : 'block'}"></div>
                        <button data-action="export-data" data-char-id="${char.id}" class="text-slate-500 hover:text-emerald-400 font-bold p-1.5 transition-colors ${isCollapsed ? 'hidden' : 'block'}" title="Exportar Dados">📥</button>
                        <button data-action="edit-char" data-char-id="${char.id}" class="text-slate-500 hover:text-blue-400 font-bold p-1.5 transition-colors ${isCollapsed ? 'hidden' : 'block'}" title="Editar Configurações">✏️</button>
                        <button data-action="ask-delete" data-char-id="${char.id}" class="text-slate-600 hover:text-red-500 font-bold p-1.5 transition-colors ${isCollapsed ? 'hidden' : 'block'}" title="Apagar Personagem">&times;</button>
                    </div>
                </div>

                <div id="content-${char.id}" class="${isCollapsed ? 'hidden' : 'block'} transition-all duration-300">
                    <div class="flex items-center justify-center gap-6 py-2 border-y border-slate-800/50 mt-2">
                        <div class="chart-wrapper" id="ring-${char.id}">
                            <div class="pokeball-core"><div class="pokeball-button"><span class="pokeball-pct" id="pct-text-${char.id}">0%</span></div></div>
                        </div>
                        <button data-action="reset-char" data-char-id="${char.id}" class="bg-slate-800 text-[8px] font-black uppercase px-4 py-2 rounded-lg border border-slate-700 hover:bg-slate-700 transition-all active:scale-95 shadow-lg shadow-black/20">${tStrings.reset}</button>
                    </div>

                    <div class="bg-slate-950/60 rounded-2xl p-3 border border-slate-800/80 shadow-inner my-1">
                        <div class="flex items-center justify-between mb-3 border-b border-slate-800/50 pb-2">
                            <div class="flex flex-col">
                                <span class="text-[8px] font-black text-slate-500 uppercase tracking-widest italic">${tStrings.finCurrent}</span>
                                <span class="text-sm font-black ${char.finance?.currentCash >= 0 ? 'text-emerald-400' : 'text-red-400'}">${formatK(char.finance?.currentCash || 0)}</span>
                            </div>
                            <div class="flex gap-1.5">
                                <button data-action="open-finance-modal" data-char-id="${char.id}" data-finance-type="set" class="w-6 h-6 rounded bg-blue-500/10 text-blue-400 hover:bg-blue-500/30 flex items-center justify-center transition-all shadow-sm border border-blue-500/20 active:scale-90" title="${tStrings.finSet}">✏️</button>
                                <button data-action="open-finance-modal" data-char-id="${char.id}" data-finance-type="in" class="w-6 h-6 rounded bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/30 flex items-center justify-center transition-all shadow-sm border border-emerald-500/20 active:scale-90" title="Lucro">+</button>
                                <button data-action="open-finance-modal" data-char-id="${char.id}" data-finance-type="out" class="w-6 h-6 rounded bg-red-500/10 text-red-400 hover:bg-red-500/30 flex items-center justify-center transition-all shadow-sm border border-red-500/20 active:scale-90" title="Gasto">-</button>
                                <button data-action="open-history-modal" data-char-id="${char.id}" class="w-6 h-6 rounded bg-slate-500/10 text-slate-400 hover:bg-slate-500/30 flex items-center justify-center transition-all shadow-sm border border-slate-500/20 active:scale-90" title="Histórico">📋</button>
                            </div>
                        </div>
                        <div class="grid grid-cols-3 gap-2 divide-x divide-slate-800/50 text-center">
                            <div class="flex flex-col"><span class="text-[7px] text-slate-500 uppercase font-bold tracking-widest">${tStrings.finToday}</span><span class="text-[11px] font-black tracking-tight">${formatK(finStats.d)}</span></div>
                            <div class="flex flex-col"><span class="text-[7px] text-slate-500 uppercase font-bold tracking-widest">${tStrings.finWeek}</span><span class="text-[11px] font-black tracking-tight">${formatK(finStats.w)}</span></div>
                            <div class="flex flex-col"><span class="text-[7px] text-slate-500 uppercase font-bold tracking-widest">${tStrings.finMonth}</span><span class="text-[11px] font-black tracking-tight">${formatK(finStats.m)}</span></div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left mt-3 items-start">
                        <div class="space-y-3">
                            ${char.config?.events && evKeys.length ? `<div><h4 class="text-[8px] font-black text-orange-400 uppercase italic mb-2">${tStrings.events}</h4>${renderList(char, 'events', evKeys)}</div>` : ''}
                            ${char.config?.dungeons && dgKeys.length ? `<div><h4 class="text-[8px] font-black text-red-500 uppercase italic mb-2">${tStrings.dungeons}</h4>${renderList(char, 'dailies', dgKeys)}</div>` : ''}
                            ${char.config?.dailies && dlKeys.length ? `<div><h4 class="text-[8px] font-black text-blue-500 uppercase italic mb-2">${tStrings.dailies}</h4>${renderList(char, 'dailies', dlKeys)}</div>` : ''}
                            ${char.config?.monthly && mKeys.length ? `<div><h4 class="text-[8px] font-black text-emerald-500 uppercase italic mb-2">${tStrings.clones}</h4>${renderList(char, 'monthly', mKeys)}</div>` : ''}
                        </div>
                        <div class="space-y-3">
                            ${char.config?.johto ? `<div><h4 class="text-[8px] font-black text-indigo-500 uppercase italic mb-2">${tStrings.johto}</h4>${renderList(char, 'johtoWeekly', [...gymKeys, 'silver'])}</div>` : ''}
                            ${char.config?.specials && spKeys.length ? `<div><h4 class="text-[8px] font-black text-amber-500 uppercase italic mb-2">${tStrings.specials}</h4>${renderList(char, 'specials', spKeys)}</div>` : ''}
                        </div>
                    </div>

                    ${char.level >= 300 && (dlNWKeys.length > 0 || spNWKeys.length > 0 || mnNWKeys.length > 0) ? `
                    <div class="mt-2 pt-4 border-t border-purple-900/40">
                        <h4 class="text-[9px] font-black text-purple-400 uppercase italic mb-3 tracking-widest flex items-center gap-2">
                            <span class="bg-purple-900/80 px-1.5 py-0.5 rounded border border-purple-500/50 text-[6px] text-white">NW</span> End-Game / Nightmare
                        </h4>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-start">
                            <div class="space-y-3">
                                ${dlNWKeys.length ? `<div><h5 class="text-[7px] text-slate-500 uppercase font-bold mb-1">Diárias</h5>${renderList(char, 'dailies', dlNWKeys)}</div>` : ''}
                                ${mnNWKeys.length ? `<div><h5 class="text-[7px] text-slate-500 uppercase font-bold mb-1">Mensais</h5>${renderList(char, 'monthly', mnNWKeys)}</div>` : ''}
                            </div>
                            <div class="space-y-3">
                                ${spNWKeys.length ? `<div><h5 class="text-[7px] text-slate-500 uppercase font-bold mb-1">Semanais</h5>${renderList(char, 'specials', spNWKeys)}</div>` : ''}
                            </div>
                        </div>
                    </div>
                    ` : ''}
                </div>
            `;
            grid.appendChild(card);
            
            if (!isCollapsed) {
                setTimeout(() => { animatePercentage(char.id, pct); }, 50);
            }
        });
    }

    function renderList(char, cat, filterKeys = null) {
        const items = char.tasks?.[cat] || {};
        const t = translations[currentLang];
        return Object.entries(items)
            .filter(([k]) => !filterKeys || filterKeys.includes(k))
            .map(([k, task]) => {
                const taskName = t.taskNames[k] || k.toUpperCase();
                const isNW = /nightmare|\bnw\b|ultra lab/i.test(taskName);
                const nwBadge = isNW ? `<span class="ml-1.5 inline-flex items-center justify-center bg-purple-900/80 text-purple-300 border border-purple-500/50 text-[6px] px-1 rounded-sm shadow-sm font-black uppercase tracking-widest" title="End-Game">NW</span>` : '';
                return `
            <div data-action="toggle-task" data-char-id="${char.id}" data-task-cat="${cat}" data-task-key="${k}" class="flex items-center justify-between p-2.5 mb-1.5 rounded-xl bg-slate-950/80 border border-slate-800 cursor-pointer hover:border-blue-900/50 transition-all duration-300 group">
                <div class="flex flex-col text-left">
                    <span class="text-[9px] font-black uppercase tracking-wide flex items-center ${task?.done ? 'text-slate-500 line-through' : 'text-slate-200'}">${taskName}${nwBadge}</span>
                    ${task?.done && task.at ? `
                        <div class="mt-1.5 flex flex-col gap-0.5">
                            <span class="text-[7.5px] font-bold text-emerald-500/90 uppercase tracking-widest">✓ ${t.doneAt}: ${formatDateTime(task.at)}</span>
                            <span class="text-[7.5px] font-bold text-blue-400/90 uppercase tracking-widest">⏳ ${t.resetAt}: ${getNextAvailableText(cat, task.at)}</span>
                        </div>
                    ` : ''}
                </div>
                <div class="custom-check ${task?.done ? 'active' : ''} shrink-0 ml-3"></div>
            </div>`;
            }).join('');
    }

    function animatePercentage(id, target) {
        const textEl = document.getElementById(`pct-text-${id}`);
        const ringEl = document.getElementById(`ring-${id}`);
        if (!textEl || !ringEl) return;
        let current = 0;
        const timer = setInterval(() => {
            current += (target - current) / 10 + 1;
            if (current >= target) { current = target; clearInterval(timer); }
            textEl.innerText = `${Math.floor(current)}%`;
            ringEl.style.background = `conic-gradient(#3b82f6 ${current}%, #1e293b 0)`;
            if (current === 100) ringEl.style.boxShadow = '0 0 15px rgba(59, 130, 246, 0.4)'; else ringEl.style.boxShadow = 'none';
        }, 30);
    }

    window.actions = {
        loginGoogle: async () => {
            try {
                window.ui.closeLoginModal();
                const googleProvider = new GoogleAuthProvider();
                const currentUser = auth.currentUser;
                
                if (currentUser && currentUser.isAnonymous) {
                    try {
                        await linkWithPopup(currentUser, googleProvider);
                    } catch (error) {
                        if (error.code === 'auth/credential-already-in-use') {
                            await signInWithPopup(auth, googleProvider);
                        } else {
                            console.error("Erro ao vincular:", error);
                            alert("Ocorreu um erro ao salvar na nuvem.");
                        }
                    }
                } else {
                    await signInWithPopup(auth, googleProvider);
                }
            } catch (error) {
                console.error("Erro no login:", error);
            }
        },
        logout: async () => {
            await signOut(auth);
            window.location.reload(); 
        },
        toggleCollapse: (id) => {
            const index = collapsedChars.indexOf(id);
            if (index > -1) {
                collapsedChars.splice(index, 1);
            } else {
                collapsedChars.push(id);
            }
            safeSetLocalStorage('pxg_collapsed_chars', JSON.stringify(collapsedChars));
            render(); 
        },
        toggle: async (charId, cat, key, e) => {
            const char = characters.find(c => c.id === charId);
            const status = char.tasks?.[cat]?.[key]?.done || false;
            
            if (status) {
                pendingUncheckToggle = { type: 'task', charId, cat, key, event: e };
                document.getElementById('uncheck-modal-overlay').style.display = 'flex';
                return;
            }
            await window.actions.executeToggle(charId, cat, key, false, e);
        },
        executeToggle: async (charId, cat, key, currentStatus, e) => {
            const char = characters.find(c => c.id === charId);
            const updated = { ...char.tasks };
            if (!updated[cat]) updated[cat] = {};
            
            let newScore = char.monthlyScore || 0;
            if (!currentStatus) newScore++;
            else newScore = Math.max(0, newScore - 1);

            if (!currentStatus && e) {
                const row = e.currentTarget;
                if (row) { row.classList.add('animate-task-done'); setTimeout(() => row.classList.remove('animate-task-done'), 500); }
            }

            updated[cat][key] = { done: !currentStatus, at: !currentStatus ? new Date().toISOString() : null };
            await updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', charId), { tasks: updated, monthlyScore: newScore });
        },
        exportData: (charId) => {
            const char = characters.find(c => c.id === charId);
            if (!char) return;
            const t = translations[currentLang];
            
            let content = `========================================\r\n`;
            content += `   RELATÓRIO DO TREINADOR: ${char.name.toUpperCase()}\r\n`;
            content += `========================================\r\n`;
            content += `Mundo: ${char.world} | Level: ${char.level} | Clã: ${char.clan.toUpperCase()}\r\n`;
            content += `Profissão: ${char.profession} (Lv ${char.profLevel})\r\n`;
            content += `Saldo Financeiro: ${char.finance?.currentCash || 0}K\r\n`;
            content += `Pontuação Produtiva Mensal: ${char.monthlyScore || 0} pts\r\n\r\n`;

            content += `--- TAREFAS CONCLUÍDAS ---\r\n`;
            
            let hasTasks = false;
            const cats = ['events', 'dailies', 'johtoWeekly', 'specials', 'monthly'];
            cats.forEach(cat => {
                if(char.tasks && char.tasks[cat]) {
                    Object.entries(char.tasks[cat]).forEach(([k, task]) => {
                        if(task.done) {
                            hasTasks = true;
                            const tName = t.taskNames[k] || k;
                            content += `[✓] ${tName}  (Feito em: ${formatDateTime(task.at)})\r\n`;
                        }
                    });
                }
            });

            if (!hasTasks) content += `Nenhuma tarefa concluída no momento.\r\n`;
            content += `\r\nGerado em: ${new Date().toLocaleString('pt-PT')} pelo PXG Check\r\n`;
            
            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const safeDownloadName = String(char.name || 'trainer').replace(/[^a-zA-Z0-9_-]/g, '_');
            a.download = `PXG_Tracker_${safeDownloadName}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },
        levelUp: async (charId, currentLevel, e) => {
            if(e) e.stopPropagation();
            const charCard = document.getElementById(`lvl-${charId}`)?.closest('.task-card');
            const charName = document.getElementById(`name-${charId}`);
            if (charCard) { charCard.classList.add('animate-level-up'); setTimeout(() => charCard.classList.remove('animate-level-up'), 1000); }
            if (charName) { charName.classList.add('animate-text-glow'); setTimeout(() => charName.classList.remove('animate-text-glow'), 1000); }
            await updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', charId), { level: currentLevel + 1 });
        },
        reset: async (charId) => {
            const char = characters.find(c => c.id === charId);
            const updated = { ...char.tasks };
            ['dailies', 'events', 'johtoWeekly', 'monthly', 'specials'].forEach(cat => {
                if(updated[cat]) Object.keys(updated[cat]).forEach(k => updated[cat][k] = { done: false, at: null });
            });
            await updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', charId), { tasks: updated });
        },
        submitFinance: async (e) => {
            e.preventDefault();
            const charId = document.getElementById('fin-char-id').value;
            const type = document.getElementById('fin-type').value;
            const val = parseInt(document.getElementById('fin-value').value);
            const reason = document.getElementById('fin-reason').value.trim() || 'Sem observação';
            if(isNaN(val) || val < 0) return;

            const char = characters.find(c => c.id === charId);
            let finance = char.finance || { transactions: [], currentCash: 0 };
            let transactions = finance.transactions || [];
            const cutoff = new Date(); cutoff.setDate(cutoff.getDate() - 45);
            transactions = transactions.filter(t => new Date(t.date) > cutoff);

            let realVal = val; if (type === 'out') realVal = -val;
            if (type === 'set') { finance.currentCash = val; transactions.push({ type: 'set', val: val, reason: `Ajuste: ${reason}`, date: new Date().toISOString() }); }
            else { finance.currentCash = (finance.currentCash || 0) + realVal; transactions.push({ type: type, val: realVal, reason: reason, date: new Date().toISOString() }); }

            await updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', charId), { 'finance': { transactions: transactions, currentCash: finance.currentCash } });
            window.ui.closeFinanceModal();
        },
        askDelete: (id) => { characterToDelete = id; document.getElementById('delete-modal-overlay').style.display = 'flex'; },
        confirmDelete: async () => {
            if (!characterToDelete) return;
            try { await deleteDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', characterToDelete)); } catch (e) {} finally { window.ui.closeDeleteModal(); }
        },
        deleteFeedback: async (feedbackId) => {
            // Usa uma modal simples do navegador como segurança antes de apagar o ticket
            try {
                await deleteDoc(doc(db, 'artifacts', DB_COLLECTION, 'public', 'data', 'feedbacks', feedbackId));
            } catch (e) {
                console.error("Erro ao apagar ticket", e);
            }
        },
        executeOrbToggle: (id) => {
            const index = userOrbsProgress.indexOf(id);
            if (index > -1) userOrbsProgress.splice(index, 1);
            else userOrbsProgress.push(id);
            
            safeSetLocalStorage('pxg_rainbow_orbs', JSON.stringify(userOrbsProgress));
            const filterText = document.getElementById('orb-search').value;
            renderOrbsList(filterText);
        },
        toggleOrb: (id, e) => {
            if(e.target.tagName.toLowerCase() === 'svg' || e.target.tagName.toLowerCase() === 'path' || e.target.tagName.toLowerCase() === 'button') return;
            
            const index = userOrbsProgress.indexOf(id);
            if (index > -1) {
                pendingUncheckToggle = { type: 'orb', id: id, event: e };
                document.getElementById('uncheck-modal-overlay').style.display = 'flex';
                return;
            }
            window.actions.executeOrbToggle(id);
        },
        markAllOrbs: (region, e) => {
            if (e) e.stopPropagation(); 
            const orbsInRegion = rainbowOrbs.filter(o => o.location === region);
            let updated = false;
            
            orbsInRegion.forEach(orb => {
                if (!userOrbsProgress.includes(orb.id)) {
                    userOrbsProgress.push(orb.id);
                    updated = true;
                }
            });
            
            if (updated) {
                safeSetLocalStorage('pxg_rainbow_orbs', JSON.stringify(userOrbsProgress));
                renderOrbsList(document.getElementById('orb-search')?.value || '');
            }
        },
        copyCoords: (text, e) => {
            e.stopPropagation(); 
            const textArea = document.createElement("textarea");
            textArea.value = text; 
            textArea.style.position = "fixed"; 
            textArea.style.left = "-999999px";
            document.body.appendChild(textArea); 
            textArea.focus(); 
            textArea.select();
            try { document.execCommand('copy'); } catch (err) {} 
            textArea.remove();
            
            const btn = e.currentTarget;
            const originalHTML = btn.innerHTML;
            btn.innerHTML = `<svg class="w-3 h-3 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>`;
            setTimeout(() => { btn.innerHTML = originalHTML; }, 2000);
        },
        copyPix: (e) => {
            const key = document.getElementById('pix-key').innerText;
            const textArea = document.createElement("textarea");
            textArea.value = key; textArea.style.position = "fixed"; textArea.style.left = "-999999px";
            document.body.appendChild(textArea); textArea.focus(); textArea.select();
            try { document.execCommand('copy'); } catch (err) {} textArea.remove();
            const btn = e.currentTarget;
            btn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>`;
            setTimeout(() => { btn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>`; }, 2000);
        },
        toggleNotifications: async () => {
            if (!("Notification" in window)) {
                alert("O seu navegador não suporta notificações.");
                return;
            }
            if (Notification.permission === "granted") {
                notificationsEnabled = !notificationsEnabled;
                safeSetLocalStorage('pxg_notifications', String(notificationsEnabled));
                window.ui.updateNotificationIcon();
            } else if (Notification.permission !== "denied") {
                const permission = await Notification.requestPermission();
                if (permission === "granted") {
                    notificationsEnabled = true;
                    safeSetLocalStorage('pxg_notifications', 'true');
                    window.ui.updateNotificationIcon();
                }
            } else {
                alert("As notificações estão bloqueadas. Permita nas configurações do seu navegador para usar o recurso.");
            }
        }
    };

    window.ui = {
        setLanguage: (lang) => { currentLang = lang; safeSetLocalStorage('pxg_lang', lang); render(); },
        checkLevel: (val) => {
            const lvl = parseInt(val) || 0;
            const endG = document.getElementById('end-game-section');
            const nwLvl = document.getElementById('nw-level-container');
            if (lvl >= 300) { endG.classList.remove('hidden'); nwLvl.classList.remove('hidden'); } 
            else { endG.classList.add('hidden'); nwLvl.classList.add('hidden'); }
        },
        checkProfession: () => {
            const profEl = document.getElementById('prof-select');
            const lvlEl = document.getElementById('prof-level-input');
            const specContainer = document.getElementById('spec-container');
            const specSelect = document.getElementById('spec-select');
            if (!profEl || !lvlEl || !specContainer || !specSelect) return;

            const prof = profEl.value;
            const lvl = parseInt(lvlEl.value) || 1;

            if (lvl >= 100) {
                specContainer.classList.remove('hidden');
                const currentSpec = specSelect.value;
                
                let options = '<option value="">Nenhuma</option>';
                if (prof === 'Professor') options += '<option value="Alquimista">Alquimista</option><option value="Acadêmico">Acadêmico</option>';
                else if (prof === 'Estilista') options += '<option value="Designer">Designer</option><option value="Decorador">Decorador</option>';
                else if (prof === 'Engenheiro') options += '<option value="Hacker">Hacker</option><option value="Mecânico">Mecânico</option>';
                else if (prof === 'Aventureiro') options += '<option value="Arqueólogo">Arqueólogo</option><option value="Cozinheiro">Cozinheiro</option>';
                
                specSelect.innerHTML = options;
                
                if (Array.from(specSelect.options).some(opt => opt.value === currentSpec)) {
                    specSelect.value = currentSpec;
                }
            } else {
                specContainer.classList.add('hidden');
                specSelect.value = '';
            }
        },
        openModal: (editId = null) => { 
            const form = document.getElementById('add-char-form'); form.reset();
            document.getElementById('edit-char-id').value = '';
            document.getElementById('modal-title').innerText = 'Novo Treinador';
            document.getElementById('btn-save').innerText = 'Salvar Treinador';
            window.ui.checkLevel(0); window.ui.renderClanDropdown(); window.ui.checkProfession();

            const defClan = clanData.volcanic;
            document.getElementById('selected-clan-input').value = 'volcanic';
            document.getElementById('current-clan-name').innerText = defClan.name;
            const defIcon = document.getElementById('current-clan-icon');
            defIcon.className = `${defClan.color} clan-badge-small text-[10px]`; defIcon.innerText = defClan.icon;

            if (editId) {
                const char = characters.find(c => c.id === editId);
                if (char) {
                    document.getElementById('edit-char-id').value = char.id;
                    document.getElementById('modal-title').innerText = 'Editar Treinador';
                    document.getElementById('btn-save').innerText = 'Atualizar Treinador';
                    form.elements['name'].value = char.name; form.elements['level'].value = char.level;
                    form.elements['world'].value = char.world; form.elements['profession'].value = char.profession || 'Professor';
                    form.elements['profLevel'].value = char.profLevel || 1;
                    window.ui.checkProfession();
                    if(char.specialization) form.elements['specialization'].value = char.specialization;
                    if(char.nwLevel) form.elements['nwLevel'].value = char.nwLevel;
                    
                    const clanKey = char.clan ? char.clan.toLowerCase() : 'volcanic';
                    const cData = clanData[clanKey] || clanData.volcanic;
                    document.getElementById('selected-clan-input').value = clanKey; document.getElementById('current-clan-name').innerText = cData.name;
                    const iconEl = document.getElementById('current-clan-icon');
                    iconEl.className = `${cData.color} clan-badge-small text-[10px]`; iconEl.innerText = cData.icon;
                    window.ui.checkLevel(char.level);
                    if(char.config) {
                        if(char.config.events !== undefined) form.elements['monitor_events'].checked = char.config.events;
                        if(char.config.dungeons !== undefined) form.elements['monitor_dungeons'].checked = char.config.dungeons;
                    }
                }
            }
            document.getElementById('modal-overlay').style.display = 'flex'; 
        },
        closeModal: () => document.getElementById('modal-overlay').style.display = 'none',
        openFinanceModal: (charId, type) => {
            document.getElementById('fin-char-id').value = charId; document.getElementById('fin-type').value = type;
            document.getElementById('fin-value').value = ''; document.getElementById('fin-reason').value = '';
            const btn = document.getElementById('fin-submit-btn'); const titleEl = document.getElementById('finance-title');
            if (type === 'set') { titleEl.innerText = 'Definir Saldo Atual'; btn.className = "w-full bg-blue-600 hover:bg-blue-500 text-white font-black py-4 rounded-xl shadow-lg uppercase tracking-widest text-[10px] mt-2 transition-all active:scale-95"; } 
            else if (type === 'in') { titleEl.innerText = 'Adicionar Lucro'; btn.className = "w-full bg-emerald-600 hover:bg-emerald-500 text-white font-black py-4 rounded-xl shadow-lg uppercase tracking-widest text-[10px] mt-2 transition-all active:scale-95"; } 
            else { titleEl.innerText = 'Adicionar Gasto'; btn.className = "w-full bg-red-600 hover:bg-red-500 text-white font-black py-4 rounded-xl shadow-lg uppercase tracking-widest text-[10px] mt-2 transition-all active:scale-95"; }
            document.getElementById('finance-modal-overlay').style.display = 'flex';
        },
        closeFinanceModal: () => { document.getElementById('finance-modal-overlay').style.display = 'none'; },
        openHistoryModal: (charId) => {
            const char = characters.find(c => c.id === charId); const listEl = document.getElementById('history-list'); listEl.innerHTML = '';
            const txs = char?.finance?.transactions || [];
            if (txs.length === 0) { listEl.innerHTML = '<p class="text-xs text-slate-500 text-center italic mt-4">Nenhuma transação registada.</p>'; } 
            else {
                const sortedTxs = [...txs].sort((a, b) => new Date(b.date) - new Date(a.date));
                sortedTxs.forEach(t => {
                    const isSet = t.type === 'set'; const isNeg = t.val < 0; const color = isSet ? 'text-blue-400' : (isNeg ? 'text-red-400' : 'text-emerald-400'); const sign = isSet ? '=' : (isNeg ? '' : '+');
                    listEl.innerHTML += `<div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center"><div class="flex flex-col"><span class="text-[10px] font-black text-slate-300">${t.reason}</span><span class="text-[8px] font-bold text-slate-500 mt-1">${formatDateTime(t.date)}</span></div><span class="text-xs font-black ${color}">${sign}${t.val}K</span></div>`;
                });
            }
            document.getElementById('history-modal-overlay').style.display = 'flex';
        },
        closeHistoryModal: () => { document.getElementById('history-modal-overlay').style.display = 'none'; },
        closeDeleteModal: () => { characterToDelete = null; document.getElementById('delete-modal-overlay').style.display = 'none'; },
        
        openLoginModal: () => document.getElementById('login-modal-overlay').style.display = 'flex',
        closeLoginModal: () => document.getElementById('login-modal-overlay').style.display = 'none',
        closeUncheckModal: () => { pendingUncheckToggle = null; document.getElementById('uncheck-modal-overlay').style.display = 'none'; },
        openPixModal: () => document.getElementById('pix-modal-overlay').style.display = 'flex',
        closePixModal: () => document.getElementById('pix-modal-overlay').style.display = 'none',
        openFeedbackModal: () => document.getElementById('feedback-modal-overlay').style.display = 'flex',
        closeFeedbackModal: () => document.getElementById('feedback-modal-overlay').style.display = 'none',
        openChangelog: () => document.getElementById('changelog-modal-overlay').style.display = 'flex',
        closeChangelog: () => document.getElementById('changelog-modal-overlay').style.display = 'none',

        toggleClanDropdown: () => document.getElementById('clan-options-list').classList.toggle('hidden'),
        toggleSubGrid: (cb, id) => { const el = document.getElementById(id); cb.checked ? el.classList.remove('opacity-30') : el.classList.add('opacity-30'); },
        
        toggleNavMenu: (e) => {
            if (e) e.stopPropagation();
            const list = document.getElementById('nav-dropdown-list');
            const chevron = document.getElementById('nav-chevron');
            if (list.classList.contains('hidden')) {
                list.classList.remove('hidden');
                chevron.style.transform = 'rotate(180deg)';
            } else {
                list.classList.add('hidden');
                chevron.style.transform = 'rotate(0deg)';
            }
        },

        renderClanDropdown: () => {
            const list = document.getElementById('clan-options-list'); list.innerHTML = '';
            Object.entries(clanData).forEach(([key, data]) => {
                const opt = document.createElement('button'); opt.type = 'button'; opt.className = "w-full text-left p-2 rounded hover:bg-slate-800 transition-all flex items-center gap-2";
                opt.onclick = () => { 
                    document.getElementById('selected-clan-input').value = key; document.getElementById('current-clan-name').innerText = data.name; 
                    const iconEl = document.getElementById('current-clan-icon');
                    iconEl.className = `${data.color} clan-badge-small text-[10px]`; iconEl.innerText = data.icon;
                    document.getElementById('clan-options-list').classList.add('hidden'); 
                };
                opt.innerHTML = `<span class="w-5 h-5 rounded flex items-center justify-center text-[10px] ${data.color}">${data.icon}</span><span class="text-[9px] uppercase font-black">${data.name}</span>`;
                list.appendChild(opt);
            });
        },
        switchTab: (tabName) => {
            if (tabName === 'orbs') ensureOrbsLoaded();
            const views = { 
                chars: document.getElementById('view-chars'), 
                orbs: document.getElementById('view-orbs'), 
                ranking: document.getElementById('view-ranking'), 
                guides: document.getElementById('view-guides'),
                about: document.getElementById('view-about'),
                admin: document.getElementById('view-admin'),
                pokelog: document.getElementById('view-pokelog') 
            };
            
            const labels = { 
                chars: 'Treinadores', 
                orbs: 'Rainbow Orbs', 
                ranking: 'Ranking', 
                guides: 'Guias F2P',
                about: 'Sobre o Projeto',
                admin: 'Painel Admin',
                pokelog: 'Pokélog (Game)'
            };
            const labelEl = document.getElementById('nav-current-label');
            if(labelEl && labels[tabName]) labelEl.innerText = labels[tabName];

            const list = document.getElementById('nav-dropdown-list');
            const chevron = document.getElementById('nav-chevron');
            if (list && !list.classList.contains('hidden')) {
                list.classList.add('hidden');
                if(chevron) chevron.style.transform = 'rotate(0deg)';
            }

            Object.keys(views).forEach(key => {
                if(views[key]) {
                    if(key === tabName) {
                        views[key].classList.remove('hidden'); views[key].classList.add('block');
                    } else {
                        views[key].classList.remove('block'); views[key].classList.add('hidden');
                    }
                }
            });
        },
        filterGuides: () => {
            const term = (document.getElementById('guide-search')?.value || '').toLowerCase();
            debounceFilterGuides(term);
        },
        filterOrbs: () => {
            const filterText = document.getElementById('orb-search')?.value || '';
            debounceFilterOrbs(filterText);
        },
        updateNotificationIcon: () => {
            const bells = document.querySelectorAll('.notification-bell');
            const permission = ("Notification" in window) ? Notification.permission : 'unsupported';
            bells.forEach(bell => {
                if (notificationsEnabled) {
                    bell.classList.remove('text-slate-500');
                    bell.classList.add('text-amber-400');
                } else {
                    bell.classList.remove('text-amber-400');
                    bell.classList.add('text-slate-500');
                }

                if (permission === 'denied') {
                    bell.classList.remove('text-amber-400');
                    bell.classList.add('text-red-400');
                    bell.title = 'Notificações bloqueadas no navegador';
                } else if (permission === 'granted' && notificationsEnabled) {
                    bell.title = 'Alertas ativos (Boss/Poképark)';
                } else if (permission === 'default') {
                    bell.title = 'Clique para permitir notificações';
                }
            });
        }
    };

    const debounceFilterGuides = debounce((term) => {
            const guides = document.querySelectorAll('.f2p-guide-card');
            guides.forEach(guide => {
                const text = guide.innerText.toLowerCase();
                guide.style.display = text.includes(term) ? 'block' : 'none';
            });
    }, 180);

    const debounceFilterOrbs = debounce((filterText) => {
        renderOrbsList(filterText);
    }, 200);

    window.ui.toggleGuide = (el) => {
        const card = el.closest('.f2p-guide-card');
        const content = card.querySelector('.guide-content');
        const chevron = el.querySelector('.chevron');
        const extras = el.querySelectorAll('.guide-extra');
        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            chevron.style.transform = 'rotate(180deg)';
            extras.forEach(e => e.classList.remove('hidden'));
        } else {
            content.classList.add('hidden');
            chevron.style.transform = 'rotate(0deg)';
            extras.forEach(e => e.classList.add('hidden'));
        }
    };

    function bindStaticControls() {
        document.getElementById('btn-notifications-desktop')?.addEventListener('click', () => window.actions.toggleNotifications());
        document.getElementById('btn-notifications-mobile')?.addEventListener('click', () => window.actions.toggleNotifications());
        document.getElementById('btn-nav-menu')?.addEventListener('click', (event) => window.ui.toggleNavMenu(event));
        document.getElementById('btn-add-top')?.addEventListener('click', () => window.ui.openModal());
        document.getElementById('btn-force-update')?.addEventListener('click', () => window.forceUpdate());
        document.getElementById('btn-login-google')?.addEventListener('click', () => window.actions.loginGoogle());
        document.getElementById('btn-close-login-modal')?.addEventListener('click', () => window.ui.closeLoginModal());
        document.getElementById('btn-close-uncheck-modal')?.addEventListener('click', () => window.ui.closeUncheckModal());
        document.getElementById('btn-copy-pix')?.addEventListener('click', (event) => window.actions.copyPix(event));
        document.getElementById('btn-close-pix-modal')?.addEventListener('click', () => window.ui.closePixModal());
        document.getElementById('btn-close-feedback-modal')?.addEventListener('click', () => window.ui.closeFeedbackModal());
        document.getElementById('btn-close-modal')?.addEventListener('click', () => window.ui.closeModal());
        document.getElementById('btn-close-finance-modal')?.addEventListener('click', () => window.ui.closeFinanceModal());
        document.getElementById('btn-close-history-modal')?.addEventListener('click', () => window.ui.closeHistoryModal());
        document.getElementById('btn-close-changelog-modal')?.addEventListener('click', () => window.ui.closeChangelog());
        document.getElementById('btn-open-feedback-modal')?.addEventListener('click', () => window.ui.openFeedbackModal());
        document.getElementById('btn-open-pix-modal')?.addEventListener('click', () => window.ui.openPixModal());
        document.getElementById('btn-open-changelog-modal')?.addEventListener('click', () => window.ui.openChangelog());
        document.getElementById('btn-no')?.addEventListener('click', () => window.ui.closeDeleteModal());
        document.getElementById('event-visual-alert')?.addEventListener('click', () => {
            const visualAlert = document.getElementById('event-visual-alert');
            if (!visualAlert) return;
            visualAlert.classList.remove('flex');
            visualAlert.classList.add('hidden');
        });

        document.getElementById('orb-search')?.addEventListener('input', () => window.ui.filterOrbs());
        document.getElementById('guide-search')?.addEventListener('input', () => window.ui.filterGuides());
        document.getElementById('level-input')?.addEventListener('input', (event) => window.ui.checkLevel(event.target.value));
        document.getElementById('prof-select')?.addEventListener('change', () => window.ui.checkProfession());
        document.getElementById('prof-level-input')?.addEventListener('input', () => window.ui.checkProfession());
        document.getElementById('clan-select-button')?.addEventListener('click', () => window.ui.toggleClanDropdown());

        document.querySelectorAll('[data-tab]').forEach((button) => {
            button.addEventListener('click', () => window.ui.switchTab(button.dataset.tab));
        });

        document.querySelectorAll('.guide-toggle').forEach((toggle) => {
            toggle.addEventListener('click', () => window.ui.toggleGuide(toggle));
        });

        document.querySelectorAll('[data-subgrid-target]').forEach((checkbox) => {
            checkbox.addEventListener('change', () => window.ui.toggleSubGrid(checkbox, checkbox.dataset.subgridTarget));
        });
    }

    document.addEventListener('click', (event) => {
        const actionable = event.target.closest('[data-action]');
        if (!actionable) return;

        const action = actionable.getAttribute('data-action');

        if (action === 'mark-all-orbs') {
            const region = decodeURIComponent(actionable.getAttribute('data-region') || '');
            window.actions.markAllOrbs(region, event);
            return;
        }

        if (action === 'toggle-orb') {
            const orbId = parseInt(actionable.getAttribute('data-orb-id') || '0', 10);
            if (orbId) window.actions.toggleOrb(orbId, event);
            return;
        }

        if (action === 'copy-orb-coords') {
            const coords = decodeURIComponent(actionable.getAttribute('data-coords') || '');
            window.actions.copyCoords(coords, event);
            return;
        }

        if (action === 'logout') {
            window.actions.logout();
            return;
        }

        if (action === 'open-login-modal') {
            window.ui.openLoginModal();
            return;
        }

        if (action === 'delete-feedback') {
            const feedbackId = actionable.getAttribute('data-feedback-id') || '';
            if (feedbackId) window.actions.deleteFeedback(feedbackId);
            return;
        }

        if (action === 'open-modal-new') {
            window.ui.openModal();
            return;
        }

        if (action === 'level-up') {
            const charId = actionable.getAttribute('data-char-id') || '';
            const level = parseInt(actionable.getAttribute('data-level') || '0', 10);
            if (charId) window.actions.levelUp(charId, level, event);
            return;
        }

        if (action === 'toggle-collapse') {
            const charId = actionable.getAttribute('data-char-id') || '';
            if (charId) window.actions.toggleCollapse(charId);
            return;
        }

        if (action === 'export-data') {
            const charId = actionable.getAttribute('data-char-id') || '';
            if (charId) window.actions.exportData(charId);
            return;
        }

        if (action === 'edit-char') {
            const charId = actionable.getAttribute('data-char-id') || '';
            window.ui.openModal(charId || null);
            return;
        }

        if (action === 'ask-delete') {
            const charId = actionable.getAttribute('data-char-id') || '';
            if (charId) window.actions.askDelete(charId);
            return;
        }

        if (action === 'reset-char') {
            const charId = actionable.getAttribute('data-char-id') || '';
            if (charId) window.actions.reset(charId);
            return;
        }

        if (action === 'open-finance-modal') {
            const charId = actionable.getAttribute('data-char-id') || '';
            const finType = actionable.getAttribute('data-finance-type') || 'set';
            if (charId) window.ui.openFinanceModal(charId, finType);
            return;
        }

        if (action === 'open-history-modal') {
            const charId = actionable.getAttribute('data-char-id') || '';
            if (charId) window.ui.openHistoryModal(charId);
            return;
        }

        if (action === 'toggle-task') {
            const charId = actionable.getAttribute('data-char-id') || '';
            const cat = actionable.getAttribute('data-task-cat') || '';
            const key = actionable.getAttribute('data-task-key') || '';
            if (charId && cat && key) window.actions.toggle(charId, cat, key, event);
            return;
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindStaticControls, { once: true });
    } else {
        bindStaticControls();
    }

    document.addEventListener('error', (event) => {
        const target = event.target;
        if (!(target instanceof HTMLImageElement)) return;
        if (!target.classList.contains('auth-avatar')) return;
        const fallback = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png';
        if (target.src !== fallback) target.src = fallback;
    }, true);

    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    if(confirmDeleteBtn) confirmDeleteBtn.onclick = window.actions.confirmDelete;

    const financeForm = document.getElementById('finance-form');
    if(financeForm) financeForm.onsubmit = window.actions.submitFinance;

    const confirmUncheckBtn = document.getElementById('confirm-uncheck-btn');
    if(confirmUncheckBtn) {
        confirmUncheckBtn.onclick = async () => {
            if (!pendingUncheckToggle) return;
            if (pendingUncheckToggle.type === 'orb') { window.actions.executeOrbToggle(pendingUncheckToggle.id); } 
            else { const { charId, cat, key, event } = pendingUncheckToggle; await window.actions.executeToggle(charId, cat, key, true, event); }
            window.ui.closeUncheckModal();
        };
    }

    const feedbackForm = document.getElementById('feedback-form');
    if(feedbackForm) {
        feedbackForm.onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.getElementById('fb-submit-btn'); const type = document.getElementById('fb-type').value; const text = document.getElementById('fb-text').value; const oldText = btn.innerText;
            const normalizedText = text.trim();
            if (normalizedText.length < 8 || normalizedText.length > 1000) {
                btn.innerText = 'Texto inválido (8-1000)';
                btn.classList.add('bg-red-600');
                setTimeout(() => { btn.innerText = oldText; btn.classList.remove('bg-red-600'); }, 2200);
                return;
            }
            
            // Garantia de Segurança: Tenta autenticar anonimamente caso o navegador tenha bloqueado a sessão inicial
            if (!auth.currentUser) {
                try { await signInAnonymously(auth); } 
                catch (err) {
                    btn.innerText = 'Aba Anônima Bloqueada!'; btn.classList.add('bg-red-600');
                    setTimeout(() => { btn.innerText = oldText; btn.classList.remove('bg-red-600'); }, 3000);
                    return;
                }
            }

            try {
                btn.innerText = 'A enviar...';
                await addDoc(collection(db, 'artifacts', DB_COLLECTION, 'public', 'data', 'feedbacks'), { uid: auth.currentUser?.uid || 'anonimo', type: type, text: normalizedText, dataLeituraFacil: new Date().toLocaleString(currentLang === 'pt' ? 'pt-PT' : 'en-US'), date: new Date().toISOString() });
                btn.innerText = 'Recebido com Sucesso! ✓'; btn.classList.add('bg-emerald-600');
                setTimeout(() => { window.ui.closeFeedbackModal(); document.getElementById('fb-text').value = ''; btn.innerText = oldText; btn.classList.remove('bg-emerald-600'); }, 2000);
            } catch (err) { 
                btn.innerText = 'Erro de Segurança (Aba Anônima?)'; btn.classList.add('bg-red-600'); 
                setTimeout(() => { btn.innerText = oldText; btn.classList.remove('bg-red-600'); }, 3000); 
            }
        };
    }

    const addCharForm = document.getElementById('add-char-form');
    if(addCharForm) {
        addCharForm.onsubmit = async (e) => {
            e.preventDefault();
            const fd = new FormData(e.target);
            const editId = document.getElementById('edit-char-id').value;

            const config = { 
                events: fd.get('monitor_events')==='on', dungeons: fd.get('monitor_dungeons')==='on', dailies: fd.get('monitor_dailies')==='on', johto: fd.get('monitor_johto')==='on', monthly: fd.get('monitor_monthly')==='on', specials: fd.get('monitor_specials')==='on', quests: fd.get('monitor_quests')==='on',
                enabledEvents: { boss: fd.get('ev_boss')==='on', park: fd.get('ev_park')==='on' },
                enabledDungeons: { blue: fd.get('dg_blue')==='on', red: fd.get('dg_red')==='on' },
                enabledDailies: { catch1: fd.get('dl_catch1')==='on', catch2: fd.get('dl_catch2')==='on', task: fd.get('dl_task')==='on', dl_bro12: fd.get('dl_bro12')==='on', dl_bro6_nw: fd.get('dl_bro6_nw')==='on', dl_falkner_nw: fd.get('dl_falkner_nw')==='on', dl_yellow_nw: fd.get('dl_yellow_nw')==='on', dl_jenny_nw: fd.get('dl_jenny_nw')==='on', dl_raven_nw: fd.get('dl_raven_nw')==='on', dl_lance_nw: fd.get('dl_lance_nw')==='on', dl_bruno_nw: fd.get('dl_bruno_nw')==='on', dl_blanca_nw: fd.get('dl_blanca_nw')==='on', dl_sidis: fd.get('dl_sidis')==='on', dl_mite_nw: fd.get('dl_mite_nw')==='on' },
                enabledGyms: { violet: fd.get('gym_violet')==='on', azalea: fd.get('gym_azalea')==='on', goldenrod: fd.get('gym_goldenrod')==='on', ecruteak: fd.get('gym_ecruteak')==='on', cianwood: fd.get('gym_cianwood')==='on', olivine: fd.get('gym_olivine')==='on', mahogany: fd.get('gym_mahogany')==='on', blackthorn: fd.get('gym_blackthorn')==='on' },
                enabledSpecials: { dog: fd.get('sp_dog')==='on', ghost: fd.get('sp_ghost')==='on', dzChristmas: fd.get('sp_dz_christmas')==='on', sp_tower: fd.get('sp_tower')==='on', sp_terror_nw: fd.get('sp_terror_nw')==='on', sp_eleanor: fd.get('sp_eleanor')==='on', sp_fawkes: fd.get('sp_fawkes')==='on', sp_factory: fd.get('sp_factory')==='on', sp_misty_nw: fd.get('sp_misty_nw')==='on', sp_lorelei_nw: fd.get('sp_lorelei_nw')==='on', sp_subj14: fd.get('sp_subj14')==='on', sp_barry_nw: fd.get('sp_barry_nw')==='on' },
                enabledMonthly: { clones: fd.get('m_clones')==='on', m_secret_lab: fd.get('m_secret_lab')==='on', m_clones_nw: fd.get('m_clones_nw')==='on' },
                enabledQuests: { qCyber: fd.get('q_cyber')==='on', qMewtwo: fd.get('q_mewtwo')==='on', qTimeTravel: fd.get('q_time_travel')==='on', qTrevo: fd.get('q_trevo')==='on', qOrbs: fd.get('q_orbs')==='on', qSarkies: fd.get('q_sarkies')==='on', qTransporteNW: fd.get('q_transporte_nw')==='on', qKoga: fd.get('q_koga')==='on', qLabNW: fd.get('q_lab_nw')==='on' }
            };

            const profLvl = parseInt(fd.get('profLevel')) || 1;
            const charData = { name: fd.get('name'), level: parseInt(fd.get('level')), world: fd.get('world'), clan: fd.get('clan'), profession: fd.get('profession'), profLevel: profLvl, specialization: profLvl >= 100 ? fd.get('specialization') : '', nwLevel: parseInt(fd.get('nwLevel')) || null, config: config };

        if (editId) {
            const existingChar = characters.find(c => c.id === editId);
            const updatedTasks = { ...existingChar.tasks };
            const baseStructure = { events: ['boss12', 'boss16', 'boss20', 'boss23', 'park11', 'park15', 'park21'], dailies: ['blue', 'red', 'catch1', 'catch2', 'task', 'dl_bro12', 'dl_bro6_nw', 'dl_falkner_nw', 'dl_yellow_nw', 'dl_jenny_nw', 'dl_raven_nw', 'dl_lance_nw', 'dl_bruno_nw', 'dl_blanca_nw', 'dl_sidis', 'dl_mite_nw'], johtoWeekly: ['silver', 'violet', 'azalea', 'goldenrod', 'ecruteak', 'cianwood', 'olivine', 'mahogany', 'blackthorn'], monthly: ['clones', 'm_secret_lab', 'm_clones_nw'], specials: ['dog', 'ghost', 'dzChristmas', 'sp_tower', 'sp_terror_nw', 'sp_eleanor', 'sp_fawkes', 'sp_factory', 'sp_misty_nw', 'sp_lorelei_nw', 'sp_subj14', 'sp_barry_nw'], quests: ['qCyber', 'qMewtwo', 'qTimeTravel', 'qTrevo', 'qOrbs', 'qSarkies', 'qTransporteNW', 'qKoga', 'qLabNW'] };
            Object.keys(baseStructure).forEach(cat => { if(!updatedTasks[cat]) updatedTasks[cat] = {}; baseStructure[cat].forEach(k => { if(!updatedTasks[cat][k]) updatedTasks[cat][k] = {done: false, at: null}; }); });
            charData.tasks = updatedTasks;
            await updateDoc(doc(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters', editId), charData);
        } else {
            charData.tasks = { events: { boss12:{done:false}, boss16:{done:false}, boss20:{done:false}, boss23:{done:false}, park11:{done:false}, park15:{done:false}, park21:{done:false} }, dailies: { blue: {done:false}, red: {done:false}, catch1: {done:false}, catch2: {done:false}, task: {done:false}, dl_bro12: {done:false}, dl_bro6_nw: {done:false}, dl_falkner_nw: {done:false}, dl_yellow_nw: {done:false}, dl_jenny_nw: {done:false}, dl_raven_nw: {done:false}, dl_lance_nw: {done:false}, dl_bruno_nw: {done:false}, dl_blanca_nw: {done:false}, dl_sidis: {done:false}, dl_mite_nw: {done:false} }, johtoWeekly: { silver: {done:false}, violet:{done:false}, azalea:{done:false}, goldenrod:{done:false}, ecruteak:{done:false}, cianwood:{done:false}, olivine:{done:false}, mahogany:{done:false}, blackthorn:{done:false} }, monthly: { clones: {done:false}, m_secret_lab: {done:false}, m_clones_nw: {done:false} }, specials: { dog: {done:false}, ghost: {done:false}, dzChristmas: {done:false}, sp_tower: {done:false}, sp_terror_nw: {done:false}, sp_eleanor: {done:false}, sp_fawkes: {done:false}, sp_factory: {done:false}, sp_misty_nw: {done:false}, sp_lorelei_nw: {done:false}, sp_subj14: {done:false}, sp_barry_nw: {done:false} }, quests: { qCyber: {done:false}, qMewtwo: {done:false}, qTimeTravel: {done:false}, qTrevo: {done:false}, qOrbs: {done:false}, qSarkies: {done:false}, qTransporteNW: {done:false}, qKoga: {done:false}, qLabNW: {done:false} } };
            charData.finance = { transactions: [], currentCash: 0 }; charData.monthlyScore = 0; charData.scoreMonth = `${new Date().getFullYear()}-${new Date().getMonth() + 1}`;
            await addDoc(collection(db, 'artifacts', DB_COLLECTION, 'users', auth.currentUser.uid, 'characters'), charData);
        }
        window.ui.closeModal();
    };
    }

    function updateUITexts() {
        const t = translations[currentLang];
        document.getElementById('btn-add-top').innerText = t.add; document.getElementById('page-subtitle').innerText = t.subtitle; document.getElementById('loading-text').innerText = t.loading;
    }
    function hideLoader() { document.getElementById('loading-spinner').style.display = 'none'; }
    
    // =========================================================================
    // 🌐 SISTEMA DE INTEGRAÇÃO CLOUDFLARE POKÉLOG (ADICIONADO)
    // =========================================================================
    const LINK_DO_CLOUDFLARE = 'https://pxg-changelog.mateuscouto27.workers.dev/'; 

    function formatarDiscord(texto) {
        if (!texto) return '';
        const safeTexto = escapeHtml(texto);
        // Converte a formatação do Discord para HTML Seguro
        return safeTexto
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
            .replace(/\*(.*?)\*/g, '<em>$1</em>') 
            .replace(/__(.*?)__/g, '<u>$1</u>') 
            .replace(/~~(.*?)~~/g, '<del>$1</del>') 
            .replace(/`(.*?)`/g, '<code class="bg-slate-800 text-blue-300 px-1 rounded">$1</code>') 
            .replace(/\n/g, '<br>');
    }

    async function carregarChangelog() {
        const mural = document.getElementById('mural-changelog');
        if (!mural) return;
        
        try {
            const resposta = await fetch(LINK_DO_CLOUDFLARE);
            if (!resposta.ok) throw new Error('Erro na rede Cloudflare');
            const dados = await resposta.json();

            mural.innerHTML = ''; 
            
            // Aceita tanto um Array direto quanto um objeto que contenha { messages: [] }
            let mensagens = Array.isArray(dados) ? dados : (dados.messages || []);
            
            if (mensagens.length === 0) {
                mural.innerHTML = '<p class="texto-aviso">Nenhuma atualização recente encontrada no servidor.</p>';
                return;
            }

            mensagens.forEach(msg => {
                const texto = typeof msg === 'string' ? msg : (msg.content || msg.texto);
                if (!texto) return;
                
                const div = document.createElement('div');
                div.className = 'mensagem-update';
                div.innerHTML = formatarDiscord(texto);
                mural.appendChild(div);
            });

        } catch (erro) {
            console.error('Erro ao carregar changelog PXG:', erro);
            mural.innerHTML = '<p class="texto-aviso text-red-400">Servidor Cloudflare indisponível no momento. Tente novamente mais tarde.</p>';
        }
    }

    // Inicializa a leitura do Worker logo que a página carrega
    document.addEventListener('DOMContentLoaded', carregarChangelog);


