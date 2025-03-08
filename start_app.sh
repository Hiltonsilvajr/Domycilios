#!/bin/bash

echo "Iniciando o aplicativo Domycilios..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Iniciar a aplicação
echo "Iniciando a aplicação..."
python run.py 