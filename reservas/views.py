from django.http import JsonResponse
from .models import Mesa, PedidoReserva
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def buscar_mesas_disponiveis(request):
    """
    View que filtra as mesas disponíveis com base na data, 
    tipo de reserva e quantidade de pessoas.
    """
    try:
        # 1. Pegamos os dados que o JavaScript enviou
        data_str = request.GET.get('data')
        tipo_id = request.GET.get('tipo')
        pessoas_str = request.GET.get('pessoas', '0')
        
        # Converte a quantidade de pessoas para número inteiro
        pessoas = int(pessoas_str) if pessoas_str.isdigit() else 0

        # Se não houver data ou tipo selecionado ainda, retornamos uma lista vazia
        if not data_str or not tipo_id:
            return JsonResponse([], safe=False)

        # O navegador manda "10/05/2026", o Python converte para objeto de data real
        try:
            if '/' in data_str:
                data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
            else:
                data_obj = data_str # Caso já esteja no formato AAAA-MM-DD
        except ValueError:
            return JsonResponse({'error': 'Formato de data inválido'}, status=400)

        # 3. FILTRO DE CAPACIDADE E ORDENAÇÃO
        # Buscamos mesas que comportam o grupo, da menor para a maior
        mesas_possiveis = Mesa.objects.filter(capacidade__gte=pessoas).order_by('capacidade')

        # Verificamos quais mesas já têm reservas CONFIRMADAS para esse dia e turno
        ocupadas_ids = PedidoReserva.objects.filter(
            data=data_obj,
            tipo_reserva_id=tipo_id,
            status='confirmado'
        ).values_list('mesa_id', flat=True)

        # Excluímos as ocupadas da nossa lista de sugestões
        disponiveis = mesas_possiveis.exclude(id__in=ocupadas_ids)

        # Montamos o pacote de dados (JSON) para enviar de volta
        dados = [
            {
                'id': m.id, 
                'descricao': f"{m.descricao} (Capacidade: {m.capacidade})"
            } 
            for m in disponiveis
        ]
        
        return JsonResponse(dados, safe=False)

    except Exception as e:
        # Se algo der muito errado, o sistema avisa o erro exato no console
        return JsonResponse({'error': str(e)}, status=500)
    

# organiza as reservas do dia para gerar etiqueta para as mesas
def imprimir_etiquetas_view(request):
    # IDs das reservas que foram passados pela URL
    ids_ids = request.GET.get('ids', '')
    if ids_ids:
        ids_list = ids_ids.split(',')
        # apenas as reservas selecionadas
        reservas = PedidoReserva.objects.filter(id__in=ids_list).select_related('cliente', 'mesa')
    else:
        reservas = PedidoReserva.objects.none()
        
    return render(request, 'reservas/etiquetas.html', {'reservas': reservas})


@login_required
def lista_portaria_view(request):
    ids_str = request.GET.get('ids', '')
    if ids_str:
        ids = ids_str.split(',')
        reservas = PedidoReserva.objects.filter(
            id__in=ids, 
            status='confirmado'
        ).select_related('cliente', 'mesa').order_by('cliente__nome')
    else:
        reservas = PedidoReserva.objects.none()
        
    return render(request, 'reservas/lista_portaria.html', {'reservas': reservas})

