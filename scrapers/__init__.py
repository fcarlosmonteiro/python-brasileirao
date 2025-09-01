"""
Brasileirão Python - Módulo de Scraping
Contém os componentes para coleta de dados das páginas web
"""

from .http_client import HTTPClient
from .parsers import TabelaParser, RodadasParser
from .config import URLS, REQUEST_CONFIG, CSS_SELECTORS

__all__ = [
    # Cliente HTTP
    'HTTPClient',
    
    # Parsers
    'TabelaParser',
    'RodadasParser',
    
    # Configurações
    'URLS',
    'REQUEST_CONFIG',
    'CSS_SELECTORS'
]
