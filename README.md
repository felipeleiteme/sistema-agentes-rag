# SAC Learning GEMS 💎

**Sistema de Aprendizado Modular com 7 Agentes Especializados**

Sistema revolucionário de 7 GEMs (agentes especializados) que transformam a curva de aprendizado através de **aprendizado interativo** guiado por inteligência artificial local.

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen.svg)
![Qwen](https://img.shields.io/badge/qwen-max-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Características Principais

- ✅ **1M Tokens Grátis** - Alibaba Cloud oferece 1 milhão de tokens gratuitos
- ✅ **7 GEMs Especializados** - Agentes independentes e autossuficientes
- ✅ **Interface Web Moderna** - Chat interativo com streaming em tempo real
- ✅ **Navegação Livre** - Explore qualquer GEM a qualquer momento
- ✅ **Progresso Visual** - Acompanhe sua jornada com indicadores claros
- ✅ **Qwen API** - Modelo de IA de última geração da Alibaba Cloud
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

### 1. Obtenha sua Chave API da Qwen

1. Acesse: https://modelstudio.console.alibabacloud.com/?tab=model#/api-key
2. Crie uma conta (se necessário)
3. Gere sua API Key
4. **Ganhe 1 milhão de tokens gratuitos!** 🎉

### 2. Clone e Configure

```bash
git clone https://github.com/felipeleiteme/sistema-agentes-rag.git
cd sistema-agentes-rag
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Copie o arquivo .env.example e configure sua chave
cp .env.example .env
# Edite o .env e adicione sua QWEN_API_KEY
```

### 3. Configure o .env

Edite o arquivo `.env` e adicione sua chave:

```bash
QWEN_API_KEY=sk-sua-chave-aqui
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-max
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
```

### 4. Execute a Interface Web

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
- **Exportação de Jornada**: Baixe todo o histórico em formato Markdown
- **Carregamento de Histórico**: A interface restaura automaticamente as conversas anteriores
- **Botão de Conclusão Rápida**: Finalize o GEM atual com um clique
- **Botão de Cópia**: Copie respostas para a área de transferência
- **Backup Automático**: Arquivo .backup criado durante reinicialização

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
│  GEMs  │              │  Qwen API  │
│  7     │◄─────────────┤ qwen-max   │
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
├── requirements.txt               # Dependências principais
├── requirements-dev.txt           # Dependências de desenvolvimento
├── requirements-extra.txt         # Dependências opcionais
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

Edite o arquivo `.env`:

```bash
# Modelos disponíveis: qwen-max, qwen-plus, qwen-turbo
LLM_MODEL=qwen-max           # Modelo mais poderoso
LLM_TEMPERATURE=0.7          # Criatividade (0.0-1.0)
LLM_MAX_TOKENS=2048          # Tamanho máximo da resposta
LLM_REQUEST_TIMEOUT=60.0     # Timeout em segundos
```

### Modelos Qwen Disponíveis

| Modelo | Descrição | Uso Recomendado |
|--------|-----------|-----------------|
| `qwen-max` | Mais poderoso | Tarefas complexas, análises profundas |
| `qwen-plus` | Balanceado | Uso geral, boa relação custo/performance |
| `qwen-turbo` | Mais rápido | Respostas rápidas, tarefas simples |

Para mudar o modelo, edite a variável `LLM_MODEL` no `.env`.

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

### GET /api/history
Retorna o histórico de conversas salvo para reconstruir o chat.

### GET /api/export
Exporta a jornada do usuário em formato Markdown.

## 🐛 Troubleshooting

### Erro de API Key

```
Error: API key not configured
```

**Solução:** Verifique se o arquivo `.env` existe e contém a chave:
```bash
cat .env
# Deve mostrar: QWEN_API_KEY=sk-...
```

### Erro de conexão com API

```
Error: Connection timeout
```

**Possíveis causas:**
1. Verifique sua conexão com internet
2. Confirme que está usando o endpoint correto (internacional vs China)
3. Verifique se a chave API está ativa no console

### Limite de tokens excedido

```
Error: Token limit exceeded
```

**Solução:**
- Você atingiu o limite de 1M tokens gratuitos
- Adicione créditos na sua conta Alibaba Cloud
- Ou reduza `LLM_MAX_TOKENS` no `.env`

### Porta 8000 em uso

```bash
# Usar outra porta
uvicorn src.web.app:app --reload --port 8001
```

### Respostas lentas

- Verifique sua conexão com internet
- Use modelo mais rápido: `qwen-turbo` no `.env`
- Reduza `LLM_MAX_TOKENS` para respostas mais curtas

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
| Primeira resposta | 2-4s |
| Respostas subsequentes | 1-3s |
| Streaming (primeira palavra) | ~200ms |
| Carregamento da interface | <100ms |
| Troca entre GEMs | <50ms |

**Nota:** Tempos podem variar dependendo da sua conexão com internet e do modelo escolhido.

## 🎓 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem base |
| **FastAPI** | Latest | Framework web |
| **LangChain** | Latest | Orquestração de LLM |
| **Qwen API** | Latest | API de IA da Alibaba Cloud |
| **Qwen Max** | Latest | Modelo de linguagem avançado |
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

- Alibaba Cloud pelo Qwen e 1M tokens gratuitos
- LangChain pelo framework
- FastAPI pela performance excepcional
- Comunidade open source

## 📧 Contato

Felipe Leite - [@felipeleiteme](https://github.com/felipeleiteme)

Link do Projeto: [https://github.com/felipeleiteme/sistema-agentes-rag](https://github.com/felipeleiteme/sistema-agentes-rag)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!

**Desenvolvido com ❤️ usando Qwen API da Alibaba Cloud**
