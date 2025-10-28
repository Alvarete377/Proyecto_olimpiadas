from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView
from .models import Encuentros, Disciplinas, Pistas, Arbitros, Equipos, EncuentrosEquipos

# Vista basada en clase para listar encuentros (ListView)
class EncuentrosListView(ListView):
    model = Encuentros
    context_object_name = 'encuentros'

class EncuentrosDetailView(DetailView):
    model = Encuentros
    context_object_name = 'encuentro'
    
    def get_queryset(self):
        # Incluye todas las relaciones para optimizar consultas
        return Encuentros.objects.select_related(
            'idDis', 'idPis', 'idArb'
        ).prefetch_related(
            'encuentrosequipos_set__equipo'
        )