import requests
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go

parametros = {
    'ano': 2021,
    'codcur': ''
}

res = requests.get(url = 'https://dados.fflch.usp.br/api/defesas', params = parametros)

dados = res.json()

tabela = pd.DataFrame(dados)

group_dict = {'Ciências Sociais': ['Ciência Política', 'Ciência Social (Antropologia Social)', 'Sociologia'],
              
              'História': ['História Social', 'História Econômica'],

              'Geografia': ['Geografia (Geografia Humana)', 'Geografia (Geografia Física)'],

              'Letras': ['Filologia e Língua Portuguesa', 'Letras (Teoria Literária e Literatura Comparada)', 
                         'Letras (Língua Inglesa e Literaturas Inglesa e Norte-Americana)', 'Literatura Brasileira', 
                         'Lingüística', 'Humanidades, Direitos e Outras Legitimidades', 
                         'Letras (Estudos Lingüísticos, Literários e Tradutológicos em Francês)',
                         'Letras (Literatura Portuguesa)', 'Letras (Língua Espanhola e Literaturas Espanhola e Hispano-Americana)',
                         'Letras (Estudos Comparados de Literaturas de Língua Portuguesa)', 'Estudos Judaicos e Árabes',
                         'Letras (Língua, Literatura e Cultura Italianas)', 'Letras (Letras Clássicas)',
                         'Letras (Língua, Literatura e Cultura Japonesa)', 'Estudos da Tradução', 
                         'Mestrado Profissional em Letras em Rede Nacional', 'Letras (Língua e Literatura Alemã)',
                         'Literatura e Cultura Russa'],
              
              'Filosofia':['Filosofia']}

final = tabela.groupby(tabela.nomcur.map({v: k for k, lista in group_dict.items() for v in lista}).rename('Curso'))['defesa_id'].count().sort_values(ascending=False)

def plot_grafico():
    
    fig = go.Figure(
    data=[go.Bar(x=final.index, y=final.values)],
    layout_title_text="Defesas de Mestrado e Doutorado realizadas em 2021 separadas por curso")

    graph = plot(fig, output_type="div")

    return graph