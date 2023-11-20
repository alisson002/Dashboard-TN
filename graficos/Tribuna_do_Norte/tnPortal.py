import pygal
import pandas as pd
import streamlit as st

# Recebe a tabela com as notícias
df_noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)

df_reporter = pd.read_csv('tabelas/noticias online/usuarios.csv')

# Manipulando as tabelas para fazer o gráfico dos reporters
ids_noticias = df_noticias['usu_id_fk']
ids_reporter = df_reporter[['usu_id', 'usu_nome']]
editoria = df_noticias[['usu_id_fk', 'edi_descricao']]

ids_noticias = ids_noticias.rename('usu_id')
editoria = editoria.rename(columns={'usu_id_fk': 'usu_id'})

merge_ids_reporterNoticias = pd.merge(ids_noticias, ids_reporter, on='usu_id', how='left')

reporter_unique = merge_ids_reporterNoticias['usu_nome'].unique()

merge2_ids_reporterNoticias_ediDescricao = pd.merge(editoria, ids_reporter, on='usu_id', how='left')


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
    
    # Recebe e 'escreve' o gráfico em svg na dashboard
    svg = pie_chart.render_data_uri()
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
    

def noticiasToTal():
    
    # Criar um gráfico de pizza
    pie_chart_total = pygal.Pie(inner_radius=0.2, half_pie=True)

    ativas = df_noticias['not_status'].value_counts()[1]
    pie_chart_total.add(f'Notícias ativas: {ativas}', ativas)
    desonline = df_noticias['not_status'].value_counts()[0]
    pie_chart_total.add(f'Notícias fora do "ar": {desonline}', desonline)
    
    
    
    svg1 = pie_chart_total.render_data_uri()
    
    # Renderizar o gráfico e incorporar no Streamlit
    st.markdown(f'<embed type="image/svg+xml" src="{svg1}" />', unsafe_allow_html=True)

def noticiasPorReporter():
    pie_chart_reporter = pygal.Pie(inner_radius=0.7)
    
    for item in reporter_unique:
        pie_chart_reporter.add(item, merge_ids_reporterNoticias['usu_nome'].value_counts()[item])
    
    # Recebe a o gráfico em svg
    svg3 = pie_chart_reporter.render_data_uri()
    
    # Renderizar o gráfico e incorporar no Streamlit
    st.markdown(f'<embed type="image/svg+xml" src="{svg3}" />', unsafe_allow_html=True)


def reporterPorEditoria():
    options3 = reporter_unique
    selected_option3 = st.selectbox("Selecione um reporter:", options3)
    
    pie_chart_repEdi = pygal.Pie(inner_radius=0.7)
    
    df_loc_repEdi = merge2_ids_reporterNoticias_ediDescricao.loc[merge2_ids_reporterNoticias_ediDescricao.usu_nome == f'{selected_option3}']
    
    df_repEdi =  df_loc_repEdi[['usu_nome', 'edi_descricao']]
    
    for item in df_repEdi['edi_descricao'].unique():
        pie_chart_repEdi.add(item, df_repEdi['edi_descricao'].value_counts()[item])
        
    svg4 = pie_chart_repEdi.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg4}" />', unsafe_allow_html=True)
    
    
    
    