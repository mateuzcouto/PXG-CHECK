# 🔒 Relatório de Segurança - PXG Check

**Data:** Março 19, 2026  
**Status:** ⚠️ **NECESSITA AJUSTES ANTES DE PUBLICAR**

---

## 📊 Resumo Executivo

| Severidade | Problema | Status |
|-----------|----------|--------|
| 🔴 CRÍTICO | API Key exposta no código | ⚠️ Requer ação |
| 🟠 ALTO | Firestore Rules não configuradas | ⚠️ Requer ação |
| 🟠 ALTO | execCommand() para copy (deprecated) | ⚠️ Requer ação |
| 🟡 MÉDIO | Google Analytics ID exposto | ⚠️ Requer ação |
| 🟡 MÉDIO | Sem rate limiting no Firestore | ⚠️ Requer ação |

---

## 🔴 CRÍTICO - MÃO NA MASSA AGORA!

### 1. **API Key Exposta no Código-Fonte**
**Localização:** `app.js` (Google Analytics ID e credits)

```javascript
// ❌ INSEGURO - NUNCA faça isso!
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S2T9XFXR8Z"></script>
```

**Risco:** Qualquer pessoa pode copiar sua chave API e:
- Spamear seu Firestore (custos $$)
- Deletar dados
- Ver dados públicos

**✅ Solução:**
1. Remova `G-S2T9XFXR8Z` do código
2. Use variável de ambiente: `VITE_GA_ID`
3. Carregue dinamicamente:
```javascript
const gaId = import.meta.env.VITE_GA_ID;
if(gaId) {
  const script = document.createElement('script');
  script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
  script.async = true;
  document.head.appendChild(script);
}
```

---

### 2. **Firestore Rules - OBRIGATÓRIO Configurar**

**Situação Atual:** Sem regras = qualquer pessoa pode:
- Ler todos os dados
- Escrever/deletar qualquer coisa
- Custo ilimitado

**✅ Solução - Configure em Firebase Console > Firestore > Rules:**

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users - apenas o proprietário acessa seus dados
    match /artifacts/{db}/users/{userId}/{document=**} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Public data (read-only para todos)
    match /artifacts/{db}/public/data/{document=**} {
      allow read: if true;
      allow create, update, delete: if request.auth != null && request.auth.uid == get(/databases/$(database)/documents/artifacts/$(db)/public/data/$(document)).data.uid;
    }
    
    // Feedback - apenas quem criou pode deletar
    match /artifacts/{db}/public/data/feedbacks/{feedbackId} {
      allow create: if request.auth != null;
      allow read: if request.auth.uid == resource.data.uid;
      allow delete: if request.auth.uid == resource.data.uid;
    }
    
    // Deny everything else
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

**⏱️ Tempo:** 2 minutos  
**Criticidade:** 🔴 MÁXIMA - sem isso, qualquer pessoa pode destruir seu banco de dados!

---

## 🟠 ALTO - Importante Corrigir

### 3. **document.execCommand('copy') - Deprecated**

**Localização:** `app.js` (funções `copyCoords()` e `copyPix()`)

```javascript
// ❌ DEPRECATED - Não funciona em browsers modernos
document.execCommand('copy');
```

**Problema:** Não funciona em navegadores atuais (Chrome, Firefox)

**✅ Solução - Use Clipboard API:**
```javascript
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Erro ao copiar:', err);
    return false;
  }
}

// Uso:
document.getElementById('copy-btn').onclick = async () => {
  const success = await copyToClipboard('seu-texto');
  if(success) alert('Copiado!');
};
```

---

### 4. **Sem Proteção Contra CSRF/XSS**

**Risco:** Injeção de código malicioso via dados do Firestore

**✅ Solução:**
```javascript
// ❌ NUNCA faça:
el.innerHTML = fetchedData;

// ✅ SEMPRE faça:
el.textContent = fetchedData;
// Ou use DOMPurify para HTML dinâmico:
el.innerHTML = DOMPurify.sanitize(fetchedData);
```

