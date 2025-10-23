# 🚀 Guia Rápido - SAC Learning GEMS

## Início Rápido em 3 Passos

### 1️⃣ Prepare o Ambiente

```bash
# Certifique-se que o Ollama está rodando
ollama list

# Se não estiver, inicie:
brew services start ollama
ollama pull llama3.2:3b

# Ative o ambiente virtual
cd meu_sistema_agentes
source .venv/bin/activate
```

### 2️⃣ Execute o Sistema

```bash
python3 sac_gems.py
```

### 3️⃣ Comece sua Jornada

```
💬 Você: iniciar
```

---

## 📋 Comandos Essenciais

| Comando | Descrição |
|---------|-----------|
| `iniciar` | Inicia a jornada pelos 7 GEMs |
| `status` | Mostra seu progresso atual |
| `listar` | Lista todos os GEMs disponíveis |
| `continuar` | Continua com o GEM atual |
| `ajuda` | Mostra mensagem de ajuda |
| `sair` | Encerra o sistema (progresso salvo) |

---

## 🗺️ Jornada pelos GEMs

### GEM 1: Mestre do Mapeamento (45 min) 🗺️

**O que você vai fazer:**
- Listar todos os papéis que você desempenha na vida
- Identificar qual papel é mais importante agora
- Priorizar com base em impacto emocional e sinergia
- Descobrir oportunidades de amplificação

**O que você vai receber:**
```
MAPA-2025-10-001
- Lista de papéis identificados
- Papel prioritário com análise F.A.S.I.L.
- Matriz de priorização
- Oportunidades de amplificação
```

### GEM 2: Diagnosticador F.O.C.O. (20-40 min) 🔍

**O que você vai fazer:**
- Separar fatos de emoções e contexto
- Mapear o impacto emocional do problema
- Identificar a necessidade profunda

