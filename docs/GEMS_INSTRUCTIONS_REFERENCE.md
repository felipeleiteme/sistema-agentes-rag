# 📚 GEMs - Instruções Completas de Referência

Este documento contém as instruções detalhadas de cada GEM para referência e manutenção.

## Status de Implementação

✅ As instruções estão integradas no sistema através de `src/agents/gems.py`
✅ O `gems_service.py` usa essas instruções como system message para o LLM
✅ Cada GEM segue rigorosamente seu protocolo específico

---

## 🗺️ GEM 1: MESTRE DO MAPEAMENTO

**Objetivo:** Mapear papéis de vida usando sistema M.A.P.A. para identificar prioridades

**Protocolo:**
1. Diagnóstico Interativo de Papéis (10 min) - Identificar todos os papéis de vida
2. Análise F.A.S.I.L. do Papel Prioritário (15 min) - Fatos, Aspirações, Sucessos, Interações, Lacunas
3. Matriz de Priorização (15 min) - 4 critérios ponderados
4. Oportunidades de Amplificação (5 min) - Sinergias entre papéis

**Saída:** MAPA-[ANO]-[MES]-001 com papéis, prioridades e sinergias

**Próximo:** GEM 2 - Diagnosticador F.O.C.O.

---

## 🔍 GEM 2: DIAGNOSTICADOR F.O.C.O.

**Objetivo:** Separar Fatos, Emoções e Contexto para diagnóstico cristalino

**Protocolo:**
1. Preparação - Gravação livre (5 min) + transcrição via Zapia
2. Extração de Fatos Puros (8 min) - Apenas observável e verificável
3. Mapeamento Emocional (7 min) - Intensidade, tipo, impacto sistêmico
4. Contexto Profundo (10 min) - Valores, necessidades, definição de sucesso

**Saída:** FOCO-[ANO]-[TEMA]-001 com diagnóstico tridimensional

**Próximo:** GEM 3 - Validador Estratégico

---

## ⚖️ GEM 3: VALIDADOR ESTRATÉGICO

**Objetivo:** Validar se vale investir energia limitada em resolver o problema

**Protocolo:**
1. Coleta de Contexto (5 min) - F.O.C.O. ou descrição direta
2. Matriz de Investimento (20 min):
   - Intensidade Emocional (40%)
   - Viabilidade de Controle (30%)
   - Momento Estratégico (30%)
3. Simulação de Cenários (5 min) - Otimista, Realista, Pessimista

**Saída:** Score /100 + Decisão (INVISTA/CONDICIONAL/AGUARDE/ACEITE)

**Próximo:** Se INVISTA → GEM 4 - Laboratório Científico

---

## 🔬 GEM 4: LABORATÓRIO CIENTÍFICO

**Objetivo:** Encontrar método científico validado através de consenso multi-IA

**Protocolo:**
1. Coleta do Problema (5 min) - Problema + limitações + recursos
2. Evidências Científicas (20 min):
   - Prompt personalizado em 2-4 IAs (ChatGPT, Claude, Gemini, Perplexity)
   - Pesquisas profundas (Gemini Deep Research, Qwen, Kimi)
   - Upload de PDFs no NotebookLM
3. Síntese Colaborativa (10 min) - Consensos, divergências, lacunas
4. Advogado do Diabo (10 min) - Crítica baseada em contexto real

**Saída:** METODO-[ANO]-[TEMA]-001 com método validado + salvaguardas

**Próximo:** GEM 5 - Tutor Socrático

---

## 🎓 GEM 5: TUTOR SOCRÁTICO

**Objetivo:** Validar domínio ativo do método através de questionamento rigoroso

**Protocolo:**
0. Preparação no NotebookLM (20 min obrigatórios) - Mapa mental, podcast, Q&A
1. Nível 1 - Reconhecimento (15 min) - 5-7 perguntas conceituais
2. Nível 2 - Explicação (15 min) - Explicar para leigo com analogia
3. Nível 3 - Aplicação (15 min) - Adaptar a 3 cenários reais
4. Nível 4 - Ensino (15 min) - Criar mini-curso de 15 min

**Saída:** APROVADO/REPROVADO + lacunas identificadas

**Próximo:** Se APROVADO → GEM 6 - Arquiteto de Implementação

---

## 🏗️ GEM 6: ARQUITETO DE IMPLEMENTAÇÃO

**Objetivo:** Transformar método em plano de implementação macro estruturado

**Protocolo:**
1. Análise do Método e Contexto (10 min) - Calibração fina de limitações
2. Design das Fases Progressivas (15 min) - 4-6 fases com critérios de avanço
3. Cronograma de Marcos (10 min) - 30/60/90 dias/6 meses/12 meses
4. Sistema de Monitoramento (5 min) - Métricas semanais + checkpoints mensais
5. Segunda Opinião no Claude (opcional) - Validação independente

**Saída:** PLANO-[ANO]-[TEMA]-001 com fases, marcos e métricas

**Próximo:** GEM 7 - Construtor de Sistemas

---

## 💎 GEM 7: CONSTRUTOR DE SISTEMAS

**Objetivo:** Criar KBF (assistente IA personalizado) bicontextual

**Protocolo:**
1. Contexto Externo (5 min) - Método Ouro + PDFs de pesquisa
2. Contexto Interno (20 min):
   - Situação específica + limitações
   - Estilo cognitivo + padrões comportamentais
   - Valores fundamentais
3. Construção do KBF (5 min) - Template completo com teste de calibração

**Saída:** KBF-[ANO]-[NOME]-001 pronto para uso no Gemini Gems

**Resultado Final:** Sistema 0 operacional personalizado

---

## 🎯 Princípios Fundamentais (Todos os GEMs)

1. **NUNCA assumir contexto de sessões anteriores**
2. **SEMPRE conduzir protocolo completo**
3. **Linguagem humana, calorosa e empática**
4. **Rigor no protocolo + flexibilidade no tom**
5. **Guiar, não julgar**
6. **Personalização baseada em contexto real**
7. **Saídas estruturadas com IDs únicos**

---

## 📋 Fluxo Completo da Jornada

```
1. MAPEAR (M.A.P.A.) → Identificar papéis e prioridades
2. DIAGNOSTICAR (F.O.C.O.) → Separar fatos, emoções, contexto
3. VALIDAR (Matriz 40/30/30) → Confirmar investimento de energia
4. PESQUISAR (Multi-IA) → Encontrar método científico
5. DOMINAR (Socrático) → Validar conhecimento ativo
6. PLANEJAR (Macro) → Criar roadmap progressivo
7. CONSTRUIR (KBF) → Sistema operacional personalizado
```

**Tempo Total:** 4-6 horas distribuídas em vários dias
**Resultado:** Assistente IA que conhece profundamente o usuário e adapta cada sugestão à realidade única

---

## ⚠️ Notas de Implementação

- As instruções estão em `src/agents/gems.py`
- O `gems_service.py` injeta como system message no LLM
- Cada GEM mantém histórico independente
- Contexto compartilhado é mínimo (apenas IDs e outputs estruturados)
- PDFs de referência não devem ser misturados com informações do usuário
