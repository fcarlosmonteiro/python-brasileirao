#!/usr/bin/env python3
"""
Análise Visual do Clube do Remo usando Plotly
Gera gráficos interativos para análise de performance
"""

import sys
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path

# Adiciona o diretório pai ao path para importar a biblioteca
sys.path.append(str(Path(__file__).parent.parent))

def carregar_dados_remo():
    """Carrega dados específicos do Remo"""
    print("🦅 Carregando dados do Clube do Remo...")
    
    # Carregar dados da tabela
    with open('dados_coletados/2025-09-09/serie_b_tabela.json', 'r', encoding='utf-8') as f:
        tabela_data = json.load(f)
    
    # Carregar dados das rodadas
    with open('dados_coletados/2025-09-09/serie_b_rodadas.json', 'r', encoding='utf-8') as f:
        rodadas_data = json.load(f)
    
    # Encontrar dados do Remo na tabela
    remo_tabela = None
    for time in tabela_data['tabela']:
        if time['nome'] == 'Remo':
            remo_tabela = time
            break
    
    # Encontrar partidas do Remo
    partidas_remo = []
    for rodada in rodadas_data['rodadas']:
        for partida in rodada['partidas']:
            if 'Remo' in partida['partida']:
                partidas_remo.append({
                    'rodada': rodada['rodada'],
                    'data': partida['data'],
                    'partida': partida['partida'],
                    'local': partida['local'],
                    'time_casa': partida['time_casa'],
                    'time_fora': partida['time_fora'],
                    'gols_casa': partida['gols_casa'],
                    'gols_fora': partida['gols_fora'],
                    'resultado_texto': partida['resultado_texto']
                })
    
    return remo_tabela, partidas_remo

def criar_grafico_performance_geral(remo_tabela):
    """Cria gráfico de performance geral do Remo"""
    print("📊 Criando gráfico de performance geral...")
    
    # Dados para o gráfico de pizza
    labels = ['Vitórias', 'Empates', 'Derrotas']
    values = [int(remo_tabela['vitorias']), int(remo_tabela['empates']), int(remo_tabela['derrotas'])]
    colors = ['#10B981', '#F59E0B', '#EF4444']  # Verde, Amarelo, Vermelho
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent+value',
        textfont_size=14
    )])
    
    fig.update_layout(
        title={
            'text': f" Performance do Remo - {remo_tabela['jogos']} jogos",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1E3A8A'}
        },
        showlegend=True,
        font=dict(size=12),
        height=500
    )
    
    return fig

