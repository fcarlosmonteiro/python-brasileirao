# ⚽ Brasileirão Python ⚽

Versão Python do projeto Brasileirão - Scraper para obter dados da tabela e das rodadas do Brasileirão Série A e B.

> **📋 Baseado no projeto original:** [@victorsouzaleal/brasileirao](https://github.com/victorsouzaleal/brasileirao) - Versão TypeScript/JavaScript

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/fcarlosmonteiro/python-brasileirao)

## 🚀 Instalação

### Pré-requisitos
- Python 3.7+
- pip

### Instalar dependências
```bash
pip install -r requirements.txt
```

## 📚 Como Usar

### Importar a biblioteca
```python
from brasileirao import Brasileirao, obter_dados_brasileirao_a, obter_dados_brasileirao_b
```

### Usando a classe Brasileirao
```python
# Criar instância
brasileirao = Brasileirao()

# Obter dados da Série A com rodadas
dados_a = brasileirao.obter_dados_brasileirao_a(rodadas=True)

# Obter dados da Série B sem rodadas
dados_b = brasileirao.obter_dados_brasileirao_b(rodadas=False)

# Salvar dados em JSON
brasileirao.salvar_json(dados_a, 'serie_a.json')

# Fechar conexões (importante!)
brasileirao.close()
```

### Usando context manager (recomendado)
```python
# Usando with (fecha automaticamente)
with Brasileirao() as brasileirao:
    dados_a = brasileirao.obter_dados_brasileirao_a(rodadas=True)
    brasileirao.salvar_json(dados_a, 'serie_a.json')
```

### Usando funções de conveniência
```python
# Série A
dados_a = obter_dados_brasileirao_a(rodadas=True)

# Série B
dados_b = obter_dados_brasileirao_b(rodadas=False)
```

## 📊 Estrutura dos Dados

### Tabela de Classificação
```python
{
    'tabela': [
        {
            'nome': 'Flamengo',
            'escudo': 'https://...',
            'posicao': '1',
            'pontos': '14',
            'jogos': '7',
            'vitorias': '4',
            'empates': '2',
            'derrotas': '1',
            'gols_pro': '13',
            'gols_contra': '6',
            'saldo_gols': '7',
            'aproveitamento': '66%'
        }
    ]
}
```

### Rodadas e Partidas
```python
{
    'rodadas': [
        {
            'rodada': '1ª rodada',
            'inicio': '13/04/2024',
            'rodada_atual': False,
            'partidas': [
                {
                    'partida': 'Criciúma x Juventude',
                    'data': 'Sáb 13/04 18h30',
                    'local': 'Heriberto Hülse',
                    'time_casa': 'Criciúma',
                    'time_fora': 'Juventude',
                    'gols_casa': '1',
                    'gols_fora': '1',
                    'resultado_texto': 'Criciúma 1 x 1 Juventude'
                }
            ]
        }
    ]
}
```

## 📊 Dataset e Coleta de Dados

### Coleta Automática

Para coletar dados automaticamente e organizá-los na pasta dataset:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar coleta automática
python scripts/coletar_dados.py

# Ou apenas Série B
python scripts/coletar_serie_b.py
```

### Estrutura dos Dados

Os dados são organizados automaticamente por data:
- `dataset/dados_coletados/YYYY-MM-DD/serie_a.json` - Dados da Série A
- `dataset/dados_coletados/YYYY-MM-DD/serie_b.json` - Dados da Série B

Cada arquivo contém tabela de classificação e rodadas completas.

### Scripts Disponíveis

- **`coletar_dados.py`**: Script principal para coleta automática
- **`exemplo_uso.py`**: Exemplos de uso da biblioteca
- **Documentação**: Veja `dataset/README.md` para detalhes

## 🔧 Funcionalidades

- ✅ **Série A**: Tabela e rodadas completas
- ✅ **Série B**: Tabela e rodadas completas
- ✅ **Exportação JSON**: Salva dados em arquivos

## 📁 Estrutura do Projeto

```
python-brasileirao/
├── __init__.py              # Inicialização do pacote
├── src/                     # Código fonte principal
│   ├── __init__.py          # Inicialização do módulo src
│   ├── brasileirao.py       # Classe principal (orquestradora)
│   ├── models.py            # Modelos de dados e tipos
│   └── utils.py             # Utilitários (JSON, conversões)
├── scrapers/                # Módulos de scraping
│   ├── __init__.py          # Inicialização do módulo scrapers
│   ├── http_client.py       # Cliente HTTP com User-Agent rotativo
│   ├── parsers.py           # Parsers para HTML
│   └── config.py            # Configurações e constantes
├── scripts/                 # Scripts de automação
│   ├── coletar_dados.py     # Script principal de coleta
│   ├── coletar_serie_b.py   # Script específico da Série B
├── dataset/                 # Estrutura para dados
│   ├── serie_a/             # Dados específicos da Série A
│   ├── serie_b/             # Dados específicos da Série B
│   ├── exemplos/            # Exemplos de dados coletados
│   ├── dados_coletados/     # Dados coletados por data
│   ├── README.md            # Documentação da pasta dataset
│   └── .gitignore           # Arquivos a serem ignorados
├── tests/                   # Testes unitários (futuro)
├── docs/                    # Documentação (futuro)
├── requirements.txt         # Dependências Python
├── LICENSE                  # Licença MIT
└── README.md                # Este arquivo
```

## 📋 Créditos e Licença

### 🤝 **Projeto Original**
Este projeto é uma versão Python do [@victorsouzaleal/brasileirao](https://github.com/victorsouzaleal/brasileirao), desenvolvido em TypeScript/JavaScript.

**Características do projeto original:**
- ✅ **4 stars** e **3 forks** no GitHub
- ✅ **Licença MIT** - Software livre e open source
- ✅ **API compatível** - Mesma estrutura de dados
- ✅ **Funcionalidades completas** - Tabela e rodadas das Séries A e B

### 📄 **Licença**
Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 🙏 **Agradecimentos**
- **@victorsouzaleal** - Pelo projeto original em TypeScript
- **Comunidade open source** - Pela inspiração e colaboração
- **Contribuidores** - Por tornarem este projeto possível