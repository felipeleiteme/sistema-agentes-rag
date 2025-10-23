#!/usr/bin/env python3
"""Chat interativo com agente RH"""
from langchain_ollama import ChatOllama
from tools import buscar_conhecimento_rh


def main():
    """Executa o chat interativo"""
    llm = ChatOllama(model="llama3.2:3b", temperature=0.7)

    print("🤖 Chat com Agente RH - Base de Conhecimento")
    print("Digite 'sair' para encerrar\n")
    print("=" * 60)

    while True:
        pergunta = input("\n💬 Você: ").strip()

        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("\n👋 Até logo!")
            break

        if not pergunta:
            continue

        print("\n🔍 Buscando informações...")
        contexto = buscar_conhecimento_rh._run(pergunta)

        prompt = f"""Você é um especialista em RH.

CONTEXTO: {contexto}

PERGUNTA: {pergunta}

Responda de forma clara e profissional em português:"""

        print("⏳ Pensando... (10-15 segundos)")
        resposta = llm.invoke(prompt)

        print(f"\n🤖 Agente RH: {resposta.content}")
        print("-" * 60)


if __name__ == "__main__":
    main()
