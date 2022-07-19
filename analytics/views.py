import base64
import io
from django.shortcuts import render
from django.http import HttpResponse
import urllib
import pandas as pd

from .utils import programas, andreNotebook

def index(request):
    dados = programas.load()
    return render(request, 'analytics/index.html', {'dados': dados })

def grafico_teste(request):
    x, y = andreNotebook.grafico_defesas()
    chart = andreNotebook.get_plot_defesas(x,y)

    context = {'chart' : chart}

    return render(request, 'analytics/andre.html', context)