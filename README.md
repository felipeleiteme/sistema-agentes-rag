# SAC Learning GEMS 💎

**Sistema de Aprendizado Modular com 7 Agentes Especializados**

Sistema revolucionário de 7 GEMs (agentes especializados) que transformam a curva de aprendizado através de **aprendizado interativo** guiado por inteligência artificial local.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen.svg)
![Ollama](https://img.shields.io/badge/ollama-llama3.2:3b-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Características Principais

- ✅ **100% Gratuito** - Sem APIs pagas, totalmente local
- ✅ **7 GEMs Especializados** - Agentes independentes e autossuficientes
- ✅ **Interface Web Moderna** - Chat interativo com streaming em tempo real
- ✅ **Navegação Livre** - Explore qualquer GEM a qualquer momento
- ✅ **Progresso Visual** - Acompanhe sua jornada com indicadores claros
- ✅ **LLM Local** - Llama 3.2 (3B) via Ollama, privacidade total
- ✅ **Performance Otimizada** - Respostas rápidas com streaming SSE

## 🎯 O que são os GEMs?

Os 7 GEMs são agentes especializados que trabalham em sequência para criar um sistema personalizado de aprendizado:

| # | GEM | Função | Duração |
|---|-----|--------|---------|
| 1️⃣ | 🗺️ **Mestre do Mapeamento** | Mapeia seus papéis de vida (M.A.P.A.) | 45 min |
| 2️⃣ | 🔍 **Diagnosticador F.O.C.O.** | Clarifica problemas (Fatos, Emoções, Contexto) | 20-40 min |
| 3️⃣ | ⚖️ **Validador Estratégico** | Valida investimento de energia | 30 min |
| 4️⃣ | 🔬 **Laboratório Científico** | Encontra métodos científicos validados | 30-45 min |
| 5️⃣ | 🎓 **Tutor Socrático** | Certifica domínio ativo | 60 min |
| 6️⃣ | 🏗️ **Arquiteto de Implementação** | Cria plano de implementação | 40 min |
| 7️⃣ | 💎 **Construtor de Sistemas** | Constrói assistente IA personalizado (KBF) | 30 min |

**Tempo total estimado:** 4-6 horas (distribuídas em vários dias)

**Resultado final:** Um KBF (Knowledge-Based Fractal) - assistente IA que te conhece profundamente e adapta cada sugestão à sua realidade única.

## 🚀 Instalação Rápida

### 1. Pré-requisitos

```bash
# macOS
brew install ollama
brew services start ollama
ollama pull llama3.2:3b

# Linux
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
```

### 2. Clone e Configure

```bash
git clone https://github.com/felipeleiteme/sistema-agentes-rag.git
cd sistema-agentes-rag
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Execute a Interface Web

```bash
uvicorn src.web.app:app --reload
```

Acesse **`http://localhost:8000`** no navegador.

## 📱 Interface Web

A interface web oferece uma experiência moderna e intuitiva:

### ✨ Principais Features

- **Streaming em Tempo Real**: Veja as respostas aparecerem palavra por palavra
- **Sidebar de Navegação**: Acesse qualquer GEM diretamente
- **Progresso Visual**: Barra de progresso e indicadores de conclusão
- **Design Responsivo**: Funciona perfeitamente em mobile e desktop
- **Tema Claro/Escuro**: Alterne entre temas com um clique
- **Histórico Persistente**: Suas conversas são salvas localmente

### 🎨 Componentes da Interface

```
┌─────────────────────────────────────────────┐
│  [☰]  SAC Learning GEMS              [🌙]  │
├──────────┬──────────────────────────────────┤
│          │                                  │
│  GEMs    │     Chat Principal              │
│  ─────   │     ─────────────               │
│          │                                  │
│  ✓ GEM 1 │  [Streaming de Mensagens]       │
│  → GEM 2 │  [Respostas em Tempo Real]      │
│    GEM 3 │  [Histórico Completo]           │
│    ...   │                                  │
│          │                                  │
│  ───────  │  ─────────────────────────────  │
│  42%     │  [Digite sua mensagem...]  [↑]  │
│  GEM 3/7 │                                  │
└──────────┴──────────────────────────────────┘
```

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────┐
│           Interface Web (FastAPI)           │
│  - Streaming SSE                            │
│  - Navegação entre GEMs                     │
│  - Gerenciamento de estado                  │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────▼─────────┐
        │   GEMService      │
        │   - Processa msgs │
        │   - Gerencia LLM  │
        └─────────┬─────────┘
                  │
        ┌─────────▼──────────┐
        │  GEMOrchestrator   │
        │  - Controla fluxo  │
        │  - Persiste estado │
        └─────────┬──────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
┌───▼────┐              ┌───────▼────┐
│  GEMs  │              │ Ollama LLM │
│  7     │◄─────────────┤ llama3.2:3b│
└────────┘              └────────────┘
```

## 📂 Estrutura do Projeto

```
sistema-agentes-rag/
├── src/
│   ├── agents/
│   │   ├── gems.py              # Definições dos 7 GEMs
│   │   ├── orchestrator.py      # Orquestrador da jornada
│   │   ├── gems_service.py      # Serviço principal dos GEMs
│   │   └── __init__.py
│   └── web/
│       ├── app.py               # FastAPI app com endpoints
│       ├── static/
│       │   ├── app.js           # JavaScript (streaming, sidebar)
│       │   └── styles.css       # Estilos modernos
│       └── templates/
│           ├── base.html
│           └── index.html       # Interface principal
├── docs/
│   ├── SAC_GEMS_README.md       # Documentação completa dos GEMs
│   ├── COMECE_AQUI.md           # Guia de início rápido
│   ├── GUIA_RAPIDO_GEMS.md      # Resumo dos GEMs
│   ├── MUDANCAS_v2.md           # Changelog da versão 2.0
│   ├── OTIMIZACAO_PERFORMANCE.md # Otimizações implementadas
│   └── CHANGELOG.md             # Histórico de mudanças
├── data/
│   └── sac_gems_knowledge.txt   # Base de conhecimento
├── sac_gems.py                  # CLI interativo
├── requirements.txt
└── README.md                    # Este arquivo
```

## 🎮 Como Usar

### 1. Interface Web (Recomendado)

```bash
uvicorn src.web.app:app --reload
```

Abra `http://localhost:8000` e:
1. Clique em **"Começar Jornada"**
2. Interaja com o GEM atual
3. Use a **sidebar** para navegar entre GEMs
4. Acompanhe seu **progresso visual**

### 2. CLI Interativo

```bash
python3 sac_gems.py
```

Comandos disponíveis:
- `iniciar` - Começa a jornada pelos GEMs
- `status` - Mostra seu progresso atual
- `listar` - Lista todos os GEMs disponíveis
- `reiniciar` - Recomeça do zero
- `sair` - Encerra o programa

## 🔧 Configuração Avançada

### Ajustar Parâmetros do LLM

Edite `src/agents/gems_service.py`:

```python
self.llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.4,      # Determinismo (0.0-1.0)
    num_predict=350,      # Tamanho da resposta
    num_ctx=1536,         # Tamanho do contexto
    num_thread=4          # Threads para CPU
)
```

### Mudar Modelo do Ollama

```bash
# Modelos disponíveis
ollama list

# Usar modelo diferente
ollama pull llama3.1:8b

# Atualizar no código
model="llama3.1:8b"
```

### Personalizar Streaming

Ajuste o delay em `src/web/app.py`:

```python
# Velocidade do streaming (segundos)
delay = 0.03 if i < 10 else 0.02
```

## 📊 Endpoints da API

### GET /api/gems
Lista todos os GEMs disponíveis e o GEM atual.

**Resposta:**
```json
{
  "gems": [...],
  "current_gem": "gem2_diagnosticador_foco"
}
```

### POST /api/chat
Envia uma mensagem (resposta completa).

**Request:**
```json
{
  "message": "Olá, quero começar"
}
```

### POST /api/chat/stream
Envia uma mensagem com streaming SSE.

**Stream Events:**
```javascript
data: {"type": "start"}
data: {"type": "chunk", "content": "palavra ", ...}
data: {"type": "done", "answer": "...", ...}
```

### POST /api/gems/{gem_id}/activate
Ativa um GEM específico para navegação livre.

### GET /api/status
Retorna o status atual da jornada.

### POST /api/reset
Reinicia a jornada do zero.

## 🐛 Troubleshooting

### Ollama não está rodando

```bash
# macOS
brew services start ollama

# Linux
sudo systemctl start ollama

# Verificar
ollama list
```

### Modelo não encontrado

```bash
ollama pull llama3.2:3b
```

### Porta 8000 em uso

```bash
# Usar outra porta
uvicorn src.web.app:app --reload --port 8001
```

### Respostas lentas

- **Normal para modelos locais!** (~10-15s)
- Primeira execução carrega o modelo (mais lento)
- Respostas subsequentes são mais rápidas
- Use modelo menor para mais velocidade: `llama3.2:1b`

### Warning sobre PyTorch

```
None of PyTorch, TensorFlow >= 2.0, or Flax have been found.
```

**Pode ignorar!** O sistema não usa PyTorch.

## 📈 Performance

### Otimizações Implementadas

- ✅ Streaming SSE para feedback imediato
- ✅ Contexto reduzido (1536 tokens) para processamento rápido
- ✅ Respostas concisas (350 tokens max)
- ✅ Cache de serviços com `@lru_cache`
- ✅ Compressão GZIP para respostas HTTP
- ✅ Delay adaptativo no streaming (mais rápido → mais lento)

### Benchmarks

| Operação | Tempo Médio |
|----------|-------------|
| Primeira resposta | 12-15s |
| Respostas subsequentes | 8-10s |
| Streaming (primeira palavra) | ~100ms |
| Carregamento da interface | <100ms |
| Troca entre GEMs | <50ms |

## 🎓 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem base |
| **FastAPI** | Latest | Framework web |
| **LangChain** | Latest | Orquestração de LLM |
| **Ollama** | Latest | Runtime LLM local |
| **Llama 3.2** | 3B | Modelo de linguagem |
| **JavaScript** | ES6+ | Frontend interativo |
| **CSS3** | - | Estilização moderna |

## 📚 Documentação Adicional

- **[SAC GEMS README](docs/SAC_GEMS_README.md)** - Documentação completa dos GEMs
- **[Comece Aqui](docs/COMECE_AQUI.md)** - Guia de início rápido
- **[Guia Rápido GEMS](docs/GUIA_RAPIDO_GEMS.md)** - Resumo dos 7 GEMs
- **[Mudanças v2.0](docs/MUDANCAS_v2.md)** - O que há de novo
- **[Otimização de Performance](docs/OTIMIZACAO_PERFORMANCE.md)** - Detalhes técnicos
- **[Changelog](docs/CHANGELOG.md)** - Histórico completo

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Roadmap

- [ ] Suporte para múltiplos usuários
- [ ] Integração com banco de dados
- [ ] Exportação de jornadas em PDF
- [ ] Modo offline completo
- [ ] App mobile (React Native)
- [ ] Suporte para mais modelos LLM
- [ ] Sistema de notificações

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Meta AI pelo Llama 3.2
- Ollama pela infraestrutura local
- LangChain pelo framework
- Comunidade open source

## 📧 Contato

Felipe Leite - [@felipeleiteme](https://github.com/felipeleiteme)

Link do Projeto: [https://github.com/felipeleiteme/sistema-agentes-rag](https://github.com/felipeleiteme/sistema-agentes-rag)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!

**Desenvolvido com ❤️ usando IA local**
