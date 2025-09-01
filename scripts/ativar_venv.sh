#!/bin/bash
# Script para ativar o ambiente virtual do projeto

echo "🐍 Ativando ambiente virtual do Brasileirão Python..."

# Verificar se estamos no diretório correto
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado!"
    echo "💡 Certifique-se de estar na pasta raiz do projeto"
    echo "💡 Execute: cd /caminho/para/python-brasileirao"
    exit 1
fi

# Ativar ambiente virtual
source venv/bin/activate

echo "✅ Ambiente virtual ativado!"
echo "🚀 Agora você pode executar:"
echo "   python scripts/coletar_dados.py"
echo ""
echo "💡 Para desativar: deactivate"
