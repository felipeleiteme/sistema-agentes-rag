# Sistema de Agentes com RAG - 100% Gratuito

Sistema de agentes inteligentes usando **Ollama** (LLM local) + **LangChain** + **RAG** (Retrieval Augmented Generation) com embeddings TF-IDF customizados.

## 🎯 Características

- ✅ **100% Gratuito** - Sem APIs pagas
- ✅ **Local** - LLM Llama 3.2 (3B) via Ollama
- ✅ **RAG** - Busca semântica em base de conhecimento
- ✅ **Embeddings TF-IDF** - Sem dependência do PyTorch
- ✅ **Multi-agentes** - Sistema inteligente de roteamento
- ✅ **Interface Web Profissional** - Chat moderno com FastAPI + templates responsivos

## 🏗️ Arquitetura

```
Pergunta do Usuário
       ↓
Sistema Multi-Agente (Router)
       ↓
    ┌──────────────────┐
    │  Pergunta de RH? │
    └────┬─────────┬───┘
         │         │
      Sim│         │Não
         ↓         ↓
   Agente RH   Agente Geral
       ↓
  RAG Tool
       ↓
  FAISS Index
  (TF-IDF)
       ↓
  Llama 3.2
       ↓
   Resposta
```

## 📂 Estrutura do Projeto

```
meu_sistema_agentes/
├── custom_embeddings.py    # Embeddings TF-IDF customizados
├── tools.py                # Ferramenta RAG para busca
├── ingest.py               # Script para criar índice FAISS
├── chat_interativo.py      # Chat interativo (principal)
├── simple_agent.py         # Sistema multi-agente completo
├── test_agent.py           # Testes rápidos
├── politica_rh.txt         # Base de conhecimento
├── faiss_index/            # Índice vetorial FAISS
└── README.md               # Este arquivo
```

## 🚀 Instalação

### 1. Instale o Ollama

```bash
brew install ollama
brew services start ollama
ollama pull llama3.2:3b
```

### 2. Configure o ambiente Python

```bash
cd meu_sistema_agentes
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Crie o índice FAISS

```bash
python3 ingest.py
```

### 4. Inicie a interface web

```bash
uvicorn src.web.app:app --reload
```

Acesse `http://localhost:8000` para utilizar o hub com visual profissional. Todas as requisições continuam sendo executadas localmente, reutilizando o mesmo roteamento de agentes.

## 🎯 Como Usar

### Chat Interativo (Recomendado)

```bash
python3 chat_interativo.py
```

Faça perguntas sobre RH e receba respostas baseadas na base de conhecimento.

### Sistema Multi-Agente Completo

```bash
python3 simple_agent.py             # modo interativo
python3 simple_agent.py --question "Qual a política de home office?"
python3 simple_agent.py --demo      # demonstração automática
```

Use o modo interativo para fazer perguntas livremente, o parâmetro `--question` para rodadas únicas e `--demo` para ver os testes pré-configurados.

### Interface Web Profissional

```bash
uvicorn src.web.app:app --reload
```

- Interface moderna responsiva com histórico local de mensagens
- Indicação visual de qual agente respondeu e se o RAG foi utilizado
- Atualização dinâmica no navegador via JavaScript nativo

### Teste Rápido

```bash
python3 test_agent.py
```

Testa a ferramenta RAG e o LLM separadamente.

## 📝 Componentes

### Custom Embeddings (`custom_embeddings.py`)

Embeddings baseados em TF-IDF usando scikit-learn, evitando a dependência do PyTorch (incompatível com Python 3.13).

### Ferramenta RAG (`tools.py`)

Ferramenta de busca semântica que:
1. Carrega o índice FAISS
2. Busca os 3 documentos mais relevantes
3. Retorna o contexto para o LLM

### Sistema Multi-Agente (`simple_agent.py`)

**Agente RH**: Usa RAG para responder perguntas sobre políticas de RH
**Agente Geral**: Responde perguntas gerais sem ferramentas
**Router**: Detecta automaticamente qual agente usar

## ⚙️ Configuração

### Adicionar novos documentos

1. Adicione arquivos `.txt` na raiz do projeto
2. Modifique `ingest.py` para carregar novos arquivos
3. Execute `python3 ingest.py` para recriar o índice

### Ajustar parâmetros do LLM

Edite os arquivos Python e modifique:

```python
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.7  # Ajuste a criatividade (0.0-1.0)
)
```

### Mudar número de documentos retornados

Em `tools.py`:

```python
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Altere o número aqui
)
```

## 🐛 Troubleshooting

### Ollama não está rodando

```bash
brew services start ollama
ollama list  # Deve mostrar llama3.2:3b
```

### Índice FAISS não encontrado

```bash
python3 ingest.py
```

### Respostas lentas

- **Normal!** Modelo local 3B demora 10-15 segundos
- Primeira execução é mais lenta (carrega o modelo)
- Respostas subsequentes são mais rápidas

### Warning sobre PyTorch

```
None of PyTorch, TensorFlow >= 2.0, or Flax have been found.
```

**Pode ignorar!** O sistema usa TF-IDF e não precisa de PyTorch.

## ✅ Testes e Validação

Para instruções completas de teste e validação do sistema, consulte o **[Guia Completo de Testes](GUIA_TESTES.md)**.

### Testes Rápidos

```bash
# Demonstração automática
python simple_agent.py --demo

# Testes automatizados
pytest -v

# Interface web
uvicorn src.web.app:app --reload
# Acesse: http://localhost:8000
```

Os testes cobrem a lógica de roteamento dos agentes e o endpoint FastAPI da interface web, garantindo a estabilidade do fluxo principal.

## 📊 Comparação com APIs Pagas

| Aspecto | Ollama Local | OpenAI API |
|---------|-------------|------------|
| Custo | $0 | ~$0.001/resp |
| Velocidade | 10-15s | 1-2s |
| Qualidade | Boa | Excelente |
| Privacidade | 100% | Compartilhado |

## 🎓 Tecnologias

- **LangChain**: Framework para LLMs
- **Ollama**: Runtime para LLMs locais
- **FAISS**: Vector database (Facebook AI)
- **TF-IDF**: Embeddings (scikit-learn)
- **Llama 3.2**: LLM da Meta (3B parâmetros)

## 📄 Licença

MIT
