"""
Parsers para extrair dados do HTML das páginas do Brasileirão
"""

from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional
from .config import CSS_SELECTORS
from src.models import Time, Partida, Rodada, TabelaClassificacao

class TabelaParser:
    """Parser para dados da tabela de classificação"""
    
    @staticmethod
    def parse_tabela(soup: BeautifulSoup) -> TabelaClassificacao:
        """
        Extrai dados da tabela de classificação
        
        Args:
            soup: BeautifulSoup object da página
            
        Returns:
            TabelaClassificacao com os times
            
        Raises:
            Exception: Em caso de erro no parsing
        """
        try:
            times = []
            seletores = CSS_SELECTORS['tabela']
            
            # Busca todas as linhas da tabela
            linhas_times = soup.select(seletores['linhas'])
            
            for linha in linhas_times:
                time = TabelaParser._parse_linha_time(linha, seletores)
                times.append(time)
            
            return TabelaClassificacao(times=times)
            
        except Exception as e:
            raise Exception(f"Erro ao fazer parsing da tabela: {str(e)}")
    
    @staticmethod
    def _parse_linha_time(linha: Tag, seletores: Dict) -> Time:
        """Extrai dados de uma linha de time da tabela"""
        def get_text(selector: str) -> str:
            element = linha.select_one(selector)
            return element.text.strip() if element else ''
        
        def get_attr(selector: str, attr: str) -> str:
            element = linha.select_one(selector)
            return element[attr] if element and attr in element.attrs else ''
        
        return Time(
            nome=get_attr(seletores['nome'], 'title'),
            escudo=get_attr(seletores['escudo'], 'src'),
            posicao=get_text(seletores['posicao']),
            pontos=get_text(seletores['pontos']),
            jogos=get_text(seletores['jogos']),
            vitorias=get_text(seletores['vitorias']),
            empates=get_text(seletores['empates']),
            derrotas=get_text(seletores['derrotas']),
            gols_pro=get_text(seletores['gols_pro']),
            gols_contra=get_text(seletores['gols_contra']),
            saldo_gols=get_text(seletores['saldo_gols']),
            aproveitamento=get_text(seletores['aproveitamento']) + '%'
        )

class RodadasParser:
    """Parser para dados das rodadas e partidas"""
    
    @staticmethod
    def parse_rodadas(soup: BeautifulSoup) -> List[Rodada]:
        """
        Extrai dados das rodadas e partidas
        
        Args:
            soup: BeautifulSoup object da página
            
        Returns:
            Lista de Rodada com suas partidas
            
        Raises:
            Exception: Em caso de erro no parsing
        """
        try:
            rodadas = []
            seletores = CSS_SELECTORS['rodadas']
            
            # Busca todas as rodadas
            elementos_rodadas = soup.select(seletores['container'])
            
            for elemento_rodada in elementos_rodadas:
                rodada = RodadasParser._parse_rodada(elemento_rodada, seletores)
                rodadas.append(rodada)
            
            return rodadas
            
        except Exception as e:
            raise Exception(f"Erro ao fazer parsing das rodadas: {str(e)}")
    
    @staticmethod
    def _parse_rodada(elemento_rodada: Tag, seletores: Dict) -> Rodada:
        """Extrai dados de uma rodada específica"""
        data_rodada = elemento_rodada.select_one(seletores['data_rodada'])
        if not data_rodada or 'data-date' not in data_rodada.attrs:
            raise Exception("Erro ao obter informações da rodada")
        
        data_completa = data_rodada['data-date']
        data_parts = data_completa.split(" ")[0].split("-")
        ano, mes, dia = data_parts
        
        titulo = elemento_rodada.select_one(seletores['titulo'])
        titulo_texto = titulo.text.strip() if titulo else ''
        
        rodada_atual = 'round' in elemento_rodada.get('class', [])
        
        partidas = RodadasParser._parse_partidas_rodada(elemento_rodada, seletores)
        
        return Rodada(
            rodada=titulo_texto,
            inicio=f"{dia}/{mes}/{ano}",
            rodada_atual=rodada_atual,
            partidas=partidas
        )
    
    @staticmethod
    def _parse_partidas_rodada(elemento_rodada: Tag, seletores: Dict) -> List[Partida]:
        """Extrai partidas de uma rodada específica"""
        partidas = []
        elementos_partidas = elemento_rodada.select(seletores['partidas'])
        
        for partida_element in elementos_partidas:
            partida = RodadasParser._parse_partida(partida_element, seletores)
            partidas.append(partida)
        
        return partidas
    
    @staticmethod
    def _parse_partida(partida_element: Tag, seletores: Dict) -> Partida:
        """Extrai dados de uma partida específica"""
        times_meta = partida_element.select_one(seletores['times_meta'])
        if not times_meta or 'content' not in times_meta.attrs:
            raise Exception("Erro ao obter informações da partida")
        
        times = times_meta['content']
        time_casa, time_fora = [t.strip() for t in times.split("x")]
        
        gols_casa = partida_element.select_one(seletores['gols_casa'])
        gols_casa_texto = gols_casa.text.strip() if gols_casa else ''
        
        gols_fora = partida_element.select_one(seletores['gols_fora'])
        gols_fora_texto = gols_fora.text.strip() if gols_fora else ''
        
        data_partida = partida_element.select_one(seletores['data_partida'])
        data_texto = data_partida.text.strip() if data_partida else ''
        
        local_partida = partida_element.select_one(seletores['local'])
        local_texto = local_partida.text.strip() if local_partida else ''
        
        return Partida(
            partida=times,
            data=data_texto,
            local=local_texto,
            time_casa=time_casa,
            time_fora=time_fora,
            gols_casa=gols_casa_texto,
            gols_fora=gols_fora_texto,
            resultado_texto=f"{time_casa} {gols_casa_texto} x {gols_fora_texto} {time_fora}"
        )
