from rest_framework import serializers
from .models import Cliente, Mesa, TipoReserva, PedidoReserva

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'whatsapp', 'email', 'ativo']
        
class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'descricao', 'capacidade']

class TipoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoReserva
        fields = ['id', 'descricao']

class PedidoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoReserva
        fields = ['id', 'cliente', 'data', 'numero_pessoas', 'tipo_reserva', 'mesa', 'status', 'observacoes']