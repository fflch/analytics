import base64
import io
from django.shortcuts import render
from django.http import HttpResponse
import urllib

from .utils import programas, grafico_defesas

def index(request):
    dados = programas.load()
    return render(request, 'analytics/index.html', {'dados': dados })

def calimaco(request):
    grafico = grafico_defesas.plot_grafico()
    return render(request, 'analytics/calimaco.html', {'grafico': grafico})