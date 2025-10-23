# 🌟 SAC Learning GEMS

## Sistema de Aprendizado Modular

Sistema com 7 agentes especializados (GEMs) que revolucionam a curva de aprendizado através de **aprendizado interativo** — prática guiada por agentes especializados.

---

## 🎯 Conceito Central

### 💎 Sistema de Amplificação Cognitiva

Os 7 GEMs trabalham em conjunto compartilhando contexto. Cada GEM lembra e usa as informações dos anteriores para criar uma experiência personalizada e contextualizada.

**10% PDF Guia Rápido** - Visão geral e troubleshooting
**90% Aprendizado Interativo** - Prática guiada nos Gems especializados

---

## 🗺️ Os 7 GEMs

### 1. 🗺️ Mestre do Mapeamento
**Portal de Entrada para Organização Holística**
- ⏰ Duração: 45 minutos
- 🎯 Objetivo: Mapeamento holístico de papéis de vida usando sistema M.A.P.A.
- 📋 Output: `MAPA-[ANO]-[MES]-001`

### 2. 🔍 Diagnosticador F.O.C.O.
**Clarificador de Problemas**
- ⏰ Duração: 20-40 minutos
- 🎯 Objetivo: Separar Fatos, Emoções e Contexto
- 📋 Output: `FOCO-[ANO]-[TEMA]-001`

### 3. ⚖️ Validador Estratégico
**Consultor de Energia Pessoal**
- ⏰ Duração: 30 minutos
- 🎯 Objetivo: Validar investimento de energia (scoring 40/30/30)
- 📋 Output: `DECISÃO: INVISTA/CONDICIONAL/AGUARDE/ACEITE`

### 4. 🔬 Laboratório Científico
**Painel de Validação Multi-IA**
- ⏰ Duração: 30-45 minutos
- 🎯 Objetivo: Encontrar método científico validado
- 📋 Output: `METODO-[ANO]-[TEMA]-001`

### 5. 🎓 Tutor Socrático
**Certificação de Domínio**
- ⏰ Duração: 60 minutos
- 🎯 Objetivo: Validar domínio ativo em 4 níveis
- 📋 Output: `CERTIFICAÇÃO: APROVADO/REPROVADO`

### 6. 🏗️ Arquiteto de Implementação
**Planejador Macro**
- ⏰ Duração: 40 minutos
- 🎯 Objetivo: Transformar método em plano detalhado
- 📋 Output: `PLANO-[ANO]-[TEMA]-001`

### 7. 💎 Construtor de Sistemas
**Arquiteto de KBFs**
- ⏰ Duração: 30 minutos
- 🎯 Objetivo: Criar assistente IA personalizado (KBF)
- 📋 Output: `KBF-[ANO]-[NOME]-001`

---

## 🚀 Instalação e Uso

### Pré-requisitos

```bash
# 1. Instale o Ollama
brew install ollama
brew services start ollama
ollama pull llama3.2:3b

# 2. Clone o repositório (se ainda não tiver)
cd meu_sistema_agentes

# 3. Ative o ambiente virtual
source .venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt
```

### Iniciando o Sistema

```bash
# Execute o sistema SAC Learning GEMS
python3 sac_gems.py
```

### Comandos Disponíveis

Durante a interação com o sistema, você pode usar:

- `iniciar` - Inicia a jornada pelos 7 GEMs
- `status` - Mostra seu progresso atual
- `listar` - Lista todos os GEMs disponíveis
- `continuar` - Continua com o GEM atual
- `reiniciar` - Reinicia a jornada
- `ajuda` - Mostra mensagem de ajuda
- `sair` - Encerra o sistema

---

## 📊 Fluxo Completo

