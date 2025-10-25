# 🔐 Login com Google - Implementação Completa

## ✅ O que foi implementado

### **1. Backend (src/auth_service.py)**
- ✅ `login_google()` - Inicia fluxo OAuth com Google
- ✅ `handle_oauth_callback()` - Processa callback e cria sessão
- ✅ Criação automática de subscription "free" para novos usuários Google

### **2. APIs (src/web/app.py)**
- ✅ `GET /api/auth/google` - Retorna URL de autenticação do Google
- ✅ `GET /auth/callback` - Recebe callback do Google e autentica usuário

### **3. Frontend**
- ✅ Botão "Continuar com Google" em `/login`
- ✅ Botão "Continuar com Google" em `/register`
- ✅ Design moderno com logo do Google
- ✅ Separador "OU" entre formulário e Google

---

## 🚀 Como Testar

### **1. Configurar URL de Callback no Google Cloud**

Como você já configurou o Google OAuth, verifique se adicionou a URL de callback correta:

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione seu projeto "SeuAgente"
3. Vá em **APIs & Services** → **Credentials**
4. Clique no seu OAuth 2.0 Client ID
5. Em **Authorized redirect URIs**, certifique-se de ter:
   ```
   http://localhost:8001/auth/callback
   ```
   (para desenvolvimento local)

6. Para produção, adicione também:
   ```
   https://[seu-projeto].supabase.co/auth/v1/callback
   ```

### **2. Verificar Configuração no Supabase**

1. Acesse [Supabase Dashboard](https://supabase.com/dashboard)
2. Selecione seu projeto
3. Vá em **Authentication** → **Providers** → **Google**
4. Verifique se:
   - ✅ Google está **Enabled** (habilitado)
   - ✅ **Client ID** e **Client Secret** estão corretos
   - ✅ **Redirect URL** está configurada

### **3. Iniciar o Servidor**

```bash
# Certifique-se de estar no diretório do projeto
cd /Users/Felipe/Documents/Projetos/Agentes/meu_sistema_agentes

# Instalar dependências (se necessário)
pip3 install -r requirements.txt

# Iniciar servidor
python3 -m uvicorn src.web.app:app --reload --port 8001
```

### **4. Testar o Fluxo**

1. **Acesse:** http://localhost:8001/login

2. **Clique em:** "Continuar com Google"

3. **Fluxo esperado:**
   - Você será redirecionado para página de login do Google
   - Escolha sua conta Google
   - Aceite as permissões solicitadas
   - Será redirecionado de volta para `/auth/callback`
   - Tokens serão salvos automaticamente no localStorage
   - Redirecionado para a home (`/`)
   - Usuário logado com sucesso! 🎉

---

## 🔍 Verificar se Funcionou

### **No Navegador:**

1. Abra **DevTools** (F12)
2. Vá na aba **Application** → **Local Storage**
3. Verifique se existem as chaves:
   - `access_token`
   - `refresh_token`
   - `user_email`
   - `user_id`

### **No Supabase:**

1. Vá em **Authentication** → **Users**
2. Verifique se seu usuário Google foi criado
3. Vá em **Table Editor** → **subscriptions**
4. Verifique se foi criado um registro com:
   - `user_id` = ID do usuário
   - `status` = "free"
   - `plan_name` = "free"

---

## 📝 Fluxo Técnico

```
1. Usuário clica em "Continuar com Google"
   ↓
2. Frontend faz GET /api/auth/google
   ↓
3. Backend chama Supabase Auth para gerar URL OAuth
   ↓
4. Usuário é redirecionado para Google
   ↓
5. Google autentica e redireciona para /auth/callback?code=XXX
   ↓
6. Backend troca o código por sessão (access_token + refresh_token)
   ↓
7. Verifica se subscription existe, se não cria uma
   ↓
8. Retorna HTML que salva tokens no localStorage
   ↓
9. Redireciona para home (/) com usuário logado
```

---

## ⚠️ Troubleshooting

### **Erro: "redirect_uri_mismatch"**
- **Causa:** URL de callback não está cadastrada no Google Cloud
- **Solução:** Adicione `http://localhost:8001/auth/callback` nas Authorized redirect URIs

### **Erro: "Invalid provider"**
- **Causa:** Google OAuth não está habilitado no Supabase
- **Solução:** Vá em Authentication → Providers → Google e habilite

### **Erro: "Missing credentials"**
- **Causa:** Client ID ou Secret não estão configurados no Supabase
- **Solução:** Adicione as credenciais do Google Cloud no Supabase

### **Tokens não são salvos**
- **Causa:** Erro no callback ou JavaScript bloqueado
- **Solução:**
  1. Verifique console do navegador (F12)
  2. Veja se há erros de CORS ou JavaScript
  3. Tente limpar cache e cookies

### **Usuário não é criado no banco**
- **Causa:** Erro ao inserir subscription
- **Solução:**
  1. Verifique se tabela `subscriptions` existe
  2. Execute o SQL das tabelas novamente se necessário
  3. Veja logs do servidor para erros

---

## 🎨 Customizações Possíveis

### **Alterar texto do botão:**
Em `login.html` e `register.html`, mude:
```html
<button class="google-button" id="google-login-button">
  ...
  Entrar com Google  <!-- Altere aqui -->
</button>
```

### **Adicionar outros provedores (GitHub, Facebook):**
1. Configure o provider no Supabase
2. Adicione botão no HTML
3. Use o mesmo fluxo com `provider: "github"` ou `provider: "facebook"`

---

## 📊 Dados do Usuário Google

Quando um usuário faz login com Google, o Supabase retorna:

```javascript
{
  user_id: "uuid-do-usuario",
  email: "usuario@gmail.com",
  full_name: "Nome do Usuário",  // Do perfil Google
  avatar_url: "https://...",     // Foto de perfil
  provider: "google"
}
```

Você pode acessar esses dados via `/api/auth/me` após login.

---

## ✅ Checklist Final

- [ ] Google OAuth configurado no Google Cloud Console
- [ ] Redirect URI cadastrada: `http://localhost:8001/auth/callback`
- [ ] Google habilitado no Supabase (Authentication → Providers)
- [ ] Client ID e Secret configurados no Supabase
- [ ] Servidor rodando em `http://localhost:8001`
- [ ] Botão "Continuar com Google" visível em /login e /register
- [ ] Tabelas `subscriptions` e demais criadas no Supabase

---

## 🎉 Pronto!

Agora seu sistema tem:
- ✅ Login com email/senha
- ✅ Login com Google OAuth
- ✅ Registro de usuários
- ✅ Criação automática de subscription free
- ✅ Salvamento de tokens
- ✅ Redirecionamento automático

**Próximo passo:** Teste o fluxo completo e comece a usar! 🚀
