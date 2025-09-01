# 📊 Dataset - Brasileirão Python

Esta pasta contém a estrutura organizada para coleta, armazenamento e análise dos dados do Brasileirão.

## 📁 Estrutura de Pastas

```
dataset/
├── serie_a/              # Dados específicos da Série A
├── serie_b/              # Dados específicos da Série B
├── scripts/              # Scripts para coleta e processamento
├── exemplos/             # Exemplos de dados coletados
├── dados_coletados/      # Dados coletados por data (criado automaticamente)
└── README.md             # Este arquivo
```

## 🚀 Como Usar

### 1. Coleta Automática de Dados

Execute o script de coleta para obter dados atualizados:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar coleta
python scripts/coletar_dados.py
```

### 2. Estrutura dos Dados Coletados

Os dados são salvos automaticamente em:
- `dataset/dados_coletados/YYYY-MM-DD/serie_a.json` - Dados completos da Série A
- `dataset/dados_coletados/YYYY-MM-DD/serie_b.json` - Dados completos da Série B

### 3. Formato dos Dados

Cada arquivo JSON contém:
- **Tabela**: Classificação atual com todos os times
- **Rodadas**: Todas as rodadas com partidas e resultados

## 📊 Exemplos de Dados

Veja a pasta `exemplos/` para arquivos de exemplo com dados reais do Brasileirão.

## 🔧 Scripts Disponíveis

- `coletar_dados.py` - Script principal para coleta automática
- (Futuros scripts para análise e processamento)

## 📈 Histórico de Coleta

Os dados são organizados por data, permitindo:
- Análise temporal das classificações
- Comparação entre diferentes rodadas
- Rastreamento da evolução dos times

## 🎯 Próximos Passos

- [ ] Scripts de análise estatística
- [ ] Comparação entre temporadas
- [ ] Exportação para outros formatos (CSV, Excel)
- [ ] Dashboard de visualização
- [ ] API para consulta dos dados históricos
