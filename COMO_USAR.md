# 🚀 Como Usar o Sistema de Agentes

## Início Rápido

### 1. Ativar Ambiente Virtual
```bash
cd meu_sistema_agentes
source .venv/bin/activate
```

### 2. Executar o Sistema

#### Modo Interativo (Recomendado)
```bash
python simple_agent.py
```
Digite suas perguntas e receba respostas em tempo real. Digite `sair` para encerrar.

#### Modo Demonstração
```bash
python simple_agent.py --demo
```
Executa 3 perguntas pré-definidas para demonstrar o sistema.

#### Pergunta Única
```bash
python simple_agent.py -q "Quantos dias de férias tem um funcionário CLT?"
```

## 📋 Exemplos de Perguntas

### Perguntas sobre RH (usa RAG):
- "Quantos dias de férias CLT?"
- "Quais são os benefícios da empresa?"
- "Qual o valor do vale refeição?"
- "Como funciona o plano de saúde?"

### Perguntas Gerais (sem RAG):
- "Qual a capital do Brasil?"
- "Como está o tempo?"
- "Me explique o que é Python"

## ⚙️ Configurações Otimizadas

O sistema foi configurado para respostas **rápidas** (3-10 segundos):
- ✅ Timeout de 20 segundos
- ✅ Respostas limitadas a 150 tokens
- ✅ Contexto reduzido a 500 caracteres
- ✅ Temperature 0.5 (mais objetivo)

## 🔧 Solução de Problemas

### Sistema travando?
1. Verifique se o Ollama está rodando:
```bash
ollama list
```

2. Se não estiver, inicie:
```bash
ollama serve
```

3. Em caso de erros, reinicie o Ollama:
```bash
pkill ollama
ollama serve
```

### Respostas lentas?
- O primeiro uso pode ser mais lento (carrega o modelo)
- Perguntas subsequentes são mais rápidas
- Limite suas perguntas a tópicos específicos

## 📁 Arquivos Importantes

- `simple_agent.py` - Sistema principal
- `tools.py` - Ferramenta RAG
- `docs/politica_rh.txt` - Base de conhecimento
- `faiss_index/` - Índice vetorial

## 🆘 Ajuda

Se encontrar problemas, verifique:
1. ✅ Ambiente virtual ativado
2. ✅ Ollama rodando
3. ✅ Modelo llama3.2:3b instalado
4. ✅ Índice FAISS criado
