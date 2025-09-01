"""
Configurações e constantes do projeto Brasileirão
"""

# URLs das APIs da TRRSF
URLS = {
    'serie_a': {
        'tabela': "https://p1.trrsf.com/api/musa-soccer/ms-standings-light?idChampionship=1436&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR",
        'rodadas': "https://p1.trrsf.com/api/musa-soccer/ms-standings-games-light?idChampionship=1436&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR"
    },
    'serie_b': {
        'tabela': "https://p1.trrsf.com/api/musa-soccer/ms-standings-light?idChampionship=1438&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR",
        'rodadas': "https://p1.trrsf.com/api/musa-soccer/ms-standings-games-light?idChampionship=1438&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR"
    }
}

# Configurações de requisição
REQUEST_CONFIG = {
    'timeout': 30,
    'max_retries': 3,
    'user_agent_rotation': True
}

# Seletores CSS para parsing
CSS_SELECTORS = {
    'tabela': {
        'linhas': "table > tbody > tr",
        'nome': '.team-name > a',
        'escudo': '.shield > a > img',
        'posicao': '.position',
        'pontos': '.points',
        'jogos': 'td[title="Jogos"]',
        'vitorias': 'td[title="Vitórias"]',
        'empates': 'td[title="Empates"]',
        'derrotas': 'td[title="Derrotas"]',
        'gols_pro': 'td[title="Gols Pró"]',
        'gols_contra': 'td[title="Gols Contra"]',
        'saldo_gols': 'td[title="Saldo de Gols"]',
        'aproveitamento': 'td[title="Aproveitamento"]'
    },
    'rodadas': {
        'container': "ul.rounds > li",
        'data_rodada': "br.date-round",
        'titulo': "h3",
        'partidas': "li.match",
        'times_meta': 'meta[itemprop="name"]',
        'gols_casa': '.goals.home',
        'gols_fora': '.goals.away',
        'data_partida': 'div.details > strong.date-manager',
        'local': 'div.details > span.stadium'
    }
}
