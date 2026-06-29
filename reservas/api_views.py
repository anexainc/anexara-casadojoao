from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Cliente, Mesa, TipoReserva, PedidoReserva
from .serializers import ClienteSerializer, MesaSerializer, TipoReservaSerializer, PedidoReservaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny] # Permite que o site envie dados sem login administrativo

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [AllowAny]

class TipoReservaViewSet(viewsets.ModelViewSet):
    queryset = TipoReserva.objects.all()
    serializer_class = TipoReservaSerializer
    permission_classes = [AllowAny]

class PedidoReservaViewSet(viewsets.ModelViewSet):
    queryset = PedidoReserva.objects.all()
    serializer_class = PedidoReservaSerializer
    permission_classes = [AllowAny]