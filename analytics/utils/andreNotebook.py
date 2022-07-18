import numpy as np
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot_defesas(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(4,4))
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('Programas')
    plt.ylabel('Numero de programas')
    plt.tight_layout()

    graph = get_graph()
    return graph

def grafico_defesas():
    parametros = {"ano":2021, "codcur": ''}
    resultado = requests.get(url = 'https://dados.fflch.usp.br/api/defesas', params = parametros)
    dados = resultado.json()
    titulos = ['Mestrado', 'Doutorado', 'Doutorado direto']
    tabela = pd.DataFrame(dados)
    tipo = tabela['nivel'].value_counts()
    lista_temporaria_x = []
    lista_eixo_y = []

    for i in dados:
        j = i.get('nivel')
        lista_temporaria_x.append(j)
        lista_eixo_x = list(set(lista_temporaria_x))
        lista_eixo_x.reverse()

    x = 0
    while x < len(tipo):
        lista_eixo_y.append(tipo[x])
        x += 1  


    return titulos, lista_eixo_y