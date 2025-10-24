"""
Orquestrador Principal do Sistema SAC Learning GEMS.
Gerencia o fluxo sequencial entre os 7 GEMs, mantendo estado e guiando o usuário.
"""

from typing import Dict, Optional, List
from datetime import datetime
import json
import os
import shutil

from .gems import (
    GEMS_INSTRUCTIONS,
    GEMS_SEQUENCE,
    get_gem_info,
    get_next_gem,
    get_all_gems
)


class GEMOrchestrator:
    """
    Orquestrador que gerencia a jornada do usuário pelos 7 GEMs.

    Responsabilidades:
    - Apresentar o sistema ao usuário
    - Guiar sequencialmente pelos GEMs
    - Manter contexto mínimo necessário (apenas IDs e outputs estruturados)
    - Sugerir próximo passo baseado no progresso
    """

    def __init__(self, state_file: str = "user_journey.json"):
        """
        Inicializa o orquestrador.

        Args:
            state_file: Arquivo para persistir estado da jornada do usuário
        """
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Carrega estado da jornada do usuário."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "current_gem": None,
            "completed_gems": [],
            "gem_outputs": {},
            "gem_conversations": {},  # Histórico completo de cada GEM
            "shared_context": "",  # Contexto compartilhado entre GEMs
            "started_at": None,
            "last_updated": None
        }

    def _save_state(self):
        """Persiste estado da jornada."""
        self.state["last_updated"] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def get_welcome_message(self) -> str:
        """Retorna mensagem de boas-vindas ao sistema."""
        return """
╔══════════════════════════════════════════════════════════════════════╗
║                 🌟 SAC LEARNING GEMS 🌟                              ║
║            Sistema de Aprendizado Modular                             ║
╚══════════════════════════════════════════════════════════════════════╝

Bem-vindo ao Sistema de Amplificação Cognitiva!

Este é um conjunto de 7 Gems (agentes) especializados que revolucionam
a curva de aprendizado através de **aprendizado interativo** — prática
guiada por agentes que trabalham em conjunto.

💎 **Como funciona:**
- Cada GEM é um especialista que se comunica com os outros
- Você será guiado sequencialmente por 7 etapas
- Os GEMs compartilham contexto para personalizar sua jornada
- No final, você terá um sistema personalizado operacional

🗺️ **Os 7 GEMs:**

1. 🗺️  Mestre do Mapeamento - Portal de entrada (45 min)
2. 🔍 Diagnosticador F.O.C.O. - Clarificador de problemas (20-40 min)
3. ⚖️  Validador Estratégico - Consultor de energia (30 min)
4. 🔬 Laboratório Científico - Painel multi-IA (30-45 min)
5. 🎓 Tutor Socrático - Certificação de domínio (60 min)
6. 🏗️  Arquiteto de Implementação - Planejador macro (40 min)
7. 💎 Construtor de Sistemas - Arquiteto de KBFs (30 min)

📊 **Tempo total estimado:** 4-6 horas (distribuídas em vários dias)

🎯 **Resultado final:** Um KBF (assistente IA personalizado) que te conhece
   e adapta cada sugestão à sua realidade única.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite 'iniciar' para começar pelo GEM 1: Mestre do Mapeamento
Digite 'status' para ver seu progresso atual
Digite 'listar' para ver todos os GEMs disponíveis
"""

    def get_current_status(self) -> str:
        """Retorna status atual da jornada do usuário."""
        if not self.state["started_at"]:
            return "❌ Você ainda não iniciou sua jornada pelos GEMs.\nDigite 'iniciar' para começar!"

        completed = len(self.state["completed_gems"])
        total = len(GEMS_SEQUENCE)
        progress = (completed / total) * 100

        status = f"""
📊 **SEU PROGRESSO:**

⏰ Iniciado em: {self.state["started_at"]}
📈 Progresso: {completed}/{total} GEMs completos ({progress:.0f}%)

✅ **GEMs Completados:**
"""

        for gem_id in self.state["completed_gems"]:
            gem_info = get_gem_info(gem_id)
            status += f"   {gem_info['emoji']} {gem_info['name']}\n"

        if self.state["current_gem"]:
            current_info = get_gem_info(self.state["current_gem"])
            status += f"\n🔄 **GEM Atual:**\n   {current_info['emoji']} {current_info['name']}\n"

        remaining = total - completed
        if remaining > 0:
            status += f"\n📋 **Restam {remaining} GEMs**\n"
        else:
            status += "\n🎉 **Parabéns! Você completou todos os GEMs!**\n"

        return status

    def list_gems(self) -> str:
        """Lista todos os GEMs disponíveis."""
        gems = get_all_gems()
        output = "\n📚 **TODOS OS 7 GEMs:**\n\n"

        for i, gem in enumerate(gems, 1):
            status_emoji = "✅" if gem["id"] in self.state["completed_gems"] else "⭕"
            output += f"{status_emoji} **{i}. {gem['emoji']} {gem['name']}**\n"
            output += f"   {gem['role']}\n"
            output += f"   📋 {gem['specialty']}\n\n"

        return output

    def start_journey(self) -> tuple[str, str]:
        """
        Inicia a jornada do usuário.

        Returns:
            Tuple com (mensagem de início, ID do primeiro GEM)
        """
        if not self.state["started_at"]:
            self.state["started_at"] = datetime.now().isoformat()

        self.state["current_gem"] = GEMS_SEQUENCE[0]
        self._save_state()

        gem_info = get_gem_info(GEMS_SEQUENCE[0])

        message = f"""
🚀 **JORNADA INICIADA!**

Bem-vindo ao primeiro GEM da sua jornada de transformação:

{gem_info['emoji']} **{gem_info['name']}**
📋 {gem_info['role']}
⏰ Duração estimada: {gem_info['duration']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 **Como começar sua conversa:**

O agente vai se apresentar de forma acolhedora e guiar você com perguntas claras durante todo o processo.

✅ **Para iniciar, você pode simplesmente dizer:**
   • "Olá" ou "Oi"
   • "Estou pronto para começar"
   • Ou começar direto contando sobre sua situação atual

🎯 **Relaxe!** O agente vai te guiar passo a passo com empatia e clareza.
Não existe resposta errada - apenas honestidade e abertura.

📝 **Dica:** Cada GEM trabalha de forma independente, então não se preocupe
    com o que foi dito antes. Foque apenas na conversa atual.

Digite sua mensagem abaixo para começar! 👇
"""

        return message, GEMS_SEQUENCE[0]

    def get_current_gem(self) -> Optional[str]:
        """Retorna o ID do GEM atual."""
        return self.state.get("current_gem")

    def activate_gem(self, gem_id: str) -> str:
        """Ativa um GEM específico."""
        self.state["current_gem"] = gem_id
        self._save_state()
        gem_info = get_gem_info(gem_id)
        return f"Ativado: {gem_info['name']} ({gem_info['emoji']})"

    def complete_gem(self, gem_id: str, output: str) -> tuple[str, Optional[str]]:
        """
        Marca um GEM como completo e sugere o próximo.

        Args:
            gem_id: ID do GEM que foi completado
            output: Output estruturado do GEM (ex: MAPA-2025-10-001)

        Returns:
            Tuple com (mensagem de conclusão, ID do próximo GEM ou None)
        """
        if gem_id not in self.state["completed_gems"]:
            self.state["completed_gems"].append(gem_id)

        self.state["gem_outputs"][gem_id] = {
            "completed_at": datetime.now().isoformat(),
            "output": output
        }

        next_gem_id = get_next_gem(gem_id)

        if next_gem_id:
            self.state["current_gem"] = next_gem_id
            self._save_state()

            completed_info = get_gem_info(gem_id)
            next_info = get_gem_info(next_gem_id)

            message = f"""
╔══════════════════════════════════════════════════════════════╗
║              ✅ GEM COMPLETADO!                               ║
╚══════════════════════════════════════════════════════════════╝

Parabéns! Você completou:
{completed_info['emoji']} **{completed_info['name']}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **PRÓXIMO PASSO:**

{next_info['emoji']} **{next_info['name']}**
📋 {next_info['role']}
⏰ Duração estimada: {next_info['duration']}

💡 **O que você precisa:**
- {completed_info['name']} está completo
- Tenha em mãos o output que você recebeu
- Separe {next_info['duration']} de foco

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite 'continuar' quando estiver pronto para o próximo GEM!
Ou digite 'status' para ver seu progresso completo.
"""
            return message, next_gem_id

        else:
            # Último GEM completado
            self.state["current_gem"] = None
            self._save_state()

            message = f"""
╔══════════════════════════════════════════════════════════════╗
║          🎉 PARABÉNS! JORNADA COMPLETADA! 🎉                 ║
╚══════════════════════════════════════════════════════════════╝

Você completou todos os 7 GEMs do Sistema SAC Learning!

✅ **Você agora tem:**
- Mapeamento completo de seus papéis (M.A.P.A.)
- Diagnóstico claro do problema (F.O.C.O.)
- Validação estratégica do investimento
- Método científico validado (Método Ouro)
- Domínio ativo certificado
- Plano de implementação macro
- KBF personalizado operacional

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 **PRÓXIMO PASSO: Manual de OPERADOR PRÁTICO**

Agora use o Manual de OPERADOR PRÁTICO para:
1. Executar diariamente com seu KBF
2. Gravar feedbacks (Otter.ai)
3. Alimentar seu KBF com transcrições reais
4. Evoluir continuamente baseado em dados reais

🎯 **Lembre-se:** Este não é o fim, é o COMEÇO da implementação!

Digite 'reiniciar' para começar uma nova jornada
Digite 'status' para revisar seu progresso
"""
            return message, None

    def get_gem_context(self, gem_id: str) -> str:
        """
        Retorna o contexto necessário para um GEM específico.

        Args:
            gem_id: ID do GEM

        Returns:
            Instruções completas do GEM
        """
        gem_info = get_gem_info(gem_id)
        return gem_info.get("instructions", "")

    def save_gem_conversation(self, gem_id: str, messages: List[Dict]) -> None:
        """
        Salva o histórico de conversas de um GEM.

        Args:
            gem_id: ID do GEM
            messages: Lista de mensagens (role + content)
        """
        if "gem_conversations" not in self.state:
            self.state["gem_conversations"] = {}

        self.state["gem_conversations"][gem_id] = messages
        self._save_state()

    def get_shared_context(self) -> str:
        """
        Constrói contexto compartilhado com HISTÓRICO COMPLETO de GEMs anteriores.

        IMPORTANTE: Compartilha conversas completas para continuidade da experiência.

        Returns:
            String com contexto formatado incluindo histórico de conversas
        """
        if not self.state.get("completed_gems"):
            return ""

        context_parts = ["**📚 CONTEXTO DA SUA JORNADA (GEMs anteriores):**\n"]
        context_parts.append("Use as informações abaixo para personalizar sua abordagem.\n")

        for gem_id in self.state["completed_gems"]:
            gem_info = get_gem_info(gem_id)
            gem_output = self.state.get("gem_outputs", {}).get(gem_id, {})
            gem_conversation = self.state.get("gem_conversations", {}).get(gem_id, [])

            context_parts.append(f"\n{'='*70}")
            context_parts.append(f"**{gem_info['emoji']} {gem_info['name']}:**\n")

            # Inclui o output estruturado
            if "output" in gem_output:
                output_text = gem_output['output']
                context_parts.append(f"**Resultado:**\n{output_text}\n")

            # Inclui resumo do histórico de conversa (apenas mensagens do usuário e assistente)
            if gem_conversation:
                context_parts.append("**Principais pontos da conversa:**")
                user_messages = []
                assistant_messages = []

                for msg in gem_conversation:
                    if msg.get("role") == "user":
                        content = msg.get("content", "")
                        if len(content) > 200:
                            content = content[:200] + "..."
                        user_messages.append(f"  - {content}")
                    elif msg.get("role") == "assistant":
                        content = msg.get("content", "")
                        if len(content) > 300:
                            content = content[:300] + "..."
                        assistant_messages.append(f"  - {content}")

                # Limita a 3 interações mais relevantes para não sobrecarregar
                if user_messages:
                    context_parts.append("\nO que o usuário compartilhou:")
                    context_parts.extend(user_messages[:3])

                if assistant_messages:
                    context_parts.append("\nPrincipais descobertas/recomendações:")
                    context_parts.extend(assistant_messages[:3])

        context_parts.append(f"\n{'='*70}\n")
        context_parts.append("**💡 IMPORTANTE:**")
        context_parts.append("- Use essas informações para NÃO pedir dados que já foram coletados")
        context_parts.append("- Personalize sua abordagem com base no perfil e contexto revelado")
        context_parts.append("- Mantenha continuidade emocional e técnica com a jornada anterior\n")

        return "\n".join(context_parts)

    def update_shared_context(self, gem_id: str, summary: str) -> None:
        """
        Atualiza o contexto compartilhado com informações de um GEM.

        Args:
            gem_id: ID do GEM
            summary: Resumo das informações importantes do GEM
        """
        if "shared_context" not in self.state:
            self.state["shared_context"] = ""

        gem_info = get_gem_info(gem_id)
        context_update = f"\n\n**{gem_info['emoji']} {gem_info['name']}:**\n{summary}"

        self.state["shared_context"] += context_update
        self._save_state()

    def reset_journey(self) -> str:
        """Reinicia a jornada do usuário."""
        # Create backup before resetting
        if os.path.exists(self.state_file):
            backup_path = f"{self.state_file}.backup"
            shutil.copy2(self.state_file, backup_path)
        
        self.state = {
            "current_gem": None,
            "completed_gems": [],
            "gem_outputs": {},
            "started_at": None,
            "last_updated": None
        }
        self._save_state()

        return """
🔄 **JORNADA REINICIADA**

Todos os dados anteriores foram mantidos no arquivo user_journey.json.backup
Você pode começar uma nova jornada agora!

Digite 'iniciar' para começar do zero.
"""

    def handle_command(self, user_input: str) -> tuple[str, Optional[str]]:
        """
        Processa comandos do orquestrador.

        Args:
            user_input: Input do usuário

        Returns:
            Tuple com (resposta, gem_id ou None)
        """
        command = user_input.lower().strip()

        if command in ["iniciar", "start", "começar"]:
            return self.start_journey()

        elif command in ["status", "progresso", "progress"]:
            return self.get_current_status(), None

        elif command in ["listar", "list", "gems"]:
            return self.list_gems(), None

        elif command in ["continuar", "continue", "próximo", "next"]:
            current_gem = self.get_current_gem()
            if current_gem:
                gem_info = get_gem_info(current_gem)
                return f"Continuando com {gem_info['emoji']} {gem_info['name']}...", current_gem
            else:
                return "Você ainda não iniciou ou já completou todos os GEMs.", None

        elif command in ["reiniciar", "reset"]:
            return self.reset_journey(), None

        elif command in ["ajuda", "help", "?"]:
            return self.get_welcome_message(), None

        else:
            return None, None  # Não é um comando, passar para o GEM
