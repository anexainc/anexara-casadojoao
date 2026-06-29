from django.contrib import admin
from django.shortcuts import redirect
from .models import GiroOcupacao, TurnosPico, FrequenciaReservas


@admin.register(GiroOcupacao)
class GiroOcupacaoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request): return False
    def has_change_permission(self, request): return False

    # Segurança por permissão nativa
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('relatorios.view_giroocupacao')

    def has_module_permission(self, request):
        return request.user.has_perm('relatorios.view_giroocupacao')

    # Redireciona para a view
    def changelist_view(self, request, extra_context=None):
        return redirect('giro_ocupacao')
    


@admin.register(TurnosPico)
class TurnosPicoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request): return False
    def has_change_permission(self, request): return False

    # Trava de segurança
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('relatorios.view_turnospico')

    def has_module_permission(self, request):
        return request.user.has_perm('relatorios.view_turnospico')

    # Redireciona para a rota
    def changelist_view(self, request, extra_context=None):
        return redirect('turnos_pico')
    


@admin.register(FrequenciaReservas)
class FrequenciaReservasAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request): return False
    def has_change_permission(self, request): return False

    # Trava de segurança nativa django
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('relatorios.view_frequenciareservas')

    def has_module_permission(self, request):
        return request.user.has_perm('relatorios.view_frequenciareservas')

    # Redireciona para a rota
    def changelist_view(self, request, extra_context=None):
        return redirect('frequencia_reservas')
    
