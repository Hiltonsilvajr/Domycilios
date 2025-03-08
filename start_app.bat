@echo off
echo Iniciando o aplicativo Domycilios...

REM Verificar se o ambiente virtual existe
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar o ambiente virtual
call venv\Scripts\activate

REM Instalar dependências
echo Instalando dependências...
pip install -r requirements.txt

REM Iniciar a aplicação
echo Iniciando a aplicação...
python run.py

pause 