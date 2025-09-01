#!/usr/bin/env python3
"""
Script para coleta específica da Série B
Coleta apenas dados da Série B e salva na pasta dataset
"""

import sys
from datetime import datetime
from pathlib import Path

# Adiciona o diretório pai ao path para importar a biblioteca
sys.path.append(str(Path(__file__).parent.parent))

from src.brasileirao import Brasileirao

def coletar_serie_b():
    """Coleta dados apenas da Série B"""
    print("🔵 Coletando dados da Série B...")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Criar diretório com data atual
    hoje = datetime.now().strftime("%Y-%m-%d")
    dir_dados = Path(__file__).parent.parent / "dados_coletados" / hoje
    dir_dados.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Salvando dados em: {dir_dados}")
    
    with Brasileirao() as brasileirao:
        # Coletar Série B
        print("🔵 Coletando Série B...")
        dados_b = brasileirao.obter_dados_brasileirao_b(rodadas=True)
        
        if 'erro' not in dados_b:
            # Salvar dados completos
            arquivo_completo = dir_dados / "serie_b.json"
            brasileirao.salvar_json(dados_b, str(arquivo_completo))
            
            # Salvar apenas tabela
            dados_tabela = {'tabela': dados_b['tabela']}
            arquivo_tabela = dir_dados / "serie_b_tabela.json"
            brasileirao.salvar_json(dados_tabela, str(arquivo_tabela))
            
            # Salvar apenas rodadas
            if 'rodadas' in dados_b:
                dados_rodadas = {'rodadas': dados_b['rodadas']}
                arquivo_rodadas = dir_dados / "serie_b_rodadas.json"
                brasileirao.salvar_json(dados_rodadas, str(arquivo_rodadas))
            
            print(f"✅ Série B: {len(dados_b['tabela'])} times, {len(dados_b.get('rodadas', []))} rodadas")
            
            # Mostrar top 5 da tabela
            print("\n🏆 Top 5 da Série B:")
            for i, time in enumerate(dados_b['tabela'][:5], 1):
                print(f"  {i}º {time['nome']} - {time['pontos']} pts")
                
        else:
            print(f"❌ Erro Série B: {dados_b['erro']}")
            return False
    
    print(f"\n🎉 Coleta da Série B concluída! Dados salvos em: {dir_dados}")
    return True

if __name__ == "__main__":
    coletar_serie_b()
