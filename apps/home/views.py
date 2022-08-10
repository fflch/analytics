from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render

import requests
import pandas as pd

from .utils import Docente, Departamento

def index(request):
    context = {
        'segment': 'index',
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))





def docente(request, sigla, parametro):
    docente = Docente(parametro, sigla)

    tabela = docente.tabela_orientandos()
    grafico_ori = docente.plota_pizza()
    grafico_artigos, grafico_titulo_artigos = docente.plota_grafico_historico_artigos()
    grafico_livros, grafico_titulo_livros = docente.plota_grafico_historico_livros()
    tabela_publi = docente.tabela_ultimas_publicacoes()
    caminho = docente.pega_caminho()

    docente = [
        {
            'nome' : docente.dados.get('nome'),
            'programa' : '',
            'departamento' : '',
            'link_lattes': 'http://lattes.cnpq.br/' + docente.dados.get('id_lattes')
        }
    ]


    grafico_pizza_titulo = [
        {
            'titulo' : 'Relação entre mestrandos e doutorandos'
        }
    ]
    

    tabela_header = [
        {
            'titulo' : 'Orientandos Ativos',
            'nome' : 'Nome',
            'nivel' : 'Nivel',
            'programa' : 'Programa'
        }
    ]

    tabela_publicacoes = [
        {
            'titulo' : 'Ultimas publicações',
            'titulo_trabalho' : 'Titulo',
            'ano' : 'Ano'
        }
    ]


    context = {
        'tabela_header' : tabela_header,
        'caminho' : caminho,
        'tabela' : tabela,
        'grafico_ori' : grafico_ori,
        'tabela_pu' : tabela_publi,
        'tabela_publicacoes' : tabela_publicacoes,
        'grafico_artigos' : grafico_artigos,
        'grafico_titulo_artigos' : grafico_titulo_artigos,
        'grafico_livros' : grafico_livros,
        'grafico_titulo_livros' : grafico_titulo_livros,
        'grafico_pizza_titulo' : grafico_pizza_titulo,
        'docente' : docente,
        'sigla_departamento' : sigla
    }

    return render(request, 'home/docentes.html', context)


def docentes(request, sigla):

    docentes = Departamento(sigla)

    df, id_lattes, nome, id = docentes.tabela_docentes(sigla)

    caminho = [
        {
            'text' : nome,
            'url' : '/departamento/' + sigla
        }
    ]

    context = {
        'caminho' : caminho,
        'nome' : nome,
        'id_lattes' : id,
        'docentes' : docentes,
        'df' : df,
        'lattes_id' : id_lattes,
        'tabela' : 'docentes',
        'sigla_departamento' : sigla
    }

    return render(request, 'home/departamento.html', context)



def departamentos(request):



    return render(request, 'home/departamentos.html')


