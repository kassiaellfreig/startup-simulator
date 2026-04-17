# 🚀 Startup Simulator - Career Training Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Linux](https://img.shields.io/badge/Linux-Mint-orange.svg)](https://linuxmint.com)

> 🎯 **Projeto desenvolvido no Linux Mint 21.x em máquina virtual dedicada**  
> Plataforma de simulação de demandas reais de **IA e Cibersegurança** para treino de analistas júnior. Gera tickets contextualizados com datasets sintéticos contendo anomalias controladas.

---

## 📋 Sobre o Projeto

Este projeto foi criado como parte de meu portfólio, ele simula o fluxo real de trabalho de um analista:

1. **Recebe um ticket de demanda** com contexto empresarial
2. **Analisa um dataset sintético** contendo anomalias embutidas
3. **Desenvolve uma solução técnica** (script, relatório, regra)
4. **Documenta o processo** para portfólio

### ✨ Funcionalidades Principais

- 🤖 **Geração de tickets via IA local** — Ollama + Qwen 2.5 (100% offline)
- 📊 **Criação automática de datasets** — CSV, JSON, logs com anomalias controladas
- 🎯 **Múltiplos cenários** — IA, Security e intersecção dos dois domínios
- 📁 **Organização automática** — Estrutura por ticket/dataset/portfolio
- 🔒 **Sem dependências externas** — Nenhuma API na nuvem após setup inicial

---

## ⚠️ Requisitos e Limitações

### 🔧 Hardware Recomendado

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| **RAM** | 4 GB | 8 GB+ |
| **Espaço em disco** | 10 GB | 20 GB+ |
| **CPU** | 2 núcleos | 4 núcleos+ |
| **GPU** | Não requerida | Opcional (acelera inferência) |

### 💾 Espaço do Modelo

- Modelo `qwen2.5:1.5b`: ~1.2 GB após download
- Cache do Ollama: ~500 MB
- **Total estimado para setup inicial**: ~2 GB

### ⏱️ Tempo de Geração

| Cenário | Tempo |
|---------|-------|
| Primeira execução (modelo frio) | 2-4 minutos |
| Execuções subsequentes (modelo quente) | 30-90 segundos |

> *Nota: Tempos variam conforme hardware da máquina*

### 🐧 Ambiente de Desenvolvimento

Este projeto foi **desenvolvido e testado em**:

- **SO**: Linux Mint Xfce
- **Ambiente**: VirtualBox VM com 4 GB RAM, 2 vCPUs
- **Python**: 3.12 via `venv`
- **Ollama**: Versão mais recente via instalador oficial

> ✅ Funciona em outras distribuições Linux (Ubuntu, Debian, Fedora)  
> ⚠️ **Windows/macOS**: Pode funcionar, mas não foi testado oficialmente

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| **Python 3.12** | Linguagem principal |
| **Ollama** | Execução local de modelos de linguagem |
| **Qwen 2.5 1.5B** | Modelo de IA para geração de tickets |
| **Pandas, NumPy** | Manipulação e geração de dados |
| **Faker** | Dados sintéticos realistas em português |
| **Requests** | Comunicação com API local do Ollama |

---

## 🚀 Instalação (Linux)

### 🔹 Pré-requisitos Obrigatórios

> ⚠️ **Importante**: Instale o Ollama e baixe o modelo **ANTES** de rodar o projeto!

```bash
# 1️⃣ Instale o Ollama (oficial para Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# 2️⃣ Inicie o serviço (se não iniciar automaticamente)
sudo systemctl start ollama
sudo systemctl enable ollama  # opcional: iniciar no boot

# 3️⃣ Baixe o modelo Qwen 2.5 1.5B (~1.2 GB)
ollama pull qwen2.5:1.5b

# 4️⃣ Verifique se está funcionando
ollama run qwen2.5:1.5b "Olá"
# → Deve responder. Pressione Ctrl+D para sair.
```

### 🔹 Instalando o Projeto

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/kassiaellfreig/startup-simulator.git
cd startup-simulator

# 2️⃣ Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Instale as dependências
pip install -r requirements.txt

# 4️⃣ (Opcional) Teste as dependências
python -c "import pandas, faker, requests; print('✅ Dependências OK')"
```

---

## ▶️ Como Usar

### Modo Básico

```bash
# Ative o ambiente (se ainda não estiver ativo)
source venv/bin/activate

# Rode o simulador
python run.py
```

### Fluxo de Uso Completo

```
🚀 STARTUP SIMULATOR - Career Training Platform
======================================================================
📋 Escolha o tipo de demanda:
  1. IA/Machine Learning
  2. Cibersegurança
  3. IA + Segurança (Intersecção)
  4. Aleatório (Mixed)

Digite o número (1-4): 2

🎯 Domínio selecionado: SECURITY
----------------------------------------------------------------------

[1/3] Gerando ticket...
🤖 [IA] Gerando ticket de security... (aguarde ~1-2 min)
✅ Ticket TK5678 gerado com sucesso!

[2/3] Gerando dataset correspondente...
✅ Dataset salvo em: datasets/TK5678_api_logs.json

[3/3] Resumo da demanda:
🎫 Ticket ID: TK5678
🏢 Contexto: Banco digital
🔥 Urgência: ALTA
📋 Título: Detecção de brute force em API de login
👤 Tarefa do Analista: Analise os logs e identifique os IPs...
🎯 Entregáveis: ["Lista de IPs", "Script Python", "Relatório"]
✅ Critério de sucesso: Identificou ≥3 IPs com ≥10 tentativas

