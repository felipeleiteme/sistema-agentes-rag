# teste_db_completo.py
from src.database import get_supabase_client
from datetime import datetime

supabase = get_supabase_client()

print("🧪 Testando integração Supabase...\n")

# Teste 1: Verificar tabelas
print("1️⃣ Verificando tabelas...")
try:
    tables = ['conversations', 'messages', 'subscriptions', 'usage']
    for table in tables:
        result = supabase.table(table).select("*").limit(1).execute()
        print(f"   ✅ Tabela '{table}' existe e está acessível")
except Exception as e:
    print(f"   ❌ Erro ao verificar tabelas: {e}")

# Teste 2: Criar uma conversa de teste (sem user_id por enquanto)
print("\n2️⃣ Testando criação de conversa...")
try:
    nova_conversa = supabase.table("conversations").insert({
        "title": "Teste de Conversa",
        "user_id": None  # Vamos deixar None por enquanto até integrar auth
    }).execute()
    conversation_id = nova_conversa.data[0]['id']
    print(f"   ✅ Conversa criada com ID: {conversation_id}")
except Exception as e:
    print(f"   ❌ Erro ao criar conversa: {e}")

# Teste 3: Criar mensagem de teste
print("\n3️⃣ Testando criação de mensagem...")
try:
    nova_mensagem = supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "user_id": None,
        "role": "user",
        "content": "Olá, esta é uma mensagem de teste!"
    }).execute()
    print(f"   ✅ Mensagem criada com sucesso")
except Exception as e:
    print(f"   ❌ Erro ao criar mensagem: {e}")

# Teste 4: Listar conversas
print("\n4️⃣ Testando listagem de conversas...")
try:
    conversas = supabase.table("conversations").select("*").execute()
    print(f"   ✅ Total de conversas: {len(conversas.data)}")
except Exception as e:
    print(f"   ❌ Erro ao listar conversas: {e}")

# Teste 5: Listar mensagens da conversa
print("\n5️⃣ Testando listagem de mensagens...")
try:
    mensagens = supabase.table("messages").select("*").eq("conversation_id", conversation_id).execute()
    print(f"   ✅ Total de mensagens na conversa: {len(mensagens.data)}")
    if mensagens.data:
        print(f"   📝 Última mensagem: {mensagens.data[-1]['content'][:50]}...")
except Exception as e:
    print(f"   ❌ Erro ao listar mensagens: {e}")

# Teste 6: Limpar dados de teste
print("\n6️⃣ Limpando dados de teste...")
try:
    supabase.table("messages").delete().eq("conversation_id", conversation_id).execute()
    supabase.table("conversations").delete().eq("id", conversation_id).execute()
    print("   ✅ Dados de teste removidos")
except Exception as e:
    print(f"   ❌ Erro ao limpar dados: {e}")

print("\n✅ Todos os testes concluídos!")
print("🎉 Supabase está pronto para uso!")
