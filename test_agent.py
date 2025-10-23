#!/usr/bin/env python3
"""Teste rápido do sistema de agentes com RAG"""
from langchain_ollama import ChatOllama
from tools import buscar_conhecimento_rh


def main():
    """Executa testes do sistema"""
    print("🤖 Teste do Sistema de Agentes com RAG\n")

    # Teste 1: Ferramenta RAG
    print("=" * 60)
    print("TESTE 1: Ferramenta RAG")
    print("=" * 60)

    pergunta = "Quantos dias de férias CLT?"
    print(f"\nPergunta: {pergunta}")
    print("\nBuscando na base de conhecimento...")

    contexto = buscar_conhecimento_rh._run(pergunta)
    print(f"\n✅ Contexto encontrado ({len(contexto)} caracteres):")
    print(contexto[:300] + "..." if len(contexto) > 300 else contexto)

    # Teste 2: LLM Ollama
    print("\n\n" + "=" * 60)
    print("TESTE 2: LLM Ollama")
    print("=" * 60)

    llm = ChatOllama(model="llama3.2:3b", temperature=0.7)

    print("\nPerguntando ao LLM...")
    prompt = f"""Você é um especialista em RH.

CONTEXTO: {contexto}

PERGUNTA: {pergunta}

Responda de forma curta e direta em português:"""

    print("\n⏳ Aguardando resposta do Llama...")
    resposta = llm.invoke(prompt)

    print(f"\n✅ RESPOSTA DO LLM:")
    print(resposta.content)

    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)


if __name__ == "__main__":
    main()
