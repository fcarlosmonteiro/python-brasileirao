"""
Brasileirão Python - Scraper para dados do Brasileirão Série A e B
"""

from .src.brasileirao import Brasileirao, obter_dados_brasileirao_a, obter_dados_brasileirao_b
from .src.models import Time, Partida, Rodada, TabelaClassificacao, DadosBrasileirao
from .scrapers.http_client import HTTPClient
from .scrapers.parsers import TabelaParser, RodadasParser
from .src.utils import JSONUtils, DataConverter, FormatUtils

__version__ = "2.0.0"
__author__ = "Brasileirão Python Team"
__license__ = "MIT"
__url__ = "https://github.com/fcarlosmonteiro/python-brasileirao"

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
    
    # Cliente HTTP
    'HTTPClient',
    
    # Parsers
    'TabelaParser',
    'RodadasParser',
    
    # Utilitários
    'JSONUtils',
    'DataConverter',
    'FormatUtils'
]
