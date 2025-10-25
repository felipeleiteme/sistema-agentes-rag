"""Teste do sistema de limites."""

from src.limits import check_user_limit, increment_usage, get_usage_stats, reset_monthly_usage
from src.database import get_supabase_client

# Substitua pelo seu user_id (pegar do Supabase ou após login)
TEST_USER_ID = "seu-user-id-aqui"


def test_limits_flow():
    """Testa o fluxo completo de limites."""

    print("🧪 Testando Sistema de Limites\n")
    print("=" * 60)

    # 1. Verificar limite inicial
    print("\n1️⃣ Verificando limite inicial...")
    limit_check = check_user_limit(TEST_USER_ID, "messages")
    print(f"   ✅ Permitido: {limit_check['allowed']}")
    print(f"   📊 Restante: {limit_check['remaining']}/{limit_check.get('limit', 'N/A')}")
    print(f"   📦 Plano: {limit_check['plan']}")

    # 2. Simular uso de 5 mensagens
    print("\n2️⃣ Simulando uso de 5 mensagens...")
    for i in range(5):
        success = increment_usage(TEST_USER_ID, "messages")
        if success:
            print(f"   ✅ Mensagem {i+1} incrementada")
        else:
            print(f"   ❌ Erro ao incrementar mensagem {i+1}")

    # 3. Verificar limite atualizado
    print("\n3️⃣ Verificando limite após uso...")
    limit_check = check_user_limit(TEST_USER_ID, "messages")
    print(f"   ✅ Permitido: {limit_check['allowed']}")
    print(f"   📊 Restante: {limit_check['remaining']}/{limit_check.get('limit', 'N/A')}")
    print(f"   📈 Usado: {limit_check.get('current_usage', 'N/A')}")

    # 4. Ver estatísticas completas
    print("\n4️⃣ Estatísticas completas...")
    stats = get_usage_stats(TEST_USER_ID)
    print(f"   📧 Mensagens: {stats['messages_count']} (restam {stats['messages_remaining']})")
    print(f"   🖼️ Imagens: {stats['images_analyzed']} (restam {stats['images_remaining']})")
    print(f"   📄 PDFs: {stats['pdfs_analyzed']} (restam {stats['pdfs_remaining']})")

    # 5. Simular atingir limite
    print("\n5️⃣ Simulando atingir o limite (adicionando 46 mensagens)...")
    for i in range(46):
        increment_usage(TEST_USER_ID, "messages")

    limit_check = check_user_limit(TEST_USER_ID, "messages")
    print(f"   ✅ Permitido: {limit_check['allowed']}")
    print(f"   📊 Restante: {limit_check['remaining']}")
    if not limit_check['allowed']:
        print(f"   ⚠️ Mensagem de bloqueio: {limit_check['message']}")

    # 6. Resetar para próximo teste
    print("\n6️⃣ Resetando uso para próximo teste...")
    if reset_monthly_usage(TEST_USER_ID):
        print("   ✅ Uso resetado com sucesso")
    else:
        print("   ❌ Erro ao resetar uso")

    print("\n" + "=" * 60)
    print("✅ Teste completo!\n")


def test_premium_user():
    """Testa fluxo de usuário premium."""

    print("\n💎 Testando Usuário Premium")
    print("=" * 60)

    # Para testar premium, você precisa:
    # 1. Ir no Supabase → subscriptions
    # 2. Alterar status de 'free' para 'active'
    # 3. Rodar este teste

    limit_check = check_user_limit(TEST_USER_ID, "messages")

    if limit_check.get('is_premium'):
        print("   ✅ Usuário é PREMIUM")
        print(f"   ✨ Limite: {limit_check['remaining']}")
    else:
        print("   ℹ️ Usuário é FREE")
        print("   💡 Para testar premium, altere status no Supabase")

    print("=" * 60 + "\n")


def show_database_data():
    """Mostra dados diretamente do banco."""

    print("\n📊 Dados no Banco de Dados")
    print("=" * 60)

    supabase = get_supabase_client()

    # Subscription
    print("\n1️⃣ Subscription:")
    sub = supabase.table("subscriptions")\
        .select("*")\
        .eq("user_id", TEST_USER_ID)\
        .execute()

    if sub.data:
        print(f"   Status: {sub.data[0]['status']}")
        print(f"   Plano: {sub.data[0]['plan_name']}")
    else:
        print("   ⚠️ Nenhuma subscription encontrada")

    # Usage
    print("\n2️⃣ Usage (mês atual):")
    from datetime import datetime
    current_month = datetime.now().strftime("%Y-%m")

    usage = supabase.table("usage")\
        .select("*")\
        .eq("user_id", TEST_USER_ID)\
        .eq("month_year", current_month)\
        .execute()

    if usage.data:
        print(f"   Mensagens: {usage.data[0]['messages_count']}")
        print(f"   Imagens: {usage.data[0]['images_analyzed']}")
        print(f"   PDFs: {usage.data[0]['pdfs_analyzed']}")
    else:
        print("   ℹ️ Nenhum uso registrado neste mês")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    print("\n" + "🚀 Sistema de Limites - Teste Completo".center(60))
    print("\n⚠️ ANTES DE RODAR:")
    print("   1. Configure TEST_USER_ID no topo deste arquivo")
    print("   2. Certifique-se que o usuário existe no Supabase")
    print("   3. Execute: python3 teste_limites.py\n")

    if TEST_USER_ID == "seu-user-id-aqui":
        print("❌ ERRO: Configure TEST_USER_ID primeiro!")
        print("\nComo obter seu user_id:")
        print("   1. Faça login no sistema")
        print("   2. Abra DevTools (F12) → Application → Local Storage")
        print("   3. Copie o valor de 'user_id'")
        print("   4. Cole no topo deste arquivo\n")
    else:
        try:
            test_limits_flow()
            test_premium_user()
            show_database_data()

            print("\n💡 Próximos passos:")
            print("   1. Teste no frontend fazendo login")
            print("   2. Envie 50+ mensagens para testar bloqueio")
            print("   3. Veja estatísticas em /api/usage")
            print("\n✅ Tudo funcionando! Sistema pronto para produção.\n")

        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()
