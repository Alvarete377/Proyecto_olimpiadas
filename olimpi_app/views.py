from django.shortcuts import render
from django.http import HttpResponse
from .models import EncuentrosEquipos
from django.views.generic import ListView
# Create your views here.


def index(request):
    return HttpResponse("caca de vaca")

'''
class EncuentrosEquipos(ListView):
    model = 'EncuentrosEquipos'
'''