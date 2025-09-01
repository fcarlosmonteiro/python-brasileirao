"""
Classe principal do Brasileirão Python
Orquestra a obtenção de dados usando os módulos especializados
"""

from typing import Dict, Optional
from scrapers.http_client import HTTPClient
from scrapers.parsers import TabelaParser, RodadasParser
from .utils import DataConverter, JSONUtils
from scrapers.config import URLS
from .models import DadosBrasileirao

class Brasileirao:
    """Classe principal para obter dados do Brasileirão Série A e B"""
    
    def __init__(self):
        """Inicializa a classe com cliente HTTP"""
        self.http_client = HTTPClient()
    
    def obter_dados_brasileirao_a(self, rodadas: bool = True) -> Dict:
        """
        Obtém dados do Brasileirão Série A
        
        Args:
            rodadas: Se deve incluir dados das rodadas
            
        Returns:
            Dicionário com dados da Série A ou erro
        """
        try:
            return self._obter_dados_serie('serie_a', rodadas)
        except Exception as e:
            return {'erro': str(e)}
    
    def obter_dados_brasileirao_b(self, rodadas: bool = True) -> Dict:
        """
        Obtém dados do Brasileirão Série B
        
        Args:
            rodadas: Se deve incluir dados das rodadas
            
        Returns:
            Dicionário com dados da Série B ou erro
        """
        try:
            return self._obter_dados_serie('serie_b', rodadas)
        except Exception as e:
            return {'erro': str(e)}
    
    def _obter_dados_serie(self, serie: str, rodadas: bool) -> Dict:
        """
        Método interno para obter dados de uma série específica
        
        Args:
            serie: Nome da série ('serie_a' ou 'serie_b')
            rodadas: Se deve incluir rodadas
            
        Returns:
            Dicionário com dados da série
        """
        urls = URLS[serie]
        
        tabela_soup = self.http_client.get_page(urls['tabela'])
        tabela = TabelaParser.parse_tabela(tabela_soup)
        
        resultado = DataConverter.dados_brasileirao_to_dict(
            DadosBrasileirao(tabela=tabela)
        )
        
        if rodadas:
            rodadas_soup = self.http_client.get_page(urls['rodadas'])
            rodadas_data = RodadasParser.parse_rodadas(rodadas_soup)
            resultado['rodadas'] = [DataConverter.rodada_to_dict(r) for r in rodadas_data]
        
        return resultado
    
    def salvar_json(self, dados: Dict, arquivo: str) -> bool:
        """
        Salva os dados em um arquivo JSON
        
        Args:
            dados: Dados a serem salvos
            arquivo: Nome do arquivo
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if JSONUtils.save_to_json(dados, arquivo):
            print(f"Dados salvos em: {arquivo}")
            return True
        else:
            print(f"Erro ao salvar arquivo: {arquivo}")
            return False
    
    def close(self):
        """Fecha o cliente HTTP"""
        self.http_client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Funções de conveniência para compatibilidade com a API original
def obter_dados_brasileirao_a(rodadas: bool = True) -> Dict:
    """
    Função de conveniência para obter dados da Série A
    
    Args:
        rodadas: Se deve incluir dados das rodadas
        
    Returns:
        Dicionário com dados da Série A
    """
    with Brasileirao() as brasileirao:
        return brasileirao.obter_dados_brasileirao_a(rodadas)

def obter_dados_brasileirao_b(rodadas: bool = True) -> Dict:
    """
    Função de conveniência para obter dados da Série B
    
    Args:
        rodadas: Se deve incluir dados das rodadas
        
    Returns:
        Dicionário com dados da Série B
    """
    with Brasileirao() as brasileirao:
        return brasileirao.obter_dados_brasileirao_b(rodadas)