======================================================================
✅ Demanda pronta! Agora é com você:
   1. Acesse o ticket em: tickets/TK5678.json
   2. Analise o dataset em: datasets/TK5678_api_logs.json
   3. Resolva e salve em: portfolio/
   4. Documente no GitHub!
```

### 🎁 Bônus: Alias para Facilitar o Uso

Para evitar digitar os mesmos comandos toda vez, adicione ao seu `~/.bashrc`:

```bash
# Adicione no final do ~/.bashrc
alias startup='cd ~/startup-simulator && source venv/bin/activate && ollama run qwen2.5:1.5b "Oi" > /dev/null 2>&1 && python run.py'

# Recarregue o bash
source ~/.bashrc

# Agora é só digitar:
startup
```

> ℹ️ Este alias: entra na pasta, ativa o venv, "esquenta" o modelo e roda o projeto — tudo em um comando!

---

## 📁 Estrutura do Projeto

```text
startup-simulator/
├── core/
│   ├── generator.py      # Gera tickets via IA (prompt engineering)
│   └── data_factory.py   # Gera datasets sintéticos com anomalias
├── tickets/              # Tickets gerados (.json) - NÃO versionado
├── datasets/             # Datasets gerados (.csv/.json) - NÃO versionado
├── portfolio/            # SUAS soluções - NÃO versionado (seu espaço!)
├── venv/                 # Ambiente virtual - NÃO versionado
├── run.py                # Entry point do projeto
├── requirements.txt      # Dependências Python
└── README.md             # Esta documentação
```

---

## 🧪 Exemplo de Ticket Gerado

```json
{
  "id": "TK5678",
  "titulo": "Detecção de brute force em API de login",
  "domain": "security",
  "contexto_empresa": "Banco digital",
  "descricao": "Pico de 500 requisições 401 em 2 minutos no endpoint /auth/login",
  "urgencia": "alta",
  "tarefa_analista": "Analise os logs e identifique os IPs responsáveis pelo ataque. Proponha regra de rate limiting.",
  "entregaveis_esperados": [
    "Lista de IPs suspeitos (CSV)",
    "Script de detecção (Python)",
    "Relatório de incidente (Markdown)"
  ],
  "data_schema": "api_logs",
  "anomalia_para_buscar": "Múltiplas requisições 401 do mesmo IP em janela de 5 minutos",
  "criterio_sucesso": "Identificou ≥3 IPs com ≥10 tentativas falhas cada",
  "restricoes_negocio": [
    "Não bloquear IPs de parceiros conhecidos",
    "Implementação em até 4h"
  ]
}
```

---

## 📊 Casos de Uso e Habilidades Praticadas

| Cenário | Habilidade Técnica | Ferramentas Envolvidas |
|---------|-------------------|----------------------|
| 🔐 Detecção de brute force em API | Análise de logs, Python, regras de rate limiting | Pandas, regex, JSON |
| ⚖️ Viés de gênero em modelo de crédito | Estatística, fairness em ML, análise exploratória | Pandas, NumPy, visualização |
| 🕵️ Session hijacking em sistema web | Forense digital, correlação de timestamps, investigação | Pandas, datetime, análise temporal |
| 📉 Data drift em pipeline de ML | Monitoramento de modelos, alertas proativos, estatística | Pandas, comparação de distribuições |

---

## 🛠️ Solução de Problemas Comuns

### ❌ "Timeout: Ollama demorou muito"

```bash
# 1. Verifique se o Ollama está rodando
sudo systemctl status ollama

# 2. Se não estiver, inicie:
sudo systemctl start ollama

# 3. Esquente o modelo manualmente antes de rodar:
ollama run qwen2.5:1.5b "Oi"
# → Ctrl+D para sair, depois rode python run.py

# 4. Se persistir, aumente o timeout em core/generator.py (linha ~75):
# timeout=600  # 10 minutos
```

### ❌ "ModuleNotFoundError: No module named 'pandas'"

```bash
# Ative o ambiente virtual antes de instalar/rodar:
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ "Permission denied" ao rodar ollama

```bash
# Adicione seu usuário ao grupo ollama (se necessário)
sudo usermod -a -G ollama $USER
# Faça logout/login para aplicar
```

### ❌ Modelo não responde / geração muito lenta

```bash
# Verifique uso de RAM:
free -h

# Se estiver com pouca RAM, feche outros programas ou aumente a RAM da VM

# Teste o modelo isoladamente:
ollama run qwen2.5:1.5b "Explique o que é um brute force em 1 frase"
```

---

## 🤝 Contribuindo

Este é um projeto de portfólio pessoal, mas **sugestões são bem-vindas**!

1. **Abra uma [Issue](https://github.com/kassiaellfreig/startup-simulator/issues)** descrevendo a sugestão ou bug
2. **Se quiser contribuir com código**:
   - Fork o repositório
   - Crie uma branch: `git checkout -b feature/minha-sugestao`
   - Commit: `git commit -m 'feat: adiciona X'`
   - Push: `git push origin feature/minha-sugestao`
   - Abra um Pull Request

> 💡 **Dica**: Mantenha o foco em melhorias que ajudem no **treino de analistas júnior** — clareza, realismo e didática são prioridades!

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.

---

## 👤 Autora

**Kássia Guedes** — Analista de IA/Security em formação

🔗 [LinkedIn](https://www.linkedin.com/in/k%C3%A1ssia-e-f-098789129/)  
🐙 [GitHub](https://github.com/kassiaellfreig)  

---

> ℹ️ **Nota sobre Privacidade**: Todos os dados gerados são sintéticos e fictícios. Nenhum dado real de usuários, empresas ou sistemas é utilizado ou armazenado por este projeto.
