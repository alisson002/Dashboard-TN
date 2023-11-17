import pygal
import pandas as pd
import streamlit as st

# Recebe a tabela com as notícias
df_noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)

df_reporter = pd.read_csv('tabelas/noticias online/usuarios.csv')

# Manipulando as tabelas para fazer o gráfico dos reporters
ids_noticias = df_noticias['usu_id_fk']
ids_reporter = df_reporter[['usu_id', 'usu_nome']]

ids_noticias = ids_noticias.rename('usu_id')

merge_ids_reporterNoticias = pd.merge(ids_noticias, ids_reporter, on='usu_id', how='left')

reporter_unique = merge_ids_reporterNoticias['usu_nome'].unique()

def noticiasPorEditoria():
    # Recebe a lista de editoriais sem repetições
    editoriais_unicos = df_noticias['edi_descricao'].unique()

    # Cria o gráfico de rosca
    pie_chart = pygal.Pie(inner_radius = 0.7)
    
    # Titulo do gráfico
    pie_chart.title = "Notícias online"
    
    # Adiciona cada item no gráfico e seu respectivo valor
    for item in editoriais_unicos:
        pie_chart.add(item, df_noticias['edi_descricao'].value_counts()[item])
    
    # 'Escreve' o gráfico em svg na dashboard
    svg = pie_chart.render_data_uri()
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
    

def noticiasToTal():
    
    # Criar um gráfico de pizza
    pie_chart_total = pygal.Pie(inner_radius=0.2, half_pie=True)

    valor_total = df_noticias['edi_descricao'].count()
    pie_chart_total.add(f'Total: {valor_total}', valor_total)
    
    # Renderizar o gráfico e incorporar no Streamlit
    svg1 = pie_chart_total.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg1}" />', unsafe_allow_html=True)

def noticiasPorReporter():
    pie_chart_reporter = pygal.Pie(inner_radius=0.7)
    
    for item in reporter_unique:
        pie_chart_reporter.add(item, merge_ids_reporterNoticias['usu_nome'].value_counts()[item])
        
    svg3 = pie_chart_reporter.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg3}" />', unsafe_allow_html=True)


def reporterPorEditoria():
    options3 = reporter_unique
    selected_option3 = st.selectbox("Selecione um reporter:", options3)
    
    pie_chart_repEdi = pygal.Pie(inner_radius=0.7)
    
    