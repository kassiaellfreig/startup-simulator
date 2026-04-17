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
```
## 📁 Estrutura do Projeto

```text
startup-simulator/
├── core/
│   ├── generator.py      # Gera tickets via IA
│   └── data_factory.py   # Gera datasets sintéticos
├── tickets/              # Tickets gerados (não versionado)
├── datasets/             # Datasets gerados (não versionado)
├── portfolio/            # Suas soluções (não versionado)
├── run.py                # Script principal
└── README.md             # Esta documentação
```

## 🎯 Como Usar

1. Execute `python run.py`
2. Escolha o domínio da demanda:
   - `1` - IA/Machine Learning
   - `2` - Cibersegurança
   - `3` - IA + Segurança (Intersecção)
   - `4` - Aleatório (Mixed)
3. Aguarde a geração do ticket (~1-2 minutos)
4. Analise os arquivos gerados:
   - `tickets/TKXXXX.json` - Descrição da demanda
   - `datasets/TKXXXX_*.csv|json` - Dados para análise
5. Desenvolva sua solução na pasta `portfolio/`
6. Documente seu processo (Markdown, Jupyter, etc.)

### Exemplo de Ticket Gerado

```json
{
  "id": "TK5678",
  "titulo": "Detecção de brute force em API de login",
  "domain": "security",
  "contexto_empresa": "Banco digital",
  "descricao": "Pico de 500 requisições 401 em 2 minutos no endpoint /auth/login",
  "urgencia": "alta",
  "tarefa_analista": "Analise os logs e identifique os IPs responsáveis...",
  "entregaveis_esperados": [
    "Lista de IPs suspeitos (CSV)",
    "Script de detecção (Python)",
    "Relatório de incidente (Markdown)"
  ],
  "data_schema": "api_logs",
  "anomalia_para_buscar": "Múltiplas requisições 401 do mesmo IP em janela de 5 minutos",
  "criterio_sucesso": "Identificou ≥3 IPs com ≥10 tentativas falhas cada"
}
```
## 📊 Exemplos de Casos de Uso

| Cenário | Habilidade Praticada |
|---------|---------------------|
| Detecção de brute force em API | Análise de logs, Python, regras de rate limiting |
| Viés de gênero em modelo de crédito | Pandas, estatística, fairness em ML |
| Session hijacking em sistema web | Forense digital, correlação de timestamps |
| Data drift em pipeline de ML | Monitoramento de modelos, alertas proativos |

## 🤝 Contribuindo

Este é um projeto de portfólio pessoal. Sugestões de melhoria são bem-vindas via Issues!

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.

## 👤 Autora

**Kássia Guedes** - Analista de IA/Security em formação  
🔗 [LinkedIn](https://www.linkedin.com/in/k%C3%A1ssia-e-f-098789129/) | 🐙 [GitHub](https://github.com/kassiaellfreig)
