from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Cliente, TipoReserva, Mesa, PedidoReserva
from datetime import date
from django.shortcuts import redirect



# 1. Personalização do Usuário do Sistema (Colaboradores e Gerência)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# 2. Gestão de Clientes (Independente)
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('whatsapp', 'nome', 'data_nascimento', 'email', 'ativo', 'data_cadastro')
    list_filter = ('nome', 'ativo', 'data_cadastro')
    search_fields = ('nome', 'whatsapp', 'email')
    list_editable = ('ativo',) 
    ordering = ('-data_cadastro',)


# 3. Mesas e Tipos
@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'capacidade')
    search_fields = ('descricao',)

@admin.register(TipoReserva)
class TipoReservaAdmin(admin.ModelAdmin):
    list_display = ('descricao',)

# Filtra os Pedidos de Reservas para trazer data "Hoje" como padrão
class DataHojeFilter(admin.SimpleListFilter):
    title = 'Data da Reserva'
    parameter_name = 'data_reserva'

    def lookups(self, request, model_admin):
        return (
            ('hoje', 'Hoje'),
            ('todas', 'Todas as datas'),
        )

    def queryset(self, request, queryset):
        # Se não houver nenhum filtro selecionado na URL, aplica o padrão (Hoje)
        if self.value() == 'hoje' or self.value() is None:
            return queryset.filter(data=date.today())
        if self.value() == 'todas':
            return queryset
        return queryset


# 4. Pedidos de Reserva
@admin.register(PedidoReserva)
class PedidoReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente_nome', 'data', 'mesa', 'status', 'colaborador')
    list_filter = (DataHojeFilter, 'status', 'tipo_reserva')
    list_editable = ('status',)
    readonly_fields = ('colaborador',)
    autocomplete_fields = ['cliente'] 
    
    # ATIVA A NOVA AÇÃO NO PAINEL ADMIN
    actions = ['imprimir_etiquetas']
    actions = ['imprimir_etiquetas', 'gerar_lista_portaria']

    # NOVA ACTION: Lista da Portaria
    @admin.action(description="Gerar Lista da Portaria (A4)")
    def gerar_lista_portaria(self, request, queryset):
        # Ordena por nome do Cliente para facilitar a busca na portaria
        selected_ids = ",".join([str(reserva.id) for reserva in queryset])
        
        # Redireciona para uma nova URL
        url = reverse('lista_portaria')
        return HttpResponseRedirect(f"{url}?ids={selected_ids}")


    def get_cliente_nome(self, obj):
        return obj.cliente.nome
    get_cliente_nome.short_description = 'Cliente'

    def save_model(self, request, obj, form, change):
        if not obj.colaborador:
            obj.colaborador = request.user
        super().save_model(request, obj, form, change)

    # LÓGICA DAS ETIQUETAS
    @admin.action(description="Imprimir etiqueta para as Mesas")
    def imprimir_etiquetas(self, request, queryset):
        # Junta os IDs de todas as reservas selecionadas separando por vírgula
        selected_ids = ",".join([str(reserva.id) for reserva in queryset])
        # Pega a URL da nossa view que criamos no urls.py
        url = reverse('imprimir_etiquetas')
        # Redireciona de forma padrão e limpa para a página de relatórios
        return HttpResponseRedirect(f"{url}?ids={selected_ids}")

    class Media:
        js = ('js/reservas_admin.js',)
