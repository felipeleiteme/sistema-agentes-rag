#!/usr/bin/env python3
"""Sistema de Agentes com RAG usando LangChain + Ollama"""
import sys

from src.agents import AgentService


service = AgentService()


def sistema_multiagente(pergunta: str) -> str:
    """Orquestra a escolha de agentes para responder à pergunta."""

    print(f"\n📋 Pergunta recebida: {pergunta}")
    print("-" * 60)
    agent_key = service.classify_question(pergunta)
    if agent_key == "hr":
        print("✅ Detectado: Pergunta sobre RH → Usando Agente RH com RAG")
    else:
        print("✅ Detectado: Pergunta geral → Usando Agente Assistente")
    sys.stdout.flush()
    resposta = service.answer_question(pergunta)
    if resposta.error:
        print(f"\n⚠️ Erro ao processar: {resposta.error}")
    return resposta.answer


def demonstracao():
    """Executa a demonstração com perguntas pré-definidas"""
    print("\n🎯 DEMONSTRAÇÃO DO SISTEMA\n")

    testes = [
        ("Pergunta sobre RH", "Quantos dias de férias tem um funcionário CLT?"),
        ("Pergunta Geral", "Qual a capital do Brasil?"),
        ("Outra Pergunta sobre RH", "Qual o valor do bônus anual para funcionários PJ?"),
    ]

    for titulo, pergunta in testes:
        print("=" * 60)
        print(f"TESTE: {titulo}")
        print("=" * 60)
        resposta = sistema_multiagente(pergunta)
        print(f"\n📤 RESPOSTA:\n{resposta}")
        print("\n")

    print("=" * 60)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 60)


def interativo():
    """Loop interativo para perguntas livres do usuário"""
    print("🤖 Sistema de Agentes com RAG Iniciado!")
    print("Digite 'sair' para encerrar.\n")

    try:
        while True:
            pergunta = input("💬 Você: ").strip()

            if not pergunta:
                continue

            if pergunta.lower() in {"sair", "exit", "quit"}:
                print("\n👋 Até logo!")
                break

            resposta = sistema_multiagente(pergunta)
            print(f"\n📤 RESPOSTA:\n{resposta}")
            print("-" * 60)
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Encerrando. Até a próxima!")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Sistema multiagente com roteamento inteligente entre agente RH e assistente geral."
    )
    parser.add_argument(
        "-q",
        "--question",
        help="Executa o sistema para uma pergunta única e imprime a resposta.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Executa a demonstração com perguntas pré-definidas.",
    )

    args = parser.parse_args()

    if args.demo:
        demonstracao()
        return

    if args.question:
        pergunta = args.question.strip()
        if not pergunta:
            raise ValueError("A pergunta fornecida está vazia.")

        resposta = sistema_multiagente(pergunta)
        print(f"\n📤 RESPOSTA:\n{resposta}")
        return

    interativo()


if __name__ == "__main__":
    main()
