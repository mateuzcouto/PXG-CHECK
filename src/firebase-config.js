// ⚠️ IMPORTANTE: Este arquivo contém credenciais da API do Firebase
// Essas credenciais SÃO públicas (client-side) e podem ser expostas no código
// Mas DEVEM ser restringidas no Firebase Console com regras de segurança

// Carrega as configurações do Firebase das variáveis de ambiente
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyD_Z3Z-...", // Substituir com sua chave
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "seu-projeto.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "seu-projeto",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "seu-projeto.appspot.com",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "000000000000",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:000000000000:web:..."
};

// Inicializa Firebase
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.0/firebase-app.js';
import { getAuth, signInAnonymously, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/10.7.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore.js';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Auto-autenticação anônima
onAuthStateChanged(auth, (user) => {
  if (!user) {
    signInAnonymously(auth).catch(err => console.error("Erro ao autenticar anonimamente:", err));
  }
});

export { auth, db };
