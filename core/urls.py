from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from reservas.api_views import ClienteViewSet, MesaViewSet, TipoReservaViewSet, PedidoReservaViewSet
from reservas.views import buscar_mesas_disponiveis, imprimir_etiquetas_view, lista_portaria_view
from relatorios.views import giro_ocupacao_view, turnos_pico_view, frequencia_reservas_view



# Rota do DRF cria os links automaticamente (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'mesas', MesaViewSet)
router.register(r'tipos-reserva', TipoReservaViewSet)
router.register(r'pedidos-reserva', PedidoReservaViewSet)


urlpatterns = [
    path('admin/buscar-mesas/', buscar_mesas_disponiveis, name='buscar_mesas'),
    path('api/', include(router.urls)), # Todos os links da API vão começar com /api/
    # Rota para impressão das etiquetas para as Mesas
    path('relatorios/imprimir-etiquetas/', imprimir_etiquetas_view, name='imprimir_etiquetas'),
    # Rota para a listagem das reservas para recepção na portaria
    path('relatorios/lista-portaria/', lista_portaria_view, name='lista_portaria'),
    # Rota para Proxy Giro & Ocupação
    path('admin/giro-ocupacao/', giro_ocupacao_view, name='giro_ocupacao'),
    # Rota para Proxy Almoço vs. Jantar
    path('admin/turnos-pico/', turnos_pico_view, name='turnos_pico'),
    # Rota para Proxy Frequencia de Reservas
    path('admin/frequencia-reservas/', frequencia_reservas_view, name='frequencia_reservas'),


    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# Suprime 'VER O SITE' do cabeçalho
admin.site.site_url = None
# Muda a frase ("Administração do Site") no subCabeçalho
admin.site.index_title = "anexaRA"
# Texto do cabeçalho superior esquerdo
# admin.site.site_header = "Casa do João Admin"