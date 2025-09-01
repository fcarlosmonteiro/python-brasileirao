"""
Brasileirão Python - Módulo Principal
Contém as classes e funcionalidades principais da biblioteca
"""

from .brasileirao import Brasileirao, obter_dados_brasileirao_a, obter_dados_brasileirao_b
from .models import Time, Partida, Rodada, TabelaClassificacao, DadosBrasileirao
from .utils import JSONUtils, DataConverter, FormatUtils

__version__ = "2.0.0"
__author__ = "Brasileirão Python Team"

__all__ = [
    # Classe principal
    'Brasileirao',
    
    # Funções de conveniência
    'obter_dados_brasileirao_a',
    'obter_dados_brasileirao_b',
    
    # Modelos de dados
    'Time',
    'Partida', 
    'Rodada',
    'TabelaClassificacao',
    'DadosBrasileirao',
    
    # Utilitários
    'JSONUtils',
    'DataConverter',
    'FormatUtils'
]
