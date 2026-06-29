from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    whatsapp = models.CharField(unique=True, blank=False, null=False, max_length=20, verbose_name="WhatsApp/Usuário")
    nome = models.CharField(max_length=100,blank=False, null=False, verbose_name="Nome Completo")
    data_nascimento = models.DateField(blank=False, null=False, verbose_name="Data do nascimento")
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="E-mail")
    ativo = models.BooleanField(default=True, verbose_name="Cadastro Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Ativo" if self.ativo else "Pendente"
        return f"{self.nome} ({status}) - {self.whatsapp}"

    class Meta:
        verbose_name = "Perfil do Cliente"
        verbose_name_plural = "Perfil dos Clientes"


class TipoReserva(models.Model):
    descricao = models.CharField(max_length=50, unique=True, verbose_name="Descrição")

    def clean(self):
        if self.descricao:
            descricao_upper = self.descricao.upper()
            exists = TipoReserva.objects.filter(descricao__iexact=descricao_upper).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError({'descricao': f"O tipo '{descricao_upper}' já está cadastrado!"})

    def save(self, *args, **kwargs):
        if self.descricao:
            self.descricao = str(self.descricao).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Tipo de Reserva"
        verbose_name_plural = "Tipos de Reserva"


class Mesa(models.Model):
    descricao = models.CharField(max_length=50, unique=True, verbose_name="Identificação da Mesa")
    capacidade = models.IntegerField(verbose_name="Capacidade de Pessoas")

    def clean(self):
        if self.descricao:
            descricao_upper = self.descricao.upper()
            exists = Mesa.objects.filter(descricao__iexact=descricao_upper).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError({'descricao': f"A mesa '{descricao_upper}' já está cadastrada!"})    

    def save(self, *args, **kwargs):
        if self.descricao:
            self.descricao = str(self.descricao).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descricao} (Capacidade: {self.capacidade})"

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"


class PedidoReserva(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    # Apenas os Clientes ativos aparecem na lista)
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT, 
        limit_choices_to={'ativo': True},
        related_name='pedidos',
        verbose_name="Cliente"
    )
    
    data = models.DateField(default=date.today, verbose_name="Data da Reserva")
    numero_pessoas = models.IntegerField(verbose_name="Nº de Pessoas")
    tipo_reserva = models.ForeignKey(TipoReserva, on_delete=models.PROTECT, verbose_name="Tipo da Reserva")
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, verbose_name="Mesa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmado')
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Colaborador continua sendo o User logado que fez o registro
    colaborador = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='atendimentos_realizados',
        verbose_name="Atendido por"
    )

    def clean(self):
        if self.mesa and self.data and self.tipo_reserva:
            ocupada = PedidoReserva.objects.filter(
                data=self.data,
                tipo_reserva=self.tipo_reserva,
                mesa=self.mesa,
                status='confirmado'
            ).exclude(id=self.id).exists()
            
            if ocupada:
                raise ValidationError(f"A {self.mesa} já está reservada para {self.tipo_reserva} nesta data!")

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Pedido de Reserva"
        verbose_name_plural = "Pedidos de Reserva"
        ordering = ['-data']

