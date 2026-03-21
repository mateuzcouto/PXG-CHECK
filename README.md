# PXG Check - Guia de Deployment no Firebase

## 📋 Pré-requisitos

- Node.js 16+ instalado
- Conta Firebase (criar em [firebase.google.com](https://firebase.google.com))
- Firebase CLI instalado (`npm install -g firebase-tools`)

## 🚀 Setup Inicial

### 1. Clonar/Preparar o Projeto
```bash
cd pxg-check
npm install
```

### 2. Configurar Firebase
```bash
firebase login
firebase init hosting
```

Selecione seu projeto Firebase:
```bash
? What do you want to use as your public directory? → src
? Configure as a single-page app (rewrite all urls to /index.html)? → Yes
? Set up automatic builds and deploys with GitHub? → No (por enquanto)
```

### 3. Criar arquivo .env local
```bash
cp .env.example .env
```

**✏️ Edite `.env` com suas credenciais Firebase:**
```
VITE_FIREBASE_API_KEY=AIzaSyD_Z3Z-xxxxxxxxxxxxxxxxxxxxxxxx
VITE_FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=seu-projeto
VITE_FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=000000000000
VITE_FIREBASE_APP_ID=1:000000000000:web:xxxxxxxxxxxxxxxxxxxxx
```

## 🧪 Testar Localmente

```bash
npm run dev
# Abre em http://localhost:5173
```

## 🔒 Configurar Regras de Segurança no Firebase

### 1. Firestore Rules (Crítico!)
No Firebase Console → Firestore → Rules:

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Public read-only
    match /artifacts/{docId=**} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
    
    // User data - apenas o proprietário pode acessar
    match /artifacts/users/{userId}/{document=**} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Feedback - público pode enviar
    match /artifacts/public/data/feedbacks/{feedbackId} {
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

### 2. Authentication Rules
Firebase Console → Authentication → Settings:
- ✅ Habilitar "Anonymous signing"
- ✅ Habilitar qualquer outro método de autenticação desejado

### 3. API Keys Restrictions (IMPORTANTE!)
Firebase Console → Project Settings → API Keys:
1. Clique na chave da Web
2. Em "Application restrictions": Selecione "HTTP referrers"
3. Adicione seu domínio: `seu-site.firebaseapp.com`
4. Em "API restrictions": Selecione apenas APIs necessárias
   - Cloud Firestore API ✅
   - Authentication ✅

## 📦 Build para Produção

```bash
npm run build
# Gera arquivos otimizados em dist/
```

## ☁️ Deploy no Firebase Hosting

```bash
# Fazer deploy
firebase deploy

# Ou apenas hosting (se tiver outros serviços)
firebase deploy --only hosting
```

## ✅ Checklist de Segurança Antes de Publicar

- [ ] `.env` **NUNCA** foi commitado no Git
- [ ] `firestore.rules` está configurado e publicado
- [ ] API Key está com restrições de domínio
- [ ] Authentication anônima habilitada (se necessário)
- [ ] Dados sensíveis não estão no cliente (senhas, tokens internos)
- [ ] HTTPS está habilitado (automático no Firebase Hosting)
- [ ] CSP (Content Security Policy) headers configurados
- [ ] Cache headers configurados corretamente

## 🐛 Debug e Troubleshooting

### Erro: "Permission denied"
→ Verificar Firestore Rules e se está autenticado

### Erro: "API key not valid"
→ Verificar credenciais em `.env`

### Site não carrega após deploy
→ Verificar `firebase.json` e se `src/` está correto

## 📚 Recursos Úteis

- [Firebase Console](https://console.firebase.google.com)
- [Firebase Hosting Docs](https://firebase.google.com/docs/hosting)
- [Firestore Rules Reference](https://firebase.google.com/docs/firestore/security/get-started)

---

**Última atualização:** Março 2026
