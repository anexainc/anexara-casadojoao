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