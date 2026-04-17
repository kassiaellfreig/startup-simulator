#!/usr/bin/env python3
"""
Fábrica de Dados - Gera datasets sintéticos realistas
Cria CSV, JSON ou logs baseados no tipo de anomalia solicitada
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random
from faker import Faker

class DataFactory:
    def __init__(self):
        self.datasets_dir = "datasets"
        os.makedirs(self.datasets_dir, exist_ok=True)
        self.fake = Faker('pt_BR')
    
    def create_dataset(self, ticket):
        """
        Cria dataset baseado no ticket - AGORA COM CONTEXTO
        
        Args:
            ticket: dicionário com informações do ticket
            
        Returns:
            str: caminho do arquivo gerado
        """
        ticket_id = ticket.get('id', 'TK0000')
        schema_type = ticket.get('data_schema', 'csv')
        anomaly_type = ticket.get('anomalia_para_buscar', 'generic')
        domain = ticket.get('domain', 'security')
        contexto = ticket.get('contexto_empresa', 'empresa')
        
        print(f"🏭 [Fábrica] Criando dataset para {ticket_id}...")
        print(f"   📌 Domínio: {domain}")
        print(f"   🏢 Contexto: {contexto}")
        print(f"   🔍 Anomalia: {anomaly_type}")
        
        # Decide o tipo de dado baseado no domínio + schema
        if domain == 'security' or 'api' in schema_type or 'log' in schema_type:
            filepath = self._create_api_logs_dataset(ticket_id, anomaly_type, contexto)
        elif domain == 'ai' and schema_type == 'csv':
            filepath = self._create_csv_dataset(ticket_id, anomaly_type, contexto, domain)
        elif schema_type == 'json':
            filepath = self._create_json_dataset(ticket_id, anomaly_type, contexto)
        elif schema_type == 'syslog':
            filepath = self._create_syslog_dataset(ticket_id, anomaly_type, contexto)
        else:
            # Fallback para CSV com contexto
            filepath = self._create_csv_dataset(ticket_id, anomaly_type, contexto, domain)
        
        print(f"✅ Dataset salvo em: {filepath}")
        return filepath
    
    def _create_csv_dataset(self, ticket_id, anomaly_type, contexto="empresa", domain="security"):
        """Cria CSV com dados contextualizados"""
        n_rows = random.randint(5000, 10000)
        
        # Escolhe colunas baseadas no domínio
        if domain == 'ai' or 'hospital' in contexto.lower() or 'médico' in contexto.lower():
            # Dados médicos/IA
            data = {
                'patient_id': [f"PCT{i:05d}" for i in range(1, n_rows + 1)],
                'idade': np.random.normal(45, 18, n_rows).astype(int),
                'genero': np.random.choice(['M', 'F', 'O'], n_rows, p=[0.48, 0.48, 0.04]),
                'tipo_consulta': np.random.choice(['triagem', 'emergencia', 'rotina', 'especialista'], n_rows),
                'tempo_espera_min': np.random.exponential(30, n_rows).astype(int),
                'resultado': np.random.choice(['normal', 'alerta', 'critico'], n_rows, p=[0.7, 0.2, 0.1]),
                'medico_id': [f"DOC{random.randint(1,50):03d}" for _ in range(n_rows)],
                'timestamp': pd.date_range(start='2026-04-01', periods=n_rows, freq='5min')
            }
            df = pd.DataFrame(data)
            
            # Injeção de anomalias médicas
            if 'duplicado' in anomaly_type.lower() or 'registro' in anomaly_type.lower():
                dup_indices = random.sample(range(len(df)), int(n_rows * 0.02))
                for idx in dup_indices:
                    dup_row = df.iloc[idx].copy()
                    dup_row['timestamp'] = dup_row['timestamp'] + pd.Timedelta(seconds=random.randint(1, 59))
                    df = pd.concat([df, pd.DataFrame([dup_row])], ignore_index=True)
            
            elif 'viés' in anomaly_type.lower() or 'bias' in anomaly_type.lower():
                mask_f = df['genero'] == 'F'
                df.loc[mask_f, 'resultado'] = np.random.choice(['normal', 'alerta', 'critico'], 
                                                               mask_f.sum(), p=[0.5, 0.3, 0.2])
            
            filepath = f"{self.datasets_dir}/{ticket_id}_patient_records.csv"
            
        else:
            # Dados financeiros (padrão original)
            data = {
                'id': range(1, n_rows + 1),
                'idade': np.random.normal(35, 12, n_rows).astype(int),
                'renda_mensal': np.random.lognormal(8, 0.8, n_rows).astype(int),
                'score_credito': np.random.randint(300, 850, n_rows),
                'historico_pagamento': np.random.choice(['limpo', 'inadimplente', 'atraso_ocasional'], n_rows),
                'genero': np.random.choice(['M', 'F', 'O'], n_rows, p=[0.48, 0.48, 0.04]),
                'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], n_rows),
                'aprovado': np.random.choice([0, 1], n_rows, p=[0.4, 0.6])
            }
            df = pd.DataFrame(data)
            
            # Injeção de anomalias financeiras
            if 'viés' in anomaly_type.lower() or 'bias' in anomaly_type.lower():
                mask_f = df['genero'] == 'F'
                df.loc[mask_f, 'score_credito'] -= np.random.randint(40, 80, mask_f.sum())
                df.loc[mask_f, 'aprovado'] = (df.loc[mask_f, 'score_credito'] > 650).astype(int)
            
            filepath = f"{self.datasets_dir}/{ticket_id}_financial_data.csv"
        
        # Limpeza de valores impossíveis
        if 'idade' in df.columns:
            df['idade'] = df['idade'].clip(18, 100)
        
        df.to_csv(filepath, index=False, encoding='utf-8')
        return filepath
    
    def _create_json_dataset(self, ticket_id, anomaly_type, contexto="empresa"):
        """Cria JSON (para APIs, logs de aplicação)"""
        n_records = random.randint(1000, 3000)
        
        records = []
        for i in range(n_records):
            record = {
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
                'user_id': f"USR{random.randint(10000, 99999)}",
                'action': random.choice(['login', 'view', 'purchase', 'logout', 'search']),
                'ip_address': self.fake.ipv4(),
                'user_agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)',
                    'python-requests/2.28.0'
                ]),
                'status_code': random.choice([200, 200, 200, 201, 400, 401, 403, 404, 500])
            }
            records.append(record)
        
        # Injeção de anomalias
        if 'injection' in anomaly_type.lower() or 'ataque' in anomaly_type.lower():
            for i in range(int(n_records * 0.05)):
                records[i]['action'] = random.choice([
                    "'; DROP TABLE users; --",
                    "<script>alert('xss')</script>",
                    "../../../etc/passwd",
                    "admin' OR '1'='1"
                ])
        
        filepath = f"{self.datasets_dir}/{ticket_id}_data.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def _create_syslog_dataset(self, ticket_id, anomaly_type, contexto="empresa"):
        """Cria logs de sistema (auth.log, syslog)"""
        n_lines = random.randint(2000, 5000)
        
        log_lines = []
        base_time = datetime.now() - timedelta(hours=24)
        
        for i in range(n_lines):
            timestamp = base_time + timedelta(seconds=random.randint(0, 86400))
            hostname = random.choice(['web01', 'db01', 'app01', 'firewall'])
            
            log_entry = f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sshd[{random.randint(1000, 9999)}]: {random.choice(['Accepted', 'Failed'])} password for {self.fake.user_name()} from {self.fake.ipv4()} port {random.randint(1024, 65535)} ssh2"
            
            log_lines.append(log_entry)
        
        # Injeção de ataque de força bruta
        if 'brute' in anomaly_type.lower() or 'força bruta' in anomaly_type.lower():
            attacker_ip = self.fake.ipv4()
            for i in range(100):
                timestamp = base_time + timedelta(hours=2, seconds=i*2)
                log_entry = f"{timestamp.strftime('%b %d %H:%M:%S')} web01 sshd[12345]: Failed password for root from {attacker_ip} port {random.randint(1024, 65535)} ssh2"
                log_lines.append(log_entry)
        
        filepath = f"{self.datasets_dir}/{ticket_id}_syslog.log"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_lines))
        
        return filepath
    
    def _create_api_logs_dataset(self, ticket_id, anomaly_type, contexto="empresa"):
        """Cria logs de API (JSON) - igual ao arquivo que você mostrou"""
        n_requests = random.randint(3000, 8000)
        
        logs = []
        endpoints = ['/api/v1/users', '/api/v1/products', '/api/v1/orders', 
                     '/api/v1/auth/login', '/api/v1/search', '/api/v1/data']
        actions = ['login', 'logout', 'view', 'search', 'purchase']
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)',
            'python-requests/2.28.0'
        ]
        
        base_time = datetime.now() - timedelta(hours=48)
        
        for i in range(n_requests):
            log_entry = {
                'timestamp': (base_time + timedelta(minutes=random.randint(0, 2880))).isoformat(),
                'user_id': f"USR{random.randint(10000, 99999)}",
                'action': random.choice(actions),
                'ip_address': self.fake.ipv4(),
                'user_agent': random.choice(user_agents),
                'status_code': random.choice([200, 200, 200, 201, 400, 401, 403, 404, 500])
            }
            logs.append(log_entry)
        
        # Injeção de anomalias de segurança
        if 'brute' in anomaly_type.lower() or 'força bruta' in anomaly_type.lower():
            attacker_ip = self.fake.ipv4()
            for i in range(100):
                logs.append({
                    'timestamp': (base_time + timedelta(hours=2, seconds=i*2)).isoformat(),
                    'user_id': f"USR{random.randint(10000, 99999)}",
                    'action': 'login',
                    'ip_address': attacker_ip,
                    'user_agent': 'python-requests/2.28.0',
                    'status_code': 401
                })
        
        elif 'hijack' in anomaly_type.lower() or 'session' in anomaly_type.lower():
            victim_user = f"USR{random.randint(10000, 99999)}"
            base_timestamp = (base_time + timedelta(hours=5)).isoformat()
            for i in range(10):
                logs.append({
                    'timestamp': base_timestamp,
                    'user_id': victim_user,
                    'action': 'view',
                    'ip_address': self.fake.ipv4(),
                    'user_agent': random.choice(user_agents),
                    'status_code': 200
                })
        
        filepath = f"{self.datasets_dir}/{ticket_id}_api_logs.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        return filepath

# Teste rápido
if __name__ == "__main__":
    test_ticket = {
        'id': 'TK9999',
        'domain': 'security',
        'data_schema': 'api_logs',
        'anomalia_para_buscar': 'session hijacking'
    }
    
    factory = DataFactory()
    factory.create_dataset(test_ticket)
