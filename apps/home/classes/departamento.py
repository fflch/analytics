import pandas as pd
from datetime import datetime
import requests


from apps.home.models import Departamento, Docente
from apps.home.classes.graficos import Grafico
from apps.home.utils import Utils

class DadosDepartamento():

    def __init__(self, sigla):
        self.sigla = sigla

    def tabela_docentes(self, api_programas, api_docentes):
        dados_programas = api_programas
        dados_docentes = api_docentes

        for i in dados_programas:
            if i['sigla'] == self.sigla:
                nome = i['nome']
                id = i['id_lattes_docentes']
                codset = i['codigo']

        docentes = [i for i in dados_docentes if int(i['codset']) == int(codset)]

        df = pd.DataFrame(docentes)

        id_lattes = df['id_lattes']
        resultado = {
            'df' : df,
            'id_lattes' : id_lattes,
            'nome' : nome,
            'id' : id
        }

        return resultado

    def pega_numero_docentes(self, api_programas, api_docentes):
        departamento = api_programas
        resultado = api_docentes

        total = 0
        ativos = 0
        aposentados = 0

        for i in resultado:
            if i.get('nomset') == departamento[0].get('nome') or i.get('nomset') == 'Lingüística':
                total += 1
                if i.get('sitatl') == 'A':
                    
                    ativos += 1
                elif i.get('sitatl') == 'P':
                    aposentados += 1

        resultado = {
            'titulo' : 'Numero de docentes',
            'texto_ativos' : { 
                                'total' : f'Total: {total}',
                                'ativos' : f'Ativos: {ativos}',
                                'aposentados' : f'Aposentados: {aposentados}'
                              },
            'numeros' : {
                'total' : total,
                'ativos' : ativos,
                'aposentados' : aposentados
            }}
        
        return resultado

    def plota_aposentados_ativos(self, api_programas, api_docentes):
        numero_docentes = self.pega_numero_docentes(api_programas, api_docentes)
        ativos_aposentados = [numero_docentes.get('numeros').get('ativos'), numero_docentes.get('numeros').get('aposentados')]
        tipos = ['Ativos', "Aposentados"]
        titulo = 'Percentual entre docentes aposentados e ativos'
        grafico = Grafico()
        grafico = grafico.grafico_pizza(values=ativos_aposentados, names=tipos,
                                        color=tipos, color_discrete_sequence=["#052e70", "#AFAFAF"], margin={'l': 20, 'r': 20, 't': 20, 'b': 20})

        resultado = {
            'titulo' : titulo,
            'grafico' : grafico
        }

        return resultado

    def plota_tipo_vinculo_docente(self, api_docentes):
        dados = api_docentes
        utils = Utils()
        departamento = utils.dptos_siglas.get(self.sigla)

        nomefnc = []
        for dado in dados:
            nomefnc.append(dado.get('api_docentes'))

        df = pd.DataFrame(nomefnc)
        df = df.loc[df['nomset'] == departamento]
        funcoes = df['nomefnc'].value_counts().index.to_list()
        dados = df['nomefnc'].value_counts().to_list()

        resultado = [] 
        x = 0
        for funcao in funcoes:
            resultado.append([funcao, dados[x]])
            x += 1

        return resultado

    def plota_prod_departamento(self, api_programas_docente_limpo):
        dados = api_programas_docente_limpo.get('api_programas_docente_limpo')
        df = pd.DataFrame(dados)
        somas = df['total_livros'].to_list(), df['total_artigos'].to_list(), df['total_capitulos'].to_list()

        x = 0
        lista_valores = []
        while x < len(somas):
            lista_valores_individuais = [int(i) for i in somas[x]]
            lista_valores.append(sum(lista_valores_individuais))
            x += 1

        resultado = [
            ["Livros", lista_valores[0]],
            ["Artigos", lista_valores[1]],
            ["Capitulos", lista_valores[2]]
        ]

        return resultado

    def tabela_trabalhos(self, api_pesquisa):
        dados = api_pesquisa

        df = pd.DataFrame(dados)
        df = pd.DataFrame(df[self.sigla])
        df = df.rename(index={
            'nome_departamento': "Nome do departamento",
            'ic_com_bolsa': "IC com bolsa",
            'ic_sem_bolsa': "IC sem bolsa",
            'pesquisadores_colab': 'Pesquisadores colaboradores ativos',
            'projetos_pesquisa': 'Projetos de pesquisa dos Docentes',
            'pesquisas_pos_doutorado_com_bolsa': 'Pesquisas pós doutorado com bolsa',
            'pesquisas_pos_doutorado_sem_bolsa': 'Pesquisas pós doutorado sem bolsa'
        })
        indices = df.index
        indices.to_list()
        valores = df[self.sigla].to_list()

        x = 0
        dados_tabela = []
        while x < len(indices):
            tabela_dados = [indices[x], valores[x]]
            dados_tabela.append(tabela_dados)
            x += 1

        headers = ['Nomes', 'Valores']

        resultado = {
            'headers' : headers,
            'tabelas' : dados_tabela
        }

        return resultado

    def plota_grafico_bolsa_sem(self, api_pesquisa_parametros):
        dados = api_pesquisa_parametros.get('api_pesquisa_parametros')

        anos = [i for i in range(int(datetime.now().year) - 6, datetime.now().year)]
        anos_str = [str(i) for i in anos]

        df = pd.DataFrame(dados)
        df = df.drop(['pesquisadores_colab', 'projetos_pesquisa'])
        labels = ["IC com bolsa", "IC sem bolsa", 'Pesquisas pós doutorado com bolsa', 'Pesquisas pós doutorado sem bolsa']
        df = df.values.tolist()
        x = 0
        for element in df:
            element.insert(0, labels[x])
            x += 1

        return df

    def plota_prod_serie_historica(self, api_programas_docente):
        dados = api_programas_docente.get('api_programas_docente')

        anos_int = [i for i in range(int(datetime.now().year) - 6, datetime.now().year)]
        anos = [str(i) for i in anos_int]

        lista_livros = []
        lista_artigos = []
        lista_capitulos = []
        x = 0
        while x < len(anos):

            z = 0
            while z < len(dados[x].get(anos[x])):
                lista_livros.append(dados[x].get(anos[x])[z].get('total_livros'))
                lista_artigos.append(dados[x].get(anos[x])[z].get('total_artigos'))
                lista_capitulos.append(dados[x].get(anos[x])[z].get('total_capitulos'))

                z += 1

            x += 1

        lista_livros = [int(i) for i in lista_livros]
        lista_artigos = [int(i) for i in lista_artigos]
        lista_capitulos = [int(i) for i in lista_capitulos]

        resultado_livros = []
        resultado_artigos = []
        resultado_capitulos = []

        g = 0
        f = len(dados[0].get(anos[0]))

        while f < len(lista_livros) + len(dados[0].get(anos[0])):

            resultado_livros.append(sum(lista_livros[g:f]))
            resultado_artigos.append(sum(lista_artigos[g:f]))
            resultado_capitulos.append(sum(lista_capitulos[g:f]))

            g = f
            f += len(dados[0].get(anos[0]))

        result = [
            ["Livros", *resultado_livros],
            ["Artigos", *resultado_artigos],
            ["Capitulos", *resultado_capitulos],
        ]

        return result

    def pega_programa_departamento(self):
        programas_dpto = Utils()
        programas_dpto = programas_dpto.pega_programas_departamento(self.sigla)
        programas_dpto = programas_dpto.get('programas')

        label = 'Programas'

        resultado = {
            'label' : label,
            'programas_dpto' : programas_dpto
        }

        return resultado
       
    def pega_tabela_defesas(self, api_defesas):
        utils = Utils()          

        resultado = []
        for defesa in api_defesas:
            codigo_departamento = defesa.get('codare')
            verifica_departamento = utils.pega_departamento_programa(codigo_departamento)

            if verifica_departamento.get('sigla') == self.sigla:
                    resultado.append(
                    [
                        defesa.get('titulo'),
                        defesa.get('nome'),
                        defesa.get('nivel'),
                        defesa.get('nomare'),
                        defesa.get('data'),
                    ]
                )

        resultado = {
            'titulo' : f'Defesas pós-graduação realizadas no ano de {datetime.now().year-1}',
            'headers' : ['Titulo', 'Nome', 'Nivel', 'Programa', 'Data'],
            'tabela' : resultado,
            'link_mestrado' : 'https://www.teses.usp.br/index.php?option=com_jumi&fileid=11&Itemid=76&lang=pt-br&filtro=',
            'link_doutorado' : 'https://www.teses.usp.br/index.php?option=com_jumi&fileid=12&Itemid=77&lang=pt-br&filtro='
        }

        return resultado

    def defesas_mestrado_doutorado(self, api_defesas):
        tipos = ['ME', 'DO', 'DD']

        x, y, z = 0, 0, 0
        nivel = []
        for defesa in api_defesas.get('api_defesas'):  

            if defesa.get('nivel') == 'ME':
                x += 1
            if defesa.get('nivel') == 'DO':
                y += 1
            if defesa.get('nivel') == 'DD':
                z += 1

        resultado = [
            ["Mestrado", x],
            ["Doutorado", y],
            ["Doutorado Direto", z]
        ]

        return resultado