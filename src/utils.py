"""
Utilitários para o projeto Brasileirão
Funções para JSON, formatação e conversões
"""

import json
from typing import Dict, Any, Union
from .models import (
    Time, Partida, Rodada, TabelaClassificacao, DadosBrasileirao,
    TimeDict, PartidaDict, RodadaDict, TabelaDict, DadosBrasileiraoDict
)

class JSONUtils:
    """Utilitários para manipulação de JSON"""
    
    @staticmethod
    def save_to_json(data: Union[Dict, Any], filename: str, encoding: str = 'utf-8') -> bool:
        """
        Salva dados em um arquivo JSON
        
        Args:
            data: Dados a serem salvos
            filename: Nome do arquivo
            encoding: Encoding do arquivo
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            with open(filename, 'w', encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {str(e)}")
            return False
    
    @staticmethod
    def load_from_json(filename: str, encoding: str = 'utf-8') -> Union[Dict, None]:
        """
        Carrega dados de um arquivo JSON
        
        Args:
            filename: Nome do arquivo
            encoding: Encoding do arquivo
            
        Returns:
            Dados carregados ou None em caso de erro
        """
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar arquivo JSON: {str(e)}")
            return None

class DataConverter:
    """Conversor entre modelos e dicionários"""
    
    @staticmethod
    def time_to_dict(time: Time) -> TimeDict:
        """Converte modelo Time para dicionário"""
        return {
            'nome': time.nome,
            'escudo': time.escudo,
            'posicao': time.posicao,
            'pontos': time.pontos,
            'jogos': time.jogos,
            'vitorias': time.vitorias,
            'empates': time.empates,
            'derrotas': time.derrotas,
            'gols_pro': time.gols_pro,
            'gols_contra': time.gols_contra,
            'saldo_gols': time.saldo_gols,
            'aproveitamento': time.aproveitamento
        }
    
    @staticmethod
    def partida_to_dict(partida: Partida) -> PartidaDict:
        """Converte modelo Partida para dicionário"""
        return {
            'partida': partida.partida,
            'data': partida.data,
            'local': partida.local,
            'time_casa': partida.time_casa,
            'time_fora': partida.time_fora,
            'gols_casa': partida.gols_casa,
            'gols_fora': partida.gols_fora,
            'resultado_texto': partida.resultado_texto
        }
    
    @staticmethod
    def rodada_to_dict(rodada: Rodada) -> RodadaDict:
        """Converte modelo Rodada para dicionário"""
        return {
            'rodada': rodada.rodada,
            'inicio': rodada.inicio,
            'rodada_atual': rodada.rodada_atual,
            'partidas': [DataConverter.partida_to_dict(p) for p in rodada.partidas]
        }
    
    @staticmethod
    def tabela_to_dict(tabela: TabelaClassificacao) -> TabelaDict:
        """Converte modelo TabelaClassificacao para dicionário"""
        return [DataConverter.time_to_dict(time) for time in tabela.times]
    
    @staticmethod
    def dados_brasileirao_to_dict(dados: DadosBrasileirao) -> DadosBrasileiraoDict:
        """Converte modelo DadosBrasileirao para dicionário"""
        resultado = {
            'tabela': DataConverter.tabela_to_dict(dados.tabela)
        }
        
        if dados.rodadas:
            resultado['rodadas'] = [DataConverter.rodada_to_dict(r) for r in dados.rodadas]
        
        return resultado

class FormatUtils:
    """Utilitários para formatação de dados"""
    
    @staticmethod
    def format_aproveitamento(pontos: str, jogos: str) -> str:
        """
        Calcula e formata o aproveitamento baseado em pontos e jogos
        
        Args:
            pontos: Pontos do time
            jogos: Número de jogos
            
        Returns:
            Aproveitamento formatado como string
        """
        try:
            pontos_int = int(pontos)
            jogos_int = int(jogos)
            
            if jogos_int == 0:
                return "0%"
            
            aproveitamento = (pontos_int / (jogos_int * 3)) * 100
            return f"{aproveitamento:.0f}%"
        except (ValueError, ZeroDivisionError):
            return "0%"
    
    @staticmethod
    def format_saldo_gols(gols_pro: str, gols_contra: str) -> str:
        """
        Calcula e formata o saldo de gols
        
        Args:
            gols_pro: Gols a favor
            gols_contra: Gols contra
            
        Returns:
            Saldo de gols formatado como string
        """
        try:
            gols_pro_int = int(gols_pro)
            gols_contra_int = int(gols_contra)
            saldo = gols_pro_int - gols_contra_int
            
            if saldo > 0:
                return f"+{saldo}"
            else:
                return str(saldo)
        except ValueError:
            return "0"
