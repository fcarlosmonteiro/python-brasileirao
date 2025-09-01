#!/usr/bin/env python3
"""
Script para coleta de dados do Brasileirão
Coleta dados das Séries A e B e salva na pasta dataset
"""

import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.brasileirao import Brasileirao

def coletar_dados():
    """Coleta dados das duas séries e salva na pasta dataset"""
    print("⚽ Iniciando coleta de dados do Brasileirão...")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    dir_dados = Path(__file__).parent.parent / "dados_coletados" / hoje
    dir_dados.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Salvando dados em: {dir_dados}")
    
    with Brasileirao() as brasileirao:
        # Coletar Série A
        print("🔴 Coletando Série A...")
        dados_a = brasileirao.obter_dados_brasileirao_a(rodadas=True)
        
        if 'erro' not in dados_a:
            arquivo_a = dir_dados / "serie_a.json"
            brasileirao.salvar_json(dados_a, str(arquivo_a))
            print(f"✅ Série A: {len(dados_a['tabela'])} times, {len(dados_a.get('rodadas', []))} rodadas")
        else:
            print(f"❌ Erro Série A: {dados_a['erro']}")
        
        # Coletar Série B
        print("🔵 Coletando Série B...")
        dados_b = brasileirao.obter_dados_brasileirao_b(rodadas=True)
        
        if 'erro' not in dados_b:
            arquivo_b = dir_dados / "serie_b.json"
            brasileirao.salvar_json(dados_b, str(arquivo_b))
            print(f"✅ Série B: {len(dados_b['tabela'])} times, {len(dados_b.get('rodadas', []))} rodadas")
        else:
            print(f"❌ Erro Série B: {dados_b['erro']}")
    
    print(f"\n🎉 Coleta concluída! Dados salvos em: {dir_dados}")

if __name__ == "__main__":
    coletar_dados()
