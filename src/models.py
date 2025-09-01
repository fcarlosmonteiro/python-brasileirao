"""
Modelos de dados e tipos para o projeto Brasileirão
"""

from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Time:
    """Modelo para dados de um time na tabela"""
    nome: str
    escudo: str
    posicao: str
    pontos: str
    jogos: str
    vitorias: str
    empates: str
    derrotas: str
    gols_pro: str
    gols_contra: str
    saldo_gols: str
    aproveitamento: str

@dataclass
class Partida:
    """Modelo para dados de uma partida"""
    partida: str
    data: str
    local: str
    time_casa: str
    time_fora: str
    gols_casa: str
    gols_fora: str
    resultado_texto: str

@dataclass
class Rodada:
    """Modelo para dados de uma rodada"""
    rodada: str
    inicio: str
    rodada_atual: bool
    partidas: List[Partida]

@dataclass
class TabelaClassificacao:
    """Modelo para tabela de classificação"""
    times: List[Time]

@dataclass
class DadosBrasileirao:
    """Modelo para dados completos do Brasileirão"""
    tabela: TabelaClassificacao
    rodadas: Optional[List[Rodada]] = None

# Tipos para compatibilidade
TimeDict = Dict[str, str]
PartidaDict = Dict[str, str]
RodadaDict = Dict[str, Union[str, bool, List[PartidaDict]]]
TabelaDict = List[TimeDict]
DadosBrasileiraoDict = Dict[str, Union[TabelaDict, List[RodadaDict]]]
