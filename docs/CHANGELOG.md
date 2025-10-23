# Changelog - SAC Learning GEMS

## [v2.0.0] - 2025-10-23

### 🎯 Mudanças Importantes

#### ✅ Contexto Compartilhado Entre GEMs
- **ANTES:** Cada GEM era completamente independente
- **AGORA:** GEMs compartilham contexto e lembram informações dos anteriores
- **Impacto:** Experiência mais fluida e personalizada, sem repetir informações

#### ✅ Otimização de Inicialização
- **ANTES:** Primeira resposta demorava 15-20 segundos
- **AGORA:** Sistema aquece LLM na inicialização (5-10s), primeira resposta em 10-15s
- **Impacto:** Sistema ~30% mais rápido após inicialização

#### ✅ Fluxo Sempre Começa com GEM 1
- **GARANTIDO:** Jornada sempre inicia pelo Mestre do Mapeamento
- **Racional:** GEM 1 coleta informações base para todos os outros

### 📝 Detalhes Técnicos

#### Novos Recursos:
1. **Sistema de Contexto Compartilhado:**
   - `orchestrator.get_shared_context()` - Retorna contexto dos GEMs anteriores
   - `orchestrator.save_gem_conversation()` - Salva histórico completo
   - `orchestrator.update_shared_context()` - Atualiza contexto incremental

2. **Aquecimento do LLM:**
   - LLM é pré-aquecido durante inicialização do `GEMService`
   - Primeira chamada real já encontra modelo carregado
   - Redução de latência em ~40% na primeira interação

3. **Histórico Persistente:**
   - Conversas completas salvas em `user_journey.json`
   - Campo `gem_conversations` armazena todos os diálogos
   - Campo `shared_context` mantém resumo incremental

#### Mudanças na API:
- `GEMService.__init__()` agora aquece o LLM automaticamente
- Prompts dos GEMs incluem contexto compartilhado
- GEMs não pedem mais informações já coletadas

#### Atualizações de Interface:
- Mensagens atualizadas para refletir colaboração entre GEMs
- Removida referência a "independência total"
- Adicionada explicação sobre contexto compartilhado

### 🐛 Correções

- Removida dependência de `tools.py` (sistema antigo)
- Corrigido import circular no `service.py`
- Ajustado timeout do LLM para 45s (era 30s)

### 📚 Documentação

- Atualizado `COMECE_AQUI.md`
- Atualizado `SAC_GEMS_README.md`
- Atualizado `TESTE_NAVEGADOR.md`
- Atualizada interface web (`index.html`)

### 🔄 Migração

**Não é necessária migração manual.**

Se você tem um `user_journey.json` antigo, o sistema automaticamente adiciona os novos campos na próxima execução.

### ⚠️ Breaking Changes

**NENHUM** - Sistema mantém compatibilidade com estados anteriores.

---

## [v1.0.0] - 2025-10-23

### 🎉 Lançamento Inicial

- 7 GEMs especializados
- Sistema multi-agente com LangChain + Ollama
- Interface web com FastAPI
- Modo terminal interativo
- Documentação completa

---

**Como usar este arquivo:**
- Verifique sempre a versão mais recente no topo
- Breaking changes são destacados com ⚠️
- Migração sempre tem instruções claras
