#!/usr/bin/env python3
"""
SAC Learning GEMS - Sistema de Aprendizado Modular
Sistema com 7 agentes especializados (GEMs) que guiam o usuário sequencialmente.
"""

import sys
from src.agents import GEMService


def main():
    """Ponto de entrada principal do sistema SAC Learning GEMS."""

    # Inicializa o serviço
    service = GEMService()

    # Mostra boas-vindas
    print(service.get_welcome_message())

    # Loop interativo
    try:
        while True:
            # Lê input do usuário
            user_input = input("\n💬 Você: ").strip()

            # Verifica se quer sair
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\n👋 Até logo! Seu progresso foi salvo em user_journey.json")
                break

            # Ignora inputs vazios
            if not user_input:
                continue

            # Processa mensagem
            response = service.process_message(user_input)

            # Mostra resposta
            if response.error:
                print(f"\n⚠️ Erro: {response.error}")
            else:
                # Cabeçalho da resposta
                if response.is_orchestrator:
                    print(f"\n🎯 Sistema:")
                else:
                    print(f"\n{response.gem_id} {response.gem_name}:")

                # Resposta
                print(f"\n{response.answer}")
                print("\n" + "-" * 70)

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Encerrando. Seu progresso foi salvo!")


if __name__ == "__main__":
    main()
