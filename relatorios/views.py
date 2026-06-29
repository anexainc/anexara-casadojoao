from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F, FloatField
from django.db.models.functions import Cast
from reservas.models import PedidoReserva 



@staff_member_required
def giro_ocupacao_view(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    reservas_query = PedidoReserva.objects.filter(status='confirmado')
    
    if data_inicio and data_fim:
        reservas_query = reservas_query.filter(data__range=[data_inicio, data_fim])
    
    # CÁLCULO DE OCUPAÇÃO GERAL
    estatisticas = reservas_query.aggregate(
        total_pessoas=Sum('numero_pessoas'),
        total_capacidade=Sum('mesa__capacidade')
    )
    
    total_pessoas = estatisticas['total_pessoas'] or 0
    total_capacidade = estatisticas['total_capacidade'] or 0
    
    taxa_ocupacao_geral = 0
    if total_capacidade > 0:
        taxa_ocupacao_geral = round((total_pessoas / total_capacidade) * 100, 1)
        
    # CÁLCULO LINHA A LINHA
    reservas_detalhe = reservas_query.annotate(
        porcentagem_uso=Cast(F('numero_pessoas'), FloatField()) / Cast(F('mesa__capacidade'), FloatField()) * 100
    ).select_related('cliente', 'mesa').order_by('-data')

    contexto = {
        'taxa_ocupacao_geral': taxa_ocupacao_geral,
        'total_pessoas': total_pessoas,
        'total_capacidade': total_capacidade,
        'reservas': reservas_detalhe,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(request, 'relatorios/giroOcupacao.html', contexto)



@staff_member_required
def turnos_pico_view(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    reservas_query = PedidoReserva.objects.filter(status='confirmado')
    
    if data_inicio and data_fim:
        reservas_query = reservas_query.filter(data__range=[data_inicio, data_fim])
    
    # MOTOR DO RELATÓRIO: Agrupa por Tipo de Reserva (Almoço, Jantar...)
    # Conta os pedidos e soma o total de pessoas de cada turno
    movimento_por_turno = reservas_query.values(
        nome_turno=F('tipo_reserva__descricao')
    ).annotate(
        total_reservas=Count('id'),
        total_clientes=Sum('numero_pessoas')
    ).order_by('-total_clientes') # O turno mais movimentado aparece no topo!
    
    # Calcula também os totais gerais do período para colocar nos cartões
    totais_gerais = reservas_query.aggregate(
        grand_total_reservas=Count('id'),
        grand_total_clientes=Sum('numero_pessoas')
    )

    contexto = {
        'movimento_por_turno': movimento_por_turno,
        'total_geral_reservas': totais_gerais['grand_total_reservas'] or 0,
        'total_geral_clientes': totais_gerais['grand_total_clientes'] or 0,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    return render(request, 'relatorios/turnosPico.html', contexto)



@staff_member_required
def frequencia_reservas_view(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    reservas_query = PedidoReserva.objects.filter(status='confirmado')
    
    if data_inicio and data_fim:
        reservas_query = reservas_query.filter(data__range=[data_inicio, data_fim])
    
    # Agrupa por Perfil do Cliente
    # Conta a quantidade de reservas e soma o total de pessoas trazidas por cada cliente
    ranking_clientes = reservas_query.values(
        nome_cliente=F('cliente__nome'),
        telefone_cliente=F('cliente__whatsapp')
    ).annotate(
        qtd_reservas=Count('id'),
        total_convidados=Sum('numero_pessoas')
    ).order_by('-qtd_reservas', '-total_convidados') # Quem reserva mais vezes fica no topo!

    contexto = {
        'ranking_clientes': ranking_clientes,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    return render(request, 'relatorios/frequenciaReservas.html', contexto)