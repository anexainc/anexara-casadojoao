@echo off
:: Script de Configuracao Automatizada - AnexaRA (Windows)
:: Este script prepara o ambiente virtual, instala as dependencias, cria o admin e levanta o servidor.

echo =====================================================================
echo    ANEXARA - SCRIPT DE CONFIGURACAO RAPIDA E INTEGRACAO (WINDOWS)
echo =====================================================================
echo.

:: 1. Verificacao do Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado no sistema!
    echo Por favor, instale o Python 3.10+ e marque a opcao "Add Python to PATH".
    pause
    exit /b
)

:: 2. Criacao do Ambiente Virtual (venv)
if not exist venv (
    echo [INFO] Criando ambiente virtual (venv)...
    python -m venv venv
    echo [SUCESSO] Ambiente virtual criado!
) else (
    echo [INFO] Ambiente virtual (venv) ja existe. Pulando criacao.
)
echo.

:: 3. Atualizacao do Pip e Instalacao de Dependencias
echo [INFO] Ativando ambiente virtual e instalando pacotes necessarios...
call venv\Scripts\activate
python -m pip install --upgrade pip

if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo [INFO] Instalando pacotes manualmente...
    pip install django django-admin-interface django-colorfield djangorestframework django-cors-headers psycopg2-binary
)
echo [SUCESSO] Todas as ferramentas do Django e API foram instaladas!
echo.

:: 4. Migracoes do Banco de Dados
echo [INFO] Rodando preparacao das tabelas no PostgreSQL...
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata tema_casajoao.json
echo.

:: 5. Criacao Automatica do Superusuario de Teste
echo [INFO] Criando superusuario administrador de testes...
echo os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); import django; django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='mahfelipe').delete(); User.objects.create_superuser('mahfelipe', 'mahfelipe982@gmail.com', 'AgoraVai') | python
echo [SUCESSO] Administrador 'mahfelipe' criado ou atualizado!
echo.

:: 6. Inicializacao do Servidor
echo =====================================================================
echo [PRONTO] O AnexaRA esta inicializando na porta 8000!
echo Para a apresentacao publica, abra OUTRO terminal e rode: ngrok http 8000
echo.
echo Dados de Acesso Administrativo para o Teste:
echo Usuario: mahfelipe
echo Senha:   AgoraVai
echo =====================================================================
echo.
python manage.py runserver 0.0.0.0:8000

pause
