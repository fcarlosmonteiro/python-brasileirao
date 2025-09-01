"""
Cliente HTTP para o projeto Brasileirão
Gerencia conexões, User-Agents rotativos e tratamento de erros
"""

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from typing import Optional
from .config import REQUEST_CONFIG

class HTTPClient:
    """Cliente HTTP com User-Agent rotativo e tratamento de erros"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()
    
    def _setup_session(self):
        """Configura a sessão HTTP inicial"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def _rotate_user_agent(self):
        """Rotaciona o User-Agent para evitar bloqueios"""
        if REQUEST_CONFIG['user_agent_rotation']:
            self.session.headers.update({'User-Agent': self.ua.random})
    
    def get_page(self, url: str) -> BeautifulSoup:
        """
        Obtém uma página HTML e retorna um objeto BeautifulSoup
        
        Args:
            url: URL da página a ser obtida
            
        Returns:
            BeautifulSoup object da página
            
        Raises:
            Exception: Em caso de erro na requisição
        """
        try:
            self._rotate_user_agent()
            
            response = self.session.get(
                url, 
                timeout=REQUEST_CONFIG['timeout']
            )
            response.raise_for_status()
            
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.Timeout:
            raise Exception(f"Timeout ao acessar: {url}")
        except requests.HTTPError as e:
            raise Exception(f"Erro HTTP {e.response.status_code}: {url}")
        except requests.RequestException as e:
            raise Exception(f"Erro de conexão: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado: {str(e)}")
    
    def close(self):
        """Fecha a sessão HTTP"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
