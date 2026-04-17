#!/usr/bin/env python3
"""
Startup Simulator - Orquestrador Principal
Gera tickets + datasets + prepara ambiente para resolução
"""

import sys
import os
import json
from datetime import datetime

# Adiciona o diretório core ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from generator import TicketGenerator
from data_factory import DataFactory

def main():
    print("="*70)
    print("🚀 STARTUP SIMULATOR - Career Training Platform")
    print("="*70)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"💼 Modo: Simulação de Empresa Real")
    print("="*70)
    
    # Inicializa componentes
    generator = TicketGenerator()
    factory = DataFactory()
    
    print("\n📋 Escolha o tipo de demanda:")
    print("  1. IA/Machine Learning")
    print("  2. Cibersegurança")
    print("  3. IA + Segurança (Intersecção)")
    print("  4. Aleatório (Mixed)")
    
    choice = input("\nDigite o número (1-4): ").strip()
    
    domain_map = {
        '1': 'ai',
        '2': 'security',
        '3': 'ai_security',
        '4': 'mixed'
    }
    
    domain = domain_map.get(choice, 'mixed')
    
    print(f"\n🎯 Domínio selecionado: {domain.upper()}")
    print("-"*70)
    
    # Gera ticket
    print("\n[1/3] Gerando ticket...")
    ticket = generator.generate_ticket(domain=domain)
    
    if not ticket:
        print("❌ Falha ao gerar ticket. Verifique se Ollama está rodando.")
        return
    
    # Gera dataset
    print("\n[2/3] Gerando dataset correspondente...")
    dataset_path = factory.create_dataset(ticket)
    
    # Resumo final
    print("\n[3/3] Resumo da demanda:")
    print("-"*70)
    print(f"🎫 Ticket ID: {ticket.get('id')}")
    print(f"📂 Ticket: tickets/{ticket.get('id')}.json")
    print(f"📊 Dataset: {dataset_path}")
    print(f"🏢 Contexto: {ticket.get('contexto_empresa', 'N/A')}")
    print(f"🔥 Urgência: {ticket.get('urgencia', 'N/A').upper()}")
    print(f"📋 Título: {ticket.get('titulo', 'N/A')}")
    
    print(f"\n📝 Descrição:")
    print(f"   {ticket.get('descricao', 'N/A')}")
    
    # ✅ NOVO: Mostrar tarefa do analista
    print(f"\n👤 Tarefa do Analista:")
    print(f"   {ticket.get('tarefa_analista', 'N/A')}")
    
    print(f"\n🎯 Entregáveis esperados:")
    for i, entregavel in enumerate(ticket.get('entregaveis_esperados', []), 1):
        print(f"   {i}. {entregavel}")
    
    print(f"\n🔍 Anomalia para buscar:")
    print(f"   {ticket.get('anomalia_para_buscar', 'N/A')}")
    
    print(f"\n✅ Critério de sucesso:")
    print(f"   {ticket.get('criterio_sucesso', 'N/A')}")
    
    print(f"\n⚠️ Restrições:")
    for restricao in ticket.get('restricoes_negocio', []):
        print(f"   • {restricao}")
    
    print("\n" + "="*70)
    print("✅ Demanda pronta! Agora é com você:")
    print("   1. Acesse o ticket em: tickets/")
    print("   2. Analise o dataset em: datasets/")
    print("   3. Resolva o problema e salve em: portfolio/")
    print("   4. Documente no GitHub!")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
