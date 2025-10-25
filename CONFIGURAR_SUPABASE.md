# ⚙️ Configurar Supabase - Desabilitar Confirmação de Email

Para permitir que usuários façam login imediatamente após o registro (sem precisar confirmar email), siga os passos:

## 📝 Passos no Painel do Supabase

1. **Acesse seu projeto** em https://supabase.com/dashboard

2. **Vá em:** `Authentication` → `Settings` (no menu lateral esquerdo)

3. **Procure a seção:** "Email Auth"

4. **Desabilite a opção:**
   - ❌ **"Enable email confirmations"**

   OU

   - ❌ **"Confirm email"**

5. **Clique em "Save"** no final da página

---

## ✅ Resultado

Após essa configuração:
- ✅ Usuários podem fazer login imediatamente após criar conta
- ✅ Não precisam verificar email
- ✅ Registro e login funcionam instantaneamente

---

## 🔧 Configuração Adicional (Opcional)

### **Auto-confirm de novos usuários:**

Se a opção acima não estiver disponível, faça isso via SQL:

1. Vá em `SQL Editor` no Supabase
2. Execute este comando:

```sql
-- Auto-confirmar todos os novos usuários
ALTER TABLE auth.users
ALTER COLUMN email_confirmed_at
SET DEFAULT NOW();
```

Ou via código na função de registro (já implementado no `auth_service.py`).

---

## 🚀 Tudo Pronto!

Agora os usuários podem:
1. Criar conta em `/register`
2. Fazer login imediatamente em `/login`
3. Usar o sistema sem precisar confirmar email
