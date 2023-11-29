import pygal
import pandas as pd
import streamlit as st

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
# Recebe as colunas 'editoria' e 'freq_edi' do df df_editorias_impresso
noticias_edi = df_editorias_impresso[['editoria','freq_edi']]

'''
GRÁFICOS DE ROSCA/PIZZA/MEIA PIZZA
'''
def noticiasPorEditoria():
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    for edi, freq in zip(noticias_edi['editoria'].unique(),noticias_edi['freq_edi'].unique()):
        pie_chart.add(edi, freq)
    svg = pie_chart.render_data_uri()
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''
DFs PARA O STREAMLIT
'''