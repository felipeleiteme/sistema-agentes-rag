# 📚 GEMs - Instruções Completas de Referência

Este documento contém as instruções detalhadas de cada GEM para referência e manutenção.

## Status de Implementação

✅ As instruções estão integradas no sistema através de `src/agents/gems.py`
✅ O `gems_service.py` usa essas instruções como system message para o LLM
✅ Cada GEM segue rigorosamente seu protocolo específico
✅ **HISTÓRICO COMPARTILHADO**: GEMs recebem contexto completo dos anteriores para continuidade

## 🔄 Arquitetura de Compartilhamento de Contexto

### Como Funciona

**Quando o usuário inicia o GEM 2 (ou qualquer GEM posterior):**

1. O sistema carrega o **histórico completo do GEM 1**
2. Injeta no contexto do GEM 2:
   - ✅ Outputs estruturados (IDs, resultados)
   - ✅ Principais mensagens do usuário
   - ✅ Principais descobertas/recomendações
3. O GEM 2 pode:
   - ❌ NÃO pedir informações já coletadas
   - ✅ Personalizar abordagem baseada no perfil revelado
   - ✅ Manter continuidade emocional e técnica

**Benefício:** Experiência fluida e personalizada sem repetições desnecessárias

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

1. **SEMPRE usar contexto de GEMs anteriores da MESMA JORNADA**
2. **NÃO pedir informações já coletadas por GEMs anteriores**
3. **Personalizar abordagem com base no perfil e histórico revelado**
4. **Conduzir protocolo completo mas com continuidade**
5. **Linguagem humana, calorosa e empática**
6. **Rigor no protocolo + flexibilidade no tom**
7. **Guiar, não julgar**
8. **Saídas estruturadas com IDs únicos**

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

### Fluxo Técnico

- As instruções estão em `src/agents/gems.py`
- O `gems_service.py` injeta como system message no LLM
- Cada GEM salva seu histórico em `orchestrator.save_gem_conversation()`
- O `orchestrator.get_shared_context()` constrói contexto enriquecido com:
  - Outputs estruturados dos GEMs anteriores
  - Resumo das 3 principais mensagens do usuário
  - Resumo das 3 principais descobertas/recomendações
- PDFs de referência não devem ser misturados com informações do usuário

### Diferença Importante

**❌ Antes:** Cada GEM era totalmente independente, sem acesso a histórico anterior
**✅ Agora:** Cada GEM recebe contexto completo da jornada para melhor experiência

**Mantido:** Cada GEM AINDA pode funcionar standalone se necessário (autossuficiência)
**Novo:** Quando em jornada sequencial, há continuidade e personalização
