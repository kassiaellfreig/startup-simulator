#!/usr/bin/env python3
"""
Gerador de Tickets - "Chefe Robô"
Conversa com Ollama para criar demandas realistas de IA e Cibersegurança
"""

import requests
import json
import os
from datetime import datetime
import random

class TicketGenerator:
    def __init__(self, model="qwen2.5:1.5b"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.tickets_dir = "tickets"
        
        # Garante que a pasta existe
        os.makedirs(self.tickets_dir, exist_ok=True)
    
    def generate_ticket(self, domain="mixed"):
        """
        Gera um ticket baseado no domínio especificado
        
        Args:
            domain: "ai", "security", "ai_security" ou "mixed"
        """
        print(f"🤖 [IA] Gerando ticket de {domain}... (aguarde)")
        
        # Contextos diferentes para variar os tickets
        contexts = {
            "ai": [
                "startup de fintech",
                "plataforma de e-commerce",
                "sistema de saúde digital",
                "app de delivery"
            ],
            "security": [
                "empresa de SaaS B2B",
                "banco digital",
                "plataforma de educação online",
                "startup de IoT"
            ],
            "ai_security": [
                "chatbot corporativo com dados sensíveis",
                "sistema de triagem médica com IA",
                "plataforma de recrutamento automatizado",
                "assistente virtual bancário"
            ],
            "mixed": [
                "startup de fintech",
                "empresa de SaaS B2B",
                "banco digital",
                "plataforma de e-commerce",
                "sistema de saúde digital",
                "startup de IoT"
            ]
        }
        
        # Escolhe contexto aleatório
        if domain == "mixed":
            domain = random.choice(["ai", "security", "ai_security"])
        
        context = random.choice(contexts.get(domain, contexts["mixed"]))
        
        # Prompt estruturado para garantir JSON válido
        prompt = f"""Você é um gestor técnico atribuindo uma tarefa para um analista júnior.
Gere UM ticket de demanda no formato de MISSÃO REAL.

REGRAS OBRIGATÓRIAS:
1. Gere APENAS JSON válido, sem markdown, sem texto extra
2. Todos os campos devem ter conteúdo REAL (nada de "...", "exemplo", "x")
3. Conteúdo em PORTUGUÊS
4. Seja específico e técnico

ESTRUTURA OBRIGATÓRIA DO JSON:
{{
  "id": "TK" + 4 dígitos aleatórios,
  "titulo": "título específico de até 80 caracteres",
  "domain": "{domain}",
  "contexto_empresa": "{context}",
  "descricao": "2-3 frases descrevendo o que aconteceu com sintomas observáveis",
  "urgencia": "baixa" ou "media" ou "alta",
  "tarefa_analista": "descrição clara do que o analista deve fazer (2-3 frases)",
  "entregaveis_esperados": ["entregável 1 específico", "entregável 2 específico", "entregável 3 específico"],
  "data_schema": "csv" ou "json" ou "syslog" ou "api_logs",
  "anomalia_para_buscar": "descrição do padrão/anomalia que existe nos dados",
  "criterio_sucesso": "como saber que a tarefa foi completada com sucesso",
  "restricoes_negocio": ["restrição 1 real", "restrição 2 real"]
}}

EXEMPLO VÁLIDO:
{{
  "id": "TK4821",
  "titulo": "Detecção de brute force em API de login",
  "domain": "security",
  "contexto_empresa": "Banco digital",
  "descricao": "Pico de 500 requisições 401 em 2 minutos no endpoint /auth/login entre 02:00-02:15",
  "urgencia": "alta",
  "tarefa_analista": "Analise os logs de API e identifique os IPs responsáveis pelo ataque. Proponha regra de rate limiting.",
  "entregaveis_esperados": ["Lista de IPs suspeitos (CSV)", "Script de detecção (Python)", "Relatório de incidente (Markdown)"],
  "data_schema": "api_logs",
  "anomalia_para_buscar": "Múltiplas requisições 401 do mesmo IP em janela de 5 minutos",
  "criterio_sucesso": "Identificou ≥3 IPs com ≥10 tentativas falhas cada",
  "restricoes_negocio": ["Não bloquear IPs de parceiros conhecidos", "Implementação em até 4h"]
}}

Agora gere o ticket REAL para este contexto: {context}.
Seja específico. Não use placeholders."""

        try:
            # Chama Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3  # Mais baixo = mais consistente em JSON
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=600)
            response.raise_for_status()
            
            # Extrai a resposta
            data = response.json()
            texto_ia = data.get("response", "")
            
            print(f"📝 [Debug] Texto bruto recebido ({len(texto_ia)} chars)")
            
               # Limpeza robusta do texto
            texto_limpo = texto_ia.strip()
            
            # Remove markdown ```json ... ```
            if "```" in texto_limpo:
                partes = texto_limpo.split("```")
                for parte in partes:
                    if "{" in parte or '"id"' in parte:
                        texto_limpo = parte.strip()
                        break
            
            # Remove prefixos comuns
            for prefixo in ["json", "JSON", "Aqui está", "Here is", ":"]:
                if texto_limpo.startswith(prefixo):
                    texto_limpo = texto_limpo[len(prefixo):].strip()
            
            # CORREÇÃO CRÍTICA: Se começa com " mas não tem {, adiciona
            if texto_limpo.startswith('"') and not texto_limpo.startswith('{'):
                texto_limpo = "{" + texto_limpo
            
            # Encontra o primeiro { e o último }
            inicio = texto_limpo.find("{")
            fim = texto_limpo.rfind("}")
            
            if inicio != -1 and fim != -1 and fim > inicio:
                texto_limpo = texto_limpo[inicio:fim+1]
            else:
                # Se ainda não achou }, adiciona no final
                if inicio != -1 and not texto_limpo.endswith("}"):
                    texto_limpo = texto_limpo + "}"
                elif inicio == -1:
                    print("❌ Não encontrei JSON válido no texto")
                    print(f"Texto: {texto_limpo[:200]}...")
                    return None
            
            # Tenta parsear
            try:
                ticket = json.loads(texto_limpo)
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON inválido, tentando corrigir... Erro: {e}")
                # Tenta remover caracteres problemáticos
                texto_limpo = texto_limpo.replace("\n", " ").replace("\t", " ")
                texto_limpo = " ".join(texto_limpo.split())  # Remove espaços extras
                try:
                    ticket = json.loads(texto_limpo)
                except:
                    print("❌ Não consegui corrigir o JSON automaticamente")
                    return None
            
            # Validação mínima dos campos
            campos_obrigatorios = ["titulo", "domain", "descricao", "urgencia"]
            for campo in campos_obrigatorios:
                if campo not in ticket:
                    print(f"⚠️ Campo {campo} faltando, adicionando padrão")
                    ticket[campo] = "N/A" if campo != "urgencia" else "media"
            
            # Gera ID se não veio
            if "id" not in ticket or not ticket["id"].startswith("TK"):
                ticket["id"] = f"TK{random.randint(1000, 9999)}"
            
            # Adiciona metadados
            ticket["created_at"] = datetime.now().isoformat()
            ticket["status"] = "pending"
            
            # Salva em arquivo
            ticket_file = f"{self.tickets_dir}/{ticket['id']}.json"
            with open(ticket_file, 'w', encoding='utf-8') as f:
                json.dump(ticket, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Ticket {ticket['id']} gerado com sucesso!")
            print(f"📁 Salvo em: {ticket_file}")
            print(f"🎯 Domínio: {ticket.get('domain', 'N/A')}")
            print(f"🔥 Urgência: {ticket.get('urgencia', 'N/A')}")
            print(f"📋 Título: {ticket.get('titulo', 'N/A')[:60]}...")
            
            return ticket
            
        except requests.exceptions.Timeout:
            print("❌ Timeout: Ollama demorou muito. Verifique se está rodando.")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            print(f"Texto recebido: {texto_ia[:200]}...")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return None

# Teste rápido se rodado diretamente
if __name__ == "__main__":
    generator = TicketGenerator()
    ticket = generator.generate_ticket(domain="mixed")
    
    if ticket:
        print("\n" + "="*60)
        print("📋 TICKET COMPLETO:")
        print(json.dumps(ticket, indent=2, ensure_ascii=False))
