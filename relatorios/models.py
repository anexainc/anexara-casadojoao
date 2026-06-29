from django.db import models
from reservas.models import PedidoReserva


# estilo PROXY
# Relatório de Giro e Ocupação
class GiroOcupacao(PedidoReserva):
    class Meta:
        proxy = True
        verbose_name = "📈 Giro & Ocupação"
        verbose_name_plural = "📈 Giro & Ocupação"


# Relatório Turnos de Picos (Almoço vs. Jantar)
class TurnosPico(PedidoReserva):
    class Meta:
        proxy = True
        verbose_name = "📈 Almoço vs. Jantar"
        verbose_name_plural = "📈 Almoços vs. Jantares"



class FrequenciaReservas(PedidoReserva):
    class Meta:
        proxy = True
        verbose_name = "📈 Frequência de Reservas"
        verbose_name_plural = "📈 Frequência de Reservas"