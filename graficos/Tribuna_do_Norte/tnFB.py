# import pygal
# import pandas as pd
# import streamlit as st
# from datetime import datetime
# import csv

# def encontrar_frase_em_csv_meta(nome_arquivo, frase_procurada):
#     try:
#         with open(nome_arquivo, 'r', newline='', encoding='utf-16') as arquivo_csv:
#             leitor_csv = csv.reader(arquivo_csv)
            
#             for numero_linha, linha in enumerate(leitor_csv, start=1):
#                 if frase_procurada in linha:
#                     return numero_linha

#         # Se a frase não for encontrada em nenhuma linha
#         return -1

#     except FileNotFoundError:
#         print(f'O arquivo {nome_arquivo} não foi encontrado.')
#         return -1

# final_alcanceFB = encontrar_frase_em_csv_meta('tabelas/meta/alcance.csv', 'Alcance do Instagram')

# dados_FB_alcance = pd.read_csv('tabelas/meta/alcance.csv',skiprows=2,encoding='utf-16',nrows=final_alcanceFB-5)

# # Função para tentar múltiplos formatos
# def try_parsing_date(text):
#     for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"):
#         try:
#             return pd.to_datetime(text, format=fmt)
#         except ValueError:
#             continue
#     return pd.NaT

# # Recebendo dados de 01/01/2022 até o momento
# # alcance FB: 28/05/2022
# # alcance IG: 28/05/2022
# # visitas FB: 28/05/2022
# # visitas IG: 28/05/2022
# # seguidores FB: 01/01/2022
# # seguidores IG: 31/08/2023
# def filtrosDatasFACEBOOK(start_date, end_date, start_date_b4, end_date_b4):
#     dados_FB_alcance_FILTRADAS = dados_FB_alcance.copy()
    
#     dados_FB_alcance_FILTRADAS = dados_FB_alcance_FILTRADAS.loc[(dados_FB_alcance_FILTRADAS['Data']>start_date) & (dados_FB_alcance_FILTRADAS['Data']<end_date)]
    
#     dados_FB_alcance_ANTERIOR = dados_FB_alcance.copy()
    
#     dados_FB_alcance_ANTERIOR = dados_FB_alcance_ANTERIOR.loc[(dados_FB_alcance_ANTERIOR['Data']>start_date_b4) & (dados_FB_alcance_ANTERIOR['Data']<end_date_b4)]
    
#     return dados_FB_alcance_ANTERIOR,dados_FB_alcance_FILTRADAS

# def FB_alcance(dados_FB_alcance_ANTERIOR, dados_FB_alcance_FILTRADAS,periodo, start_date, end_date, start_date_b4, end_date_b4):
    
#     line_chart = pygal.Line()
#     line_chart.title = 'FB: Alcance'
#     line_chart.x_labels = map(str, range(1, (periodo.days)))
#     line_chart.add(f'Anterior: {start_date_b4} \n a \n{end_date_b4}',dados_FB_alcance_ANTERIOR['Primary'].cumsum())
#     line_chart.x_labels = map(lambda d: pd.to_datetime(d).strftime('%d-%m-%Y'), dados_FB_alcance_FILTRADAS['Data'])
#     line_chart.add(f'Período selecionado: {start_date} \n a \n{end_date}',dados_FB_alcance_FILTRADAS['Primary'].cumsum())
#     svg = line_chart.render_data_uri()
#     st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
    
    
    
#     xy_chart = pygal.XY(stroke=False)
#     xy_chart.title = 'Correlation'
    
#     # Obter os valores para o gráfico
#     dados_FB_alcance_FILTRADAS['Data'] = pd.to_datetime(dados_FB_alcance_FILTRADAS['Data'])
#     # data_points = list(zip(dados_FB_alcance_FILTRADAS['Data'].apply(lambda x: x.timestamp()), dados_FB_alcance_FILTRADAS['Primary'].cumsum()))
#     # xy_chart.add('A', data_points)
#     # Obter os valores para o gráfico
#     data_points = list(zip(dados_FB_alcance_FILTRADAS['Data'], dados_FB_alcance_FILTRADAS['Primary'].cumsum()))
#     # Adicionar os dados ao gráfico
#     xy_chart.add('A', [(data.timestamp(), value) for data, value in data_points])
#     # Customizar o formato do eixo x para datas legíveis
#     xy_chart.x_labels = [(data) for data, value in data_points]
#     xy_chart.x_labels_major = xy_chart.x_labels
#     xy_chart.show_x_labels = True
#     xy_chart.show_minor_x_labels = False
#     svg = xy_chart.render_data_uri()
#     st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
    
#     # TENTAR FAZER DO MEU JEITO MAS COM ESSE FOR DENTRO DA PARTE DOS DADOS TB, COM GRÁFICO DE LINHAS