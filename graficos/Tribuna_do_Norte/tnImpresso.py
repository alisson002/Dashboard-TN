import pygal
import pandas as pd
import streamlit as st
from graficos.Tribuna_do_Norte import tnPortal

# Raios para os gráficos de rosca
raio_interno = 0.7
raio_half = 0.2

'''RECEBENDO OS DF'''
# Recebe a tabela com as notícias do impresso
# low_memory=False por a tabela ser grande
df_noticias_impresso = pd.read_csv('tabelas/impresso/dados_impresso.csv', low_memory=False)

# Recebe a tabela com as notícias do impresso
# low_memory=False por a tabela ser grande
df_editorias_impresso = pd.read_csv('tabelas/impresso/EDI_impresso.csv', low_memory=False)


'''
MANIPULANDO OS DFs
'''
reporteres_impresso = df_noticias_impresso['reporter_fotografo'].value_counts().reset_index().replace({'icarocesarcarvalho':'Icaro Cesar Carvalho', 'Fernandasouzajh': 'Fernanda Souza', 'adenilson_costa': 'Adenilson Costa'})

reporteres_impresso.columns = ['reporter_fotografo', 'freq']

# Recebe a coluna 'editoria' do df df_editorias_impresso
noticias_edi = df_editorias_impresso[['editoria', 'freq_edi']]

# Nesse caso vai sem ['editoria'] por ser um tipo Series e só ter aquela coluna
noticias_edi_uniRow = noticias_edi.drop_duplicates()

# Agrupa o DataFrame pelo valor da coluna 'editoria' e soma os valores em cada grupo
noticias_edi_somado = noticias_edi.drop_duplicates().groupby('editoria')['freq_edi'].sum().sort_values(ascending=False).reset_index()

# # Conta a frequência da linha 'Pauta sem editoria'
# freq_pauta_sem_editoria = df_editorias_impresso[df_editorias_impresso['editoria'] == 'Pauta sem editoria']['freq_edi'].sum()

# # Adiciona a linha 'Pauta sem editoria' ao DataFrame noticias_edi_somado
# noticias_edi_somado.loc[len(noticias_edi_somado)] = ['Pauta sem editoria', freq_pauta_sem_editoria]


'''
GRÁFICOS DE ROSCA/PIZZA/MEIA PIZZA
'''
# NATAL ESTÁ DUPLICADO
# RESOLVER O PROBLEMA E PEGAROS DOIS VALORES
# REMOVER OS NOMES DOS REPORTERES QUE ESTÃO COMO EDITORIA
def noticiasPorEditoria():
    
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    for edi, freq in zip(noticias_edi_somado['editoria'],noticias_edi_somado['freq_edi']):
        pie_chart.add(edi, freq)
    
    svg = pie_chart.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
def noticiasPorReporter():
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    for rep_fot,freq in zip(reporteres_impresso['reporter_fotografo'], reporteres_impresso['freq']):
        if rep_fot in ['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷']:
            continue
        else:
            pie_chart.add(rep_fot.title(), freq)
    
    svg = pie_chart.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos():
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    for rep_fot,freq in zip(reporteres_impresso['reporter_fotografo'], reporteres_impresso['freq']):
        if rep_fot in ['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷']:
            pie_chart.add(rep_fot.title(), freq)
        else:
            continue
    
    svg = pie_chart.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
'''
DFs PARA O STREAMLIT
'''

'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''

table_reporteres_impresso = reporteres_impresso.copy()

table_reporteres_impresso = table_reporteres_impresso.loc[~table_reporteres_impresso['reporter_fotografo'].isin(['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷'])]

table_reporteres_impresso['reporter_fotografo'] = table_reporteres_impresso['reporter_fotografo'].str.title()

# O método map substitui os valores que não estão no dicionário de mapeamento por None por padrão. Portanto, dessa forma fica comvários Nones no df

# table_reporteres_impresso['reporter_fotografo'] = table_reporteres_impresso['reporter_fotografo'].map({'icarocesarcarvalho':'Icaro Cesar Carvalho', 'Fernandasouzajh': 'Fernanda Souza'})

'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
table_fotografos = reporteres_impresso.copy()

table_fotografos = table_fotografos.loc[table_fotografos['reporter_fotografo'].isin(['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷'])]

table_fotografos['reporter_fotografo'] = table_fotografos['reporter_fotografo'].str.title()
