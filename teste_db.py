# teste_db.py
from src.database import get_supabase_client

supabase = get_supabase_client()

# Teste simples
try:
    result = supabase.table("conversations").select("id").limit(1).execute()
    print("✅ Conexão com Supabase OK!")
except Exception as e:
    print(f"❌ Erro: {e}")
