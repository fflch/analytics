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
    count = 0
    count1 = 0
    count2 = 0
    titulos = ['Mestrado', 'Doutorado', 'Doutorado direto']

    for i in dados:
        if i['nivel'] == "ME":
            count += 1

        if i['nivel'] == "DO":
            count1 += 1

        if i['nivel'] == "DD":
            count2 += 1    

    valores_y = [count, count1, count2]


    return titulos, valores_y