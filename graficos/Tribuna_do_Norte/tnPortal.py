import pygal
import pandas as pd
import streamlit as st
from io import BytesIO

def noticiasPorEditoria():
    dados_Noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)

    editoriais_unicos = dados_Noticias['edi_descricao'].unique()

    pie_chart = pygal.Pie(inner_radius = 0.7)
    #pie_chart = pygal.Pie(inner_radius = 0.4, half_pie=True)
    pie_chart.title = "Notícias online"
    for item in editoriais_unicos:
        pie_chart.add(item, dados_Noticias['edi_descricao'].value_counts()[item])

    pie_chart
