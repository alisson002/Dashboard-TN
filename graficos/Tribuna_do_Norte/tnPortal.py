import pygal
import pandas as pd
import streamlit as st
from io import BytesIO
import base64  # Adicione esta linha


def noticiasPorEditoria():
    dados_Noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)

    editoriais_unicos = dados_Noticias['edi_descricao'].unique()

    pie_chart = pygal.Pie(inner_radius = 0.7)
    #pie_chart = pygal.Pie(inner_radius = 0.4, half_pie=True)
    pie_chart.title = "Notícias online"
    for item in editoriais_unicos:
        pie_chart.add(item, dados_Noticias['edi_descricao'].value_counts()[item])

    # svg = pie_chart.render()
    # render_svg(svg)
    svg = pie_chart.render_data_uri()

    # Exibindo o gráfico no Streamlit
    
    return svg
    
def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