**Ação:** Instale DOMPurify:
```bash
npm install dompurify
npm install -D @types/dompurify
```

---

## 🟡 MÉDIO - Melhorias Recomendadas

### 5. **Rate Limiting no Firestore**
**Problema:** Usuários podem enviar unlimited requests

**✅ Solução:** Configure Cloud Functions:
```javascript
// Cloud Function - enviar para functions/
exports.submitFeedback = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError('unauthenticated');
  
  // Rate limit (1 feedback por minuto)
  const userFeedbacks = await admin.firestore()
    .collection('artifacts/artifacts/public/data/feedbacks')
    .where('uid', '==', context.auth.uid)
    .where('date', '>=', new Date(Date.now() - 60000))
    .get();
    
  if (userFeedbacks.size > 0) {
    throw new functions.https.HttpsError('resource-exhausted', 'Aguarde antes de enviar outro feedback');
  }
  
  await admin.firestore()
    .collection('artifacts/artifacts/public/data/feedbacks')
    .add({...data, uid: context.auth.uid, date: new Date()});
});
```

---

### 6. **Validação de Dados do Cliente**
```javascript
// ❌ Aceita qualquer coisa
const val = parseInt(document.getElementById('fin-value').value);

// ✅ Valida tudo
function validateFinanceValue(val) {
  if (!val) throw new Error('Valor inválido');
  const num = parseInt(val);
  if (isNaN(num) || num < 0 || num > 1000000) {
    throw new Error('Valor deve estar entre 0 e 1.000.000');
  }
  return num;
}
```

---

### 7. **Sem HTTPS Headers**
**Problema:** Falta de Content Security Policy

**✅ Solução - Adicione em `firebase.json`:**
```json
{
  "hosting": {
    "headers": [
      {
        "source": "**",
        "headers": [
          {
            "key": "Content-Security-Policy",
            "value": "default-src 'self'; script-src 'self' https://cdn.tailwindcss.com https://www.googletagmanager.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data: https:; frame-ancestors 'none'"
          },
          {
            "key": "X-Content-Type-Options",
            "value": "nosniff"
          },
          {
            "key": "X-Frame-Options",
            "value": "DENY"
          },
          {
            "key": "Referrer-Policy",
            "value": "strict-origin-when-cross-origin"
          }
        ]
      }
    ]
  }
}
```

---

## ✅ Checklist Final de Deployment

Antes de publicar online:

- [ ] Remover `G-S2T9XFXR8Z` do código (usar env vars)
- [ ] Configurar Firestore Rules (Firebase Console)
- [ ] Criar arquivo `.env` com credenciais reais
- [ ] Garantir `.env` está no `.gitignore`
- [ ] Testar offline em `npm run dev`
- [ ] Passar Firestore Rules para produção
- [ ] Restringir API Key por domínio (Firebase Console > Settings)
- [ ] Configurar Cloud Functions para rate limiting
- [ ] Testar em incógnito (sem cache)
- [ ] Testar em mobile
- [ ] Backup do banco de dados

---

## 📚 Recursos Importante

1. **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** - Vulnerabilidades web
2. **[Firebase Security Rules](https://firebase.google.com/docs/firestore/security/get-started)**
3. **[CSP Configurator](https://www.csplinter.com/)**
4. **[DOMPurify Docs](https://github.com/cure53/DOMPurify)**

---

## 🚨 Próximos Passos

1. ✅ Aplique as correções críticas
2. ✅ Teste localmente (`npm run dev`)
3. ✅ Faça deploy: `firebase deploy --only hosting`
4. ✅ Monitore no Firebase Console
5. ✅ Configure alertas para custos altos

**Sem seguir este guia, seu site pode sofrer ataques ou ter custos inesperados!**

---

*Relatório gerado automaticamente. Revise e aplique conforme necessário.*
