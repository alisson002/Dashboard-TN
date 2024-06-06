import pygal
import pandas as pd
import streamlit as st
from datetime import datetime
import csv
import plotly.graph_objects as go

def encontrar_frase_em_csv_meta(nome_arquivo, frase_procurada):
    try:
        with open(nome_arquivo, 'r', newline='', encoding='utf-16') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            
            for numero_linha, linha in enumerate(leitor_csv, start=1):
                if frase_procurada in linha:
                    return numero_linha

        # Se a frase não for encontrada em nenhuma linha
        return -1

    except FileNotFoundError:
        print(f'O arquivo {nome_arquivo} não foi encontrado.')
        return -1

# final_alcanceFB = encontrar_frase_em_csv_meta('tabelas/meta/alcance.csv', 'Alcance do Instagram')

#dados_FB_alcance = pd.read_csv('tabelas/meta/alcance.csv',skiprows=2,encoding='utf-16',nrows=final_alcanceFB-5)
dados_FB_alcance = pd.read_csv('tabelas/meta/AlcanceFB.csv',encoding='utf-16')

# Função para tentar múltiplos formatos
def try_parsing_date(text):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"):
        try:
            return pd.to_datetime(text, format=fmt)
        except ValueError:
            continue
    return pd.NaT

# Recebendo dados de 01/01/2022 até o momento
# alcance FB: 28/05/2022
# alcance IG: 28/05/2022
# visitas FB: 28/05/2022
# visitas IG: 28/05/2022
# seguidores FB: 01/01/2022
# seguidores IG: 31/08/2023
def filtrosDatasFACEBOOK(start_date, end_date, start_date_b4, end_date_b4):
    dados_FB_alcance_FILTRADAS = dados_FB_alcance.copy()
    
    dados_FB_alcance_FILTRADAS = dados_FB_alcance_FILTRADAS.loc[(dados_FB_alcance_FILTRADAS['Data']>start_date) & (dados_FB_alcance_FILTRADAS['Data']<end_date)]
    
    dados_FB_alcance_ANTERIOR = dados_FB_alcance.copy()
    
    dados_FB_alcance_ANTERIOR = dados_FB_alcance_ANTERIOR.loc[(dados_FB_alcance_ANTERIOR['Data']>start_date_b4) & (dados_FB_alcance_ANTERIOR['Data']<end_date_b4)]
    
    return dados_FB_alcance_ANTERIOR,dados_FB_alcance_FILTRADAS

def FB_alcance(dados_FB_alcance_ANTERIOR, dados_FB_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    dados_FB_alcance_FILTRADAS['Data'] = pd.to_datetime(dados_FB_alcance_FILTRADAS['Data'])
    dados_FB_alcance_ANTERIOR['Data'] = pd.to_datetime(dados_FB_alcance_ANTERIOR['Data'])

    # Manter as datas originais
    dados_FB_alcance_FILTRADAS['Data_Original'] = dados_FB_alcance_FILTRADAS['Data']
    dados_FB_alcance_ANTERIOR['Data_Original'] = dados_FB_alcance_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = dados_FB_alcance_FILTRADAS['Data'].min() - dados_FB_alcance_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    dados_FB_alcance_ANTERIOR['Data'] = dados_FB_alcance_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    dados_FB_alcance_FILTRADAS['Dia'] = range(1, len(dados_FB_alcance_FILTRADAS) + 1)
    dados_FB_alcance_ANTERIOR['Dia'] = range(1, len(dados_FB_alcance_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=dados_FB_alcance_FILTRADAS['Dia'],
    y=dados_FB_alcance_FILTRADAS['Primary'],
    mode='lines+markers',
    name=f'Selecionado: {start_date} a {end_date}',
    text=dados_FB_alcance_FILTRADAS['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#2f55a4')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=dados_FB_alcance_ANTERIOR['Dia'],
    y=dados_FB_alcance_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f'Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {end_date_b4.strftime('%d-%m-%Y')}',
    text=dados_FB_alcance_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#6184D1')
    ))

    # Configura o layout
    fig.update_layout(
    title='Alcance do FB - Comparação de Períodos',
    title_x=0.1,
    title_xanchor='left',
    title_y=0.85,
    xaxis_title='Dias',
    yaxis_title='Alcance',
    hovermode='x unified',
    yaxis=dict(tickformat='.'),
    legend=dict(x=1, y=1, xanchor='right', yanchor='bottom', font=dict(size=10))
    )
    
    st.plotly_chart(fig)