def criar_grafico_gols(partidas_remo):
    """Cria gráfico de gols pró e contra"""
    print("⚽ Criando gráfico de gols...")
    
    # Filtrar apenas jogos com resultado
    jogos_com_resultado = [p for p in partidas_remo if p['gols_casa'] != '' and p['gols_fora'] != '']
    
    gols_pro = []
    gols_contra = []
    rodadas = []
    
    for partida in jogos_com_resultado:
        if partida['time_casa'] == 'Remo':
            gols_pro.append(int(partida['gols_casa']))
            gols_contra.append(int(partida['gols_fora']))
        else:
            gols_pro.append(int(partida['gols_fora']))
            gols_contra.append(int(partida['gols_casa']))
        
        rodadas.append(partida['rodada'])
    
    fig = go.Figure()
    
    # Gols pró
    fig.add_trace(go.Scatter(
        x=rodadas,
        y=gols_pro,
        mode='lines+markers',
        name='Gols Pró',
        line=dict(color='#10B981', width=3),
        marker=dict(size=8)
    ))
    
    # Gols contra
    fig.add_trace(go.Scatter(
        x=rodadas,
        y=gols_contra,
        mode='lines+markers',
        name='Gols Contra',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title={
            'text': "⚽ Evolução dos Gols - Remo",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1E3A8A'}
        },
        xaxis_title="Rodadas",
        yaxis_title="Gols",
        font=dict(size=12),
        height=500,
        hovermode='x unified'
    )
    
    return fig

def criar_grafico_performance_adversarios(partidas_remo):
    """Cria gráfico de performance por adversário"""
    print("🎯 Criando gráfico de performance por adversário...")
    
    adversarios = {}
    
    for partida in partidas_remo:
        # Pular jogos sem resultado
        if partida['gols_casa'] == '' or partida['gols_fora'] == '':
            continue
            
        if partida['time_casa'] == 'Remo':
            adversario = partida['time_fora']
            gols_remo = int(partida['gols_casa'])
            gols_adversario = int(partida['gols_fora'])
        else:
            adversario = partida['time_casa']
            gols_remo = int(partida['gols_fora'])
            gols_adversario = int(partida['gols_casa'])
        
        if adversario not in adversarios:
            adversarios[adversario] = {
                'jogos': 0,
                'vitorias': 0,
                'empates': 0,
                'derrotas': 0,
                'gols_pro': 0,
                'gols_contra': 0
            }
        
        adversarios[adversario]['jogos'] += 1
        adversarios[adversario]['gols_pro'] += gols_remo
        adversarios[adversario]['gols_contra'] += gols_adversario
        
        if gols_remo > gols_adversario:
            adversarios[adversario]['vitorias'] += 1
        elif gols_remo == gols_adversario:
            adversarios[adversario]['empates'] += 1
        else:
            adversarios[adversario]['derrotas'] += 1
    
    # Preparar dados para o gráfico
    nomes_adversarios = []
    aproveitamentos = []
    cores = []
    
    for adversario, stats in adversarios.items():
        if stats['jogos'] > 0:
            aproveitamento = ((stats['vitorias'] * 3 + stats['empates']) / (stats['jogos'] * 3)) * 100
            nomes_adversarios.append(adversario)
            aproveitamentos.append(aproveitamento)
            
            # Definir cor baseada no aproveitamento
            if aproveitamento >= 70:
                cores.append('#10B981')  # Verde
            elif aproveitamento >= 40:
                cores.append('#F59E0B')  # Amarelo
            else:
                cores.append('#EF4444')  # Vermelho
    
    fig = go.Figure(data=[
        go.Bar(
            x=nomes_adversarios,
            y=aproveitamentos,
            marker_color=cores,
            text=[f"{ap:.1f}%" for ap in aproveitamentos],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title={
            'text': "🎯 Aproveitamento por Adversário - Remo",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1E3A8A'}
        },
        xaxis_title="Adversários",
        yaxis_title="Aproveitamento (%)",
        font=dict(size=12),
        height=600,
        xaxis_tickangle=-45
    )
    
    return fig

def criar_grafico_casa_fora(partidas_remo):
    """Cria gráfico comparando performance em casa vs fora"""
    print("🏠 Criando gráfico casa vs fora...")
    
    casa_stats = {'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}
    fora_stats = {'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}
    
    for partida in partidas_remo:
        # Pular jogos sem resultado
        if partida['gols_casa'] == '' or partida['gols_fora'] == '':
            continue
            
        if partida['time_casa'] == 'Remo':
            casa_stats['jogos'] += 1
            gols_remo = int(partida['gols_casa'])
            gols_adversario = int(partida['gols_fora'])
        else:
            fora_stats['jogos'] += 1
            gols_remo = int(partida['gols_fora'])
            gols_adversario = int(partida['gols_casa'])
        
        if gols_remo > gols_adversario:
            if partida['time_casa'] == 'Remo':
                casa_stats['vitorias'] += 1
            else:
                fora_stats['vitorias'] += 1
        elif gols_remo == gols_adversario:
            if partida['time_casa'] == 'Remo':
                casa_stats['empates'] += 1
            else:
                fora_stats['empates'] += 1
        else:
            if partida['time_casa'] == 'Remo':
                casa_stats['derrotas'] += 1
            else:
                fora_stats['derrotas'] += 1
    
    # Calcular aproveitamentos
    aproveitamento_casa = ((casa_stats['vitorias'] * 3 + casa_stats['empates']) / (casa_stats['jogos'] * 3)) * 100 if casa_stats['jogos'] > 0 else 0
    aproveitamento_fora = ((fora_stats['vitorias'] * 3 + fora_stats['empates']) / (fora_stats['jogos'] * 3)) * 100 if fora_stats['jogos'] > 0 else 0
    
    fig = go.Figure(data=[
        go.Bar(
            x=['Em Casa', 'Fora de Casa'],
            y=[aproveitamento_casa, aproveitamento_fora],
            marker_color=['#1E3A8A', '#3B82F6'],
            text=[f"{aproveitamento_casa:.1f}%", f"{aproveitamento_fora:.1f}%"],
            textposition='auto',
            textfont=dict(size=16, color='white')
        )
    ])
    
    fig.update_layout(
        title={
            'text': "🏠 Performance Casa vs Fora - Remo",
            'x': 0.5,
            'font': {'size': 20, 'color': '#1E3A8A'}
        },
        xaxis_title="Local",
        yaxis_title="Aproveitamento (%)",
        font=dict(size=12),
        height=500
    )
    
    return fig

def criar_dashboard_completo(remo_tabela, partidas_remo):
    """Cria dashboard completo com todos os gráficos"""
    print("📊 Criando dashboard completo...")
    
    # Criar subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Performance Geral",
            "Evolução dos Gols",
            "Performance por Adversário",
            "Casa vs Fora"
        ),
        specs=[[{"type": "pie"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Gráfico 1: Performance Geral (Pizza)
    labels = ['Vitórias', 'Empates', 'Derrotas']
    values = [int(remo_tabela['vitorias']), int(remo_tabela['empates']), int(remo_tabela['derrotas'])]
    colors = ['#10B981', '#F59E0B', '#EF4444']
    
    fig.add_trace(
        go.Pie(labels=labels, values=values, marker_colors=colors, hole=0.3),
        row=1, col=1
    )
    
    # Gráfico 2: Evolução dos Gols
    jogos_com_resultado = [p for p in partidas_remo if p['gols_casa'] != '' and p['gols_fora'] != '']
    gols_pro = []
    gols_contra = []
    rodadas = []
    
    for partida in jogos_com_resultado:
        if partida['time_casa'] == 'Remo':
            gols_pro.append(int(partida['gols_casa']))
            gols_contra.append(int(partida['gols_fora']))
        else:
            gols_pro.append(int(partida['gols_fora']))
            gols_contra.append(int(partida['gols_casa']))
        rodadas.append(partida['rodada'])
    
    fig.add_trace(
        go.Scatter(x=rodadas, y=gols_pro, mode='lines+markers', name='Gols Pró', line=dict(color='#10B981')),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=rodadas, y=gols_contra, mode='lines+markers', name='Gols Contra', line=dict(color='#EF4444')),
        row=1, col=2
    )
    
    # Gráfico 3: Performance por Adversário
    adversarios = {}
    for partida in partidas_remo:
        if partida['gols_casa'] == '' or partida['gols_fora'] == '':
            continue
            
        if partida['time_casa'] == 'Remo':
            adversario = partida['time_fora']
            gols_remo = int(partida['gols_casa'])
            gols_adversario = int(partida['gols_fora'])
        else:
            adversario = partida['time_casa']
            gols_remo = int(partida['gols_fora'])
            gols_adversario = int(partida['gols_casa'])
        
        if adversario not in adversarios:
            adversarios[adversario] = {'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}
        
        adversarios[adversario]['jogos'] += 1
        if gols_remo > gols_adversario:
            adversarios[adversario]['vitorias'] += 1
        elif gols_remo == gols_adversario:
            adversarios[adversario]['empates'] += 1
        else:
            adversarios[adversario]['derrotas'] += 1
    
    nomes_adversarios = []
    aproveitamentos = []
    for adversario, stats in adversarios.items():
        if stats['jogos'] > 0:
            aproveitamento = ((stats['vitorias'] * 3 + stats['empates']) / (stats['jogos'] * 3)) * 100
            nomes_adversarios.append(adversario)
            aproveitamentos.append(aproveitamento)
    
    fig.add_trace(
        go.Bar(x=nomes_adversarios, y=aproveitamentos, name='Aproveitamento'),
        row=2, col=1
    )
    
    # Gráfico 4: Casa vs Fora
    casa_stats = {'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}
    fora_stats = {'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}
    
    for partida in partidas_remo:
        if partida['gols_casa'] == '' or partida['gols_fora'] == '':
            continue
            
        if partida['time_casa'] == 'Remo':
            casa_stats['jogos'] += 1
            gols_remo = int(partida['gols_casa'])
            gols_adversario = int(partida['gols_fora'])
        else:
            fora_stats['jogos'] += 1
            gols_remo = int(partida['gols_fora'])
            gols_adversario = int(partida['gols_casa'])
        
        if gols_remo > gols_adversario:
            if partida['time_casa'] == 'Remo':
                casa_stats['vitorias'] += 1
            else:
                fora_stats['vitorias'] += 1
        elif gols_remo == gols_adversario:
            if partida['time_casa'] == 'Remo':
                casa_stats['empates'] += 1
            else:
                fora_stats['empates'] += 1
        else:
            if partida['time_casa'] == 'Remo':
                casa_stats['derrotas'] += 1
            else:
                fora_stats['derrotas'] += 1
    
    aproveitamento_casa = ((casa_stats['vitorias'] * 3 + casa_stats['empates']) / (casa_stats['jogos'] * 3)) * 100 if casa_stats['jogos'] > 0 else 0
    aproveitamento_fora = ((fora_stats['vitorias'] * 3 + fora_stats['empates']) / (fora_stats['jogos'] * 3)) * 100 if fora_stats['jogos'] > 0 else 0
    
    fig.add_trace(
        go.Bar(x=['Em Casa', 'Fora'], y=[aproveitamento_casa, aproveitamento_fora], name='Casa vs Fora'),
        row=2, col=2
    )
    
    fig.update_layout(
        title={
            'text': "Clube do Remo Analytics",
            'x': 0.5,
            'font': {'size': 24, 'color': '#1E3A8A'}
        },
        height=800,
        showlegend=False,
        font=dict(size=10)
    )
    
    return fig

def salvar_graficos(figuras, remo_tabela):
    """Salva os gráficos em arquivos HTML"""
    print("💾 Salvando gráficos...")
    
    # Criar diretório para os gráficos
    Path("graficos_remo").mkdir(exist_ok=True)
    
    # Salvar gráficos individuais
    figuras['performance_geral'].write_html("graficos_remo/performance_geral.html")
    figuras['gols'].write_html("graficos_remo/evolucao_gols.html")
    figuras['adversarios'].write_html("graficos_remo/performance_adversarios.html")
    figuras['casa_fora'].write_html("graficos_remo/casa_vs_fora.html")
    figuras['dashboard'].write_html("graficos_remo/dashboard_completo.html")
    
    print("✅ Gráficos salvos em:")
    print("   📊 graficos_remo/performance_geral.html")
    print("   ⚽ graficos_remo/evolucao_gols.html")
    print("   🎯 graficos_remo/performance_adversarios.html")
    print("   🏠 graficos_remo/casa_vs_fora.html")
    print("   📈 graficos_remo/dashboard_completo.html")

def main():
    """Função principal"""
    print("🦅 ANÁLISE VISUAL DO REMO - Plotly")
    print("=" * 50)
    print(f"📅 Análise realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Carregar dados
        remo_tabela, partidas_remo = carregar_dados_remo()
        
        if not remo_tabela:
            print("❌ Erro: Dados do Remo não encontrados!")
            return
        
        print(f"✅ Dados carregados: {len(partidas_remo)} partidas encontradas")
        
        # Criar gráficos
        figuras = {
            'performance_geral': criar_grafico_performance_geral(remo_tabela),
            'gols': criar_grafico_gols(partidas_remo),
            'adversarios': criar_grafico_performance_adversarios(partidas_remo),
            'casa_fora': criar_grafico_casa_fora(partidas_remo),
            'dashboard': criar_dashboard_completo(remo_tabela, partidas_remo)
        }
        
        # Salvar gráficos
        salvar_graficos(figuras, remo_tabela)
        
        print("\n🎉 Análise visual concluída com sucesso!")
        print("🌐 Abra os arquivos HTML no navegador para visualizar os gráficos interativos!")
        
    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")

if __name__ == "__main__":
    main()
