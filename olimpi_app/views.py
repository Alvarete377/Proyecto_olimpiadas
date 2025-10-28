from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import ListView
from .models import Encuentros, Disciplinas, Pistas, Arbitros, Equipos, EncuentrosEquipos

# Vista basada en clase para listar encuentros (ListView)
class EncuentrosListView(ListView):
    model = Encuentros
    context_object_name = 'encuentros'  # ← ¡IMPORTANTE!