```
Tempo total: 4-6 horas (distribuídas em vários dias)

┌─────────────────────────────────────┐
│  1. Mestre do Mapeamento (45 min)   │
│     → MAPA-2025-10-001              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Diagnosticador F.O.C.O. (20-40) │
│     → FOCO-2025-TEMA-001            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Validador Estratégico (30 min)  │
│     → DECISÃO: INVISTA              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. Laboratório Científico (30-45)  │
│     → METODO-2025-TEMA-001          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  5. Tutor Socrático (60 min)        │
│     → CERTIFICAÇÃO: APROVADO        │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  6. Arquiteto de Implementação (40) │
│     → PLANO-2025-TEMA-001           │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  7. Construtor de Sistemas (30 min) │
│     → KBF-2025-NOME-001             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Manual de OPERADOR PRÁTICO         │
│  Execução diária + Evolução         │
└─────────────────────────────────────┘
```

---

## 🔑 Pontos Críticos de Design

### 1. 🔒 Autossuficiência Total
Cada GEM funciona como aplicativo independente - coleta todas informações necessárias na própria sessão.

### 2. 📚 Contexto Educativo Obrigatório
Todo GEM explica rapidamente o conceito científico antes de aplicar.

### 3. ⏱️ Protocolos Estruturados
Fluxo claro com tempos definidos evita conversas infinitas.

### 4. 🎯 Orientação para Próximo Passo
Todo GEM termina indicando especificamente qual ferramenta usar depois.

### 5. 📋 Formato de Saída Padronizado
Resultados estruturados com IDs únicos.

### 6. 🔄 Validação Cruzada Inteligente
Sistema reconhece quando usuário traz resultados de GEMs anteriores.

### 7. ⚡ Protocolo Temporal Rígido
Limites de tempo forçam síntese e evitam perfeccionismo paralisante.

---

## 📁 Estrutura do Projeto

```
meu_sistema_agentes/
├── sac_gems.py                     # Ponto de entrada principal
├── src/
│   └── agents/
│       ├── gems.py                 # Definições dos 7 GEMs
│       ├── orchestrator.py         # Orquestrador principal
│       ├── gems_service.py         # Serviço de integração
│       └── ...
├── data/
│   └── sac_gems_knowledge.txt      # Base de conhecimento
├── user_journey.json               # Estado da jornada (auto-gerado)
└── SAC_GEMS_README.md              # Este arquivo
```

---

## 🎯 Resultado Final

Após completar os 7 GEMs, você terá:

- ✅ **Mapeamento completo** de seus papéis de vida (M.A.P.A.)
- ✅ **Diagnóstico claro** do problema (F.O.C.O.)
- ✅ **Validação estratégica** do investimento de energia
- ✅ **Método científico validado** com base em pesquisas
- ✅ **Domínio ativo certificado** através de 4 níveis
- ✅ **Plano de implementação macro** detalhado e progressivo
- ✅ **KBF personalizado operacional** (assistente IA que te conhece)

### 📖 Manual de OPERADOR PRÁTICO

Com seu KBF criado, você:
1. Consulta o KBF para plano micro diário
2. Executa e grava feedback em áudio
3. Alimenta o KBF com transcrições reais
4. Repete diariamente por 7 dias
5. Sistema evolui automaticamente com sua realidade

**Este não é o fim, é o COMEÇO da implementação!**

---

## 🛠️ Tecnologias

- **LangChain**: Framework para LLMs
- **Ollama**: Runtime para LLMs locais
- **Llama 3.2**: LLM da Meta (3B parâmetros)
- **Python**: Linguagem principal
- **JSON**: Persistência de estado

---

## 📄 Licença

MIT

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Este é um sistema modular e cada GEM pode ser melhorado independentemente.

### Áreas de Melhoria

- Adicionar mais GEMs especializados
- Melhorar detecção de conclusão de GEMs
- Adicionar exportação de jornada completa
- Interface web para melhor UX
- Integração com NotebookLM e outras ferramentas

---

## 📞 Suporte

Para questões ou sugestões, abra uma issue no repositório.

**Boa jornada pelos GEMs! 💎**
