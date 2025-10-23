# 📋 Guia Completo de Testes e Validação

Este guia fornece instruções detalhadas para testar e validar todos os componentes do sistema.

## 📑 Índice

- [Pré-requisitos](#pré-requisitos)
- [Preparação do Ambiente](#preparação-do-ambiente)
- [Testes do Sistema Simples (CLI)](#testes-do-sistema-simples-cli)
- [Testes da Interface Web](#testes-da-interface-web)
- [Testes Automatizados](#testes-automatizados)
- [Testes do Sistema Avançado (CrewAI)](#testes-do-sistema-avançado-crewai)
- [Checklist de Validação](#checklist-de-validação)
- [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

Antes de começar os testes, certifique-se de ter:

- ✅ **Python 3.11+** instalado
- ✅ **Ollama** instalado e rodando
- ✅ **Modelo Llama 3.2 (3B)** baixado
- ✅ **Variáveis de ambiente** configuradas (arquivo `.env`)

---

## Preparação do Ambiente

### PASSO 1: Ativar Ambiente Virtual

```bash
cd /caminho/para/meu_sistema_agentes
source .venv/bin/activate
```

### PASSO 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

### PASSO 3: Verificar Ollama

```bash
# Verificar se Ollama está rodando
ollama list

# Deve mostrar o modelo llama3.2:3b
# Se não tiver, instalar:
ollama pull llama3.2:3b

# Testar o modelo
ollama run llama3.2:3b "Olá, como você está?"
```

**Saída esperada:**
```
NAME              ID              SIZE      MODIFIED
llama3.2:3b       abc123def...    2.0 GB    X days ago
```

### PASSO 4: Criar Índice FAISS

```bash
python ingest.py
```

**Saída esperada:**
```
Iniciando ingestão da base de conhecimento (usando embeddings TF-IDF)...
Carregando base de conhecimento a partir de: /caminho/docs/politica_rh.txt
Documento dividido em 8 pedaços.
Criando banco de dados vetorial FAISS...
✅ Base de conhecimento criada e salva como 'faiss_index'.
```

---

## Testes do Sistema Simples (CLI)

### Teste 1: Demonstração Automática

```bash
python simple_agent.py --demo
```

**O que esperar:**
- Sistema executa 3 perguntas pré-definidas
- Mostra classificação automática (RH vs Geral)
- Exibe respostas dos agentes

**Saída esperada:**
```
🎯 DEMONSTRAÇÃO DO SISTEMA

============================================================
TESTE: Pergunta sobre RH
============================================================

📋 Pergunta recebida: Quantos dias de férias tem um funcionário CLT?
------------------------------------------------------------
✅ Detectado: Pergunta sobre RH → Usando Agente RH com RAG
--- Ferramenta RAG Recebeu a Pergunta: Quantos dias de férias...
--- Contexto Encontrado: Funcionários CLT têm direito a 30 dias...

📤 RESPOSTA:
Funcionários CLT têm direito a 30 dias corridos de férias após 12 meses de trabalho.

============================================================
TESTE: Pergunta Geral
============================================================

📋 Pergunta recebida: Qual a capital do Brasil?
------------------------------------------------------------
✅ Detectado: Pergunta geral → Usando Agente Assistente

📤 RESPOSTA:
A capital do Brasil é Brasília.

============================================================
TESTE: Outra Pergunta sobre RH
============================================================

📋 Pergunta recebida: Qual o valor do bônus anual para funcionários PJ?
------------------------------------------------------------
✅ Detectado: Pergunta sobre RH → Usando Agente RH com RAG

📤 RESPOSTA:
Funcionários PJ recebem bônus anual de R$5.000,00 mediante entrega de projetos.

============================================================
✅ DEMONSTRAÇÃO CONCLUÍDA!
============================================================
```

### Teste 2: Pergunta Única

```bash
python simple_agent.py -q "Quantos dias de férias tem um funcionário CLT?"
```

**Validações:**
- ✅ Sistema identifica como pergunta de RH
- ✅ Usa ferramenta RAG
- ✅ Retorna resposta baseada na base de conhecimento

### Teste 3: Modo Interativo

```bash
python simple_agent.py
```

**Perguntas para testar:**

1. **Pergunta sobre RH:**
   ```
   Quantos dias de férias tenho direito?
   ```

2. **Pergunta Geral:**
   ```
   Qual a capital do Brasil?
   ```

3. **Pergunta sobre Benefícios:**
   ```
   Como funciona o regime PJ?
   ```

4. **Pergunta sobre Bônus:**
   ```
   Qual o valor do bônus anual para CLT?
   ```

**Para sair:**
```
sair
```

---

## Testes da Interface Web

### PASSO 1: Iniciar Servidor Web

```bash
# Terminal 1
cd /caminho/para/meu_sistema_agentes
source .venv/bin/activate
uvicorn src.web.app:app --reload --host 0.0.0.0 --port 8000
```

**Saída esperada:**
```
INFO:     Will watch for changes in these directories: ['/caminho/meu_sistema_agentes']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### PASSO 2: Testar Interface no Navegador

1. **Abra o navegador em:** `http://localhost:8000`

2. **Você verá:**
   - Interface web moderna com tema escuro
   - Campo de texto para perguntas
   - Botão "Enviar"
   - Área de histórico de conversas

3. **Faça estas perguntas:**

   **Pergunta 1 (RH):**
   ```
   Quantos dias de férias tem um funcionário CLT?
   ```

   **Resultado esperado:**
   - Mensagem aparece na área de chat
   - Mostra badge "🏢 Agente RH"
   - Exibe "✅ Contexto usado"
   - Mostra preview do contexto da base

   **Pergunta 2 (Geral):**
   ```
   Qual a capital do Brasil?
   ```

   **Resultado esperado:**
   - Mensagem aparece na área de chat
   - Mostra badge "💬 Assistente"
   - Exibe "⚪ Sem contexto"

   **Pergunta 3 (RH):**
   ```
   Qual o valor do bônus anual para funcionários PJ?
   ```

### PASSO 3: Testar API REST Diretamente

```bash
# Terminal 2 (novo terminal)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Quantos dias de férias tem um funcionário CLT?"}'
```

**Resposta esperada (JSON):**
```json
{
  "question": "Quantos dias de férias tem um funcionário CLT?",
  "answer": "Funcionários CLT têm direito a 30 dias corridos de férias após 12 meses de trabalho.",
  "agent": "rh",
  "used_context": true,
  "context_preview": "Funcionários CLT têm direito a 30 dias corridos de férias após 12 meses de trabalho...",
  "error": null
}
```

### PASSO 4: Testar Health Check

```bash
curl http://localhost:8000/
```

Deve retornar o HTML da página principal.

---

## Testes Automatizados

### Executar Todos os Testes

```bash
pytest tests/ -v
```

**Saída esperada:**
```
tests/test_agent_service.py::test_classify_hr_question PASSED
tests/test_agent_service.py::test_classify_general_question PASSED
tests/test_agent_service.py::test_answer_hr_question PASSED
tests/test_agent_service.py::test_answer_general_question PASSED
tests/test_web_app.py::test_read_home PASSED
tests/test_web_app.py::test_chat_endpoint PASSED

========================= 6 passed in 2.34s =========================
```

### Executar Teste Específico

```bash
# Testar apenas serviço de agentes
pytest tests/test_agent_service.py -v

# Testar apenas API web
pytest tests/test_web_app.py -v
```

### Executar com Cobertura

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Testes do Sistema Avançado (CrewAI)

⚠️ **Estes testes requerem LiteLLM Proxy e APIs pagas (OpenAI/Anthropic)**

### PASSO 1: Configurar Variáveis de Ambiente

Verifique se o arquivo `.env` contém:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LITELLM_PROXY_URL=http://localhost:4000
```

### PASSO 2: Iniciar LiteLLM Proxy

```bash
# Terminal separado
cd /caminho/para/meu_sistema_agentes
litellm --config config/litellm_config.yaml --port 4000
```

**Saída esperada:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000
```

### PASSO 3: Testar Health do Proxy

```bash
curl http://localhost:4000/health
```

**Resposta esperada:**
```json
{"status": "healthy"}
```

### PASSO 4: Testar Agentes CrewAI

Crie um arquivo de teste `test_crew_manual.py`:

```python
from src.agents.crew_agents import ResearchCrew

def test_research_crew():
    crew = ResearchCrew()
    result = crew.create_crew("políticas de férias da empresa").kickoff()
    print("\n" + "="*60)
    print("RESULTADO DA CREW:")
    print("="*60)
    print(result)
    print("="*60)

if __name__ == "__main__":
    test_research_crew()
```

Execute:

```bash
python test_crew_manual.py
```

---

## Checklist de Validação

### ✅ Sistema Simple Agent (Ollama)

- [ ] **Ingestão**: `python ingest.py` cria `faiss_index/` sem erros
- [ ] **Classificação**: Sistema distingue perguntas RH de gerais
- [ ] **Agente RH**: Responde com contexto da base de conhecimento
- [ ] **Agente Geral**: Responde sem usar RAG
- [ ] **Modo Demo**: `--demo` executa 3 testes automaticamente
- [ ] **Modo Interativo**: Aceita perguntas livres e sai com "sair"
- [ ] **Modo Pergunta Única**: `-q "pergunta"` funciona

### ✅ Interface Web

- [ ] **Servidor**: Inicia sem erros na porta 8000
- [ ] **Página**: `http://localhost:8000` carrega interface
- [ ] **Chat**: Perguntas retornam respostas na interface
- [ ] **API**: `POST /api/chat` retorna JSON válido
- [ ] **Histórico**: Mensagens aparecem na área de chat
- [ ] **Badges**: Mostra corretamente agente usado e contexto
- [ ] **Responsivo**: Interface funciona em diferentes tamanhos de tela

### ✅ Testes Automatizados

- [ ] **pytest**: Todos os testes passam (6/6)
- [ ] **Serviço**: Testes de classificação funcionam
- [ ] **API**: Endpoints retornam status 200
- [ ] **Erro Handling**: Erros são tratados corretamente

### ✅ Sistema CrewAI (Opcional)

- [ ] **Proxy**: LiteLLM inicia e responde em `/health`
- [ ] **Configuração**: APIs OpenAI e Anthropic estão válidas
- [ ] **RAG Tool**: Ferramenta busca documentos corretamente
- [ ] **Agentes**: Crew executa tarefas sequencialmente
- [ ] **Modelos**: GPT-4o, Claude Haiku e Sonnet acessíveis

---

## Troubleshooting

### ❌ Erro: "Model not found" / "llama3.2:3b not available"

**Solução:**
```bash
ollama pull llama3.2:3b
ollama list  # Verificar se aparece
```

### ❌ Erro: "FAISS index not found"

**Solução:**
```bash
python ingest.py
ls faiss_index/  # Deve mostrar index.faiss e index.pkl
```

### ❌ Erro: "Connection refused" ao acessar API

**Causa:** Porta 8000 já está em uso

**Solução:**
```bash
# Ver processo usando a porta
lsof -i :8000

# Matar processo
kill -9 <PID>

# Ou usar outra porta
uvicorn src.web.app:app --reload --port 8001
```

### ❌ Erro: "Ollama connection error"

**Solução:**
```bash
# Verificar se Ollama está rodando
brew services list | grep ollama

# Iniciar se necessário
brew services start ollama

# Testar conexão
curl http://localhost:11434/api/tags
```

### ❌ Erro: "OpenAI API key invalid" (CrewAI)

**Solução:**
```bash
# Verificar se chave está no .env
cat .env | grep OPENAI_API_KEY

# Testar chave
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### ❌ Respostas muito lentas (>30s)

**Possíveis causas:**
1. **Primeira execução** - Ollama carrega modelo (normal)
2. **Hardware limitado** - Modelo 3B precisa de RAM suficiente
3. **Ollama sobrecarregado** - Reinicie o serviço

**Solução:**
```bash
brew services restart ollama
```

### ❌ Erro: "No module named 'sklearn'"

**Solução:**
```bash
pip install scikit-learn>=1.3.0
```

### ❌ Erro: "No module named 'langchain_ollama'"

**Solução:**
```bash
pip install langchain-ollama==0.1.3
```

### ❌ Interface web não carrega CSS/JS

**Causa:** Arquivos estáticos não encontrados

**Solução:**
```bash
# Verificar se arquivos existem
ls src/web/static/
ls src/web/templates/

# Reiniciar servidor
uvicorn src.web.app:app --reload
```

---

## Logs e Diagnóstico

### Ver logs do Ollama

```bash
# macOS
tail -f ~/.ollama/logs/server.log

# Linux
journalctl -u ollama -f
```

### Ver processos ativos

```bash
ps aux | grep -E "ollama|uvicorn|litellm"
```

### Testar conectividade com Ollama

```bash
# Listar modelos disponíveis
curl http://localhost:11434/api/tags

# Testar geração
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Olá!",
  "stream": false
}'
```

### Verificar uso de memória

```bash
# Ver uso de RAM
top -o MEM | head -20

# Ver uso do Ollama especificamente
ps aux | grep ollama | awk '{print $4}'  # % memória
```

---

## Exemplo de Sessão Completa

```bash
# Terminal 1: Preparar ambiente
cd /caminho/para/meu_sistema_agentes
source .venv/bin/activate
python ingest.py

# Terminal 1: Testar CLI
python simple_agent.py --demo

# Terminal 2: Iniciar servidor web
cd /caminho/para/meu_sistema_agentes
source .venv/bin/activate
uvicorn src.web.app:app --reload --port 8000

# Terminal 3: Testar API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Quantos dias de férias tem funcionário CLT?"}'

# Terminal 4: Rodar testes automatizados
pytest tests/ -v

# Navegador: Abrir interface
open http://localhost:8000
```

---

## 🎯 Critérios de Sucesso Final

O sistema está **100% funcional** se:

1. ✅ `python ingest.py` cria índice sem erros
2. ✅ `python simple_agent.py --demo` executa 3 testes com sucesso
3. ✅ Interface web acessível em `http://localhost:8000`
4. ✅ API retorna JSON válido em `/api/chat`
5. ✅ `pytest tests/ -v` - todos os 6 testes passam
6. ✅ Perguntas sobre RH usam RAG
7. ✅ Perguntas gerais não usam RAG
8. ✅ Respostas aparecem em menos de 20 segundos

---

## 📞 Suporte

Se encontrar problemas não listados aqui:

1. Verifique os logs do Ollama
2. Confirme que todas as dependências estão instaladas
3. Teste cada componente isoladamente
4. Revise o arquivo `.env`

**Boa sorte com os testes! 🚀**
