import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# --- SCRIPT PARA CRIAR O SUPERUSUÁRIO AUTOMATICAMENTE ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Altere aqui para o usuário e senha que você deseja usar no Render:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('vpictures', 'valmonpictures@gmail.com', 'minhasenha123')
        print("Superusuário criado com sucesso via WSGI!")
except Exception as e:
    print(f"Erro ao criar superusuário: {e}")


# --- SCRIPT PARA IMPORTAR O TEMA AUTOMATICAMENTE ---
try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    
    # Caminho do arquivo json que vai subir pro Render
    tema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tema_casajoao.json')
    
    if os.path.exists(tema_path):
        # Executa o comando de importação dentro do servidor do Render
        call_command('loaddata', tema_path)
        print("Tema personalizado importado com sucesso via WSGI!")
except Exception as e:
    print(f"Erro ao importar o tema: {e}")