**Dica:** Grave um áudio de 3-5 minutos explicando sua situação e transcreva via Zapia (https://zapia.com/)

**O que você vai receber:**
```
FOCO-2025-TEMA-001
- Fatos objetivos
- Impacto emocional (1-10)
- Necessidade profunda e valores
```

### GEM 3: Validador Estratégico (30 min) ⚖️

**O que você vai fazer:**
- Avaliar se vale investir energia neste problema
- Analisar 3 dimensões: Intensidade (40%), Controle (30%), Momento (30%)
- Simular cenários otimista, realista e pessimista

**O que você vai receber:**
```
SCORING: 77.8/100
DECISÃO: INVISTA
- Se INVISTA → Vá para o Laboratório Científico
- Se CONDICIONAL → Melhore uma variável primeiro
- Se AGUARDE/ACEITE → Analise outro desafio
```

### GEM 4: Laboratório Científico (30-45 min) 🔬

**O que você vai fazer:**
- Buscar método científico validado para seu problema
- Consultar 2-4 IAs diferentes (ChatGPT, Claude, Gemini, Perplexity)
- Criar notebook no NotebookLM com as pesquisas
- Validar com "Advogado do Diabo"

**Ferramentas necessárias:**
- ChatGPT (https://chatgpt.com/)
- Claude (https://claude.ai/)
- Gemini (https://gemini.google.com/app)
- NotebookLM (https://notebooklm.google.com/)

**O que você vai receber:**
```
METODO-2025-TEMA-001
- Nome do método
- Princípio central
- Base científica
- Etapas de implementação
- Métricas de progresso
- Salvaguardas críticas
```

### GEM 5: Tutor Socrático (60 min) 🎓

**O que você vai fazer:**
- Validar seu domínio do Método Ouro em 4 níveis
- Estudar com NotebookLM (mapa mental, podcast, Q&A)
- Reconhecer → Explicar → Aplicar → Ensinar

**Pré-requisito:** Jejum cognitivo de 24h após ler o Método Ouro

**O que você vai receber:**
```
CERTIFICAÇÃO DE DOMÍNIO
RESULTADO: APROVADO ou REPROVADO
- Se APROVADO → Arquiteto de Implementação
- Se REPROVADO → Revise lacunas e refaça em 48h
```

### GEM 6: Arquiteto de Implementação (40 min) 🏗️

**O que você vai fazer:**
- Transformar Método Ouro em plano detalhado
- Criar 4-6 fases progressivas
- Definir cronograma de marcos (30/60/90 dias)
- Estabelecer sistema de monitoramento

**Opcional mas recomendado:** Buscar segunda opinião no Claude

**O que você vai receber:**
```
PLANO-2025-TEMA-001
- Nome do plano
- Visão de sucesso (12 meses)
- Arquitetura das fases
- Cronograma de marcos
- Sistema de monitoramento
- Salvaguardas integradas
```

### GEM 7: Construtor de Sistemas (30 min) 💎

**O que você vai fazer:**
- Criar seu KBF (assistente IA personalizado)
- Combinar Contexto Externo (Método Ouro) + Contexto Interno (seu perfil)
- Definir protocolos operacionais
- Testar calibração

**O que você vai receber:**
```
KBF-2025-NOME-001
- Instruções completas do seu assistente
- Contexto externo e interno
- Protocolo operacional
- Teste de calibração
```

**Como usar:** Cole no Gemini Gems (https://gemini.google.com/app)

---

## 📖 Depois dos 7 GEMs: Manual de OPERADOR PRÁTICO

### Ciclo Diário

```
1. Consulte seu KBF → Plano micro do dia
2. Execute → Grave áudio de feedback
3. Transcreva (Otter.ai ou Zapia)
4. Alimente o KBF com feedback
5. Repita por 7 dias
```

### Ferramentas para Execução

- **KBF Operacional:** Gemini Gems
- **Gravação de Feedback:** Otter.ai (https://otter.ai/) ou Zapia
- **Revisão:** NotebookLM

### Regras de Ouro

- ✅ Nunca pule a gravação (combustível da evolução)
- ✅ Nunca execute sem consultar KBF primeiro
- ✅ Nunca interprete feedback sozinho
- ✅ Sempre use roadmap como bússola

---

## 🎯 Dicas de Sucesso

### 1. Separe Tempo
- Reserve 1-2 horas por GEM
- Não tente fazer todos no mesmo dia
- Faça pausas entre GEMs

### 2. Prepare os Materiais
- Antes do GEM 2: Grave áudio da situação
- Antes do GEM 4: Crie contas nas IAs
- Antes do GEM 5: Estude com NotebookLM

### 3. Salve Tudo
- Seu progresso fica em `user_journey.json`
- Copie os outputs de cada GEM
- Organize em uma pasta/nota

### 4. Seja Honesto
- Os GEMs funcionam melhor com honestidade
- Não idealize sua situação
- Compartilhe limitações reais

---

## ❓ Perguntas Frequentes

**P: Posso pular um GEM?**
R: Não recomendado. Cada GEM prepara o próximo. O sistema é sequencial.

**P: Preciso fazer tudo de uma vez?**
R: Não! Distribua em vários dias. O sistema salva seu progresso.

**P: Posso voltar a um GEM anterior?**
R: Sim, use o comando `reiniciar` ou acesse diretamente.

**P: E se o LLM der uma resposta ruim?**
R: Reformule sua pergunta com mais contexto. Os GEMs são guiados por instruções detalhadas.

**P: Quanto custa?**
R: 100% gratuito usando Ollama local. Ferramentas externas (ChatGPT, Claude, etc.) têm planos gratuitos suficientes.

---

## 🐛 Troubleshooting

### Ollama não responde
```bash
brew services restart ollama
ollama list
```

### Respostas muito lentas
- Normal! Modelo local demora 10-15s
- Primeira execução é mais lenta

### Erro ao processar mensagem
- Verifique se o Ollama está rodando
- Tente reiniciar o script
- Seu progresso está salvo

---

## 📞 Suporte

Para questões ou sugestões, consulte o [README completo do SAC Learning GEMS](SAC_GEMS_README.md).

**Boa jornada! 💎**
