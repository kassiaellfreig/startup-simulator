# 🚀 Startup Simulator - Career Training Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Sobre o Projeto

Plataforma de simulação de demandas reais de **IA e Cibersegurança** para treino de analistas júnior. 
Gera tickets contextualizados com datasets sintéticos contendo anomalias controladas para prática de investigação.

### ✨ Funcionalidades

- 🤖 Geração de tickets via IA local (Ollama + Qwen 2.5)
- 📊 Criação automática de datasets (CSV, JSON, logs)
- 🎯 Cenários de IA, Security e intersecção dos dois
- 📁 Organização automática por ticket/dataset/portfolio
- 🔒 100% offline após setup inicial

## 🛠️ Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| Python 3.12 | Linguagem principal |
| Ollama | IA local |
| Qwen 2.5 1.5B | Modelo de linguagem |
| Pandas, NumPy | Geração de dados |
| Faker | Dados sintéticos realistas |

## 🚀 Instalação

### Pré-requisitos
- Python 3.12+
- Ollama instalado (https://ollama.ai)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/kassiaellfreig/startup-simulator.git
cd startup-simulator

# 2. Instale o modelo no Ollama
ollama pull qwen2.5:1.5b

# 3. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 4. Instale dependências
pip install -r requirements.txt

# 5. Rode o simulador
python run.py
