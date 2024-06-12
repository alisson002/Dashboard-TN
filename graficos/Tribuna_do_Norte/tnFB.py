import pygal
import pandas as pd
import streamlit as st
from datetime import datetime
import csv
import plotly
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

def transformaData_final(data):
    return (pd.to_datetime(data)-pd.DateOffset(days=1)).strftime('%d-%m-%Y')

def transformaData_inicio(data):
    return (pd.to_datetime(data)).strftime('%d-%m-%Y')

final_alcanceFB = encontrar_frase_em_csv_meta('tabelas/meta/Alcance.csv', 'Alcance do Instagram')

dados_FB_alcance = pd.read_csv('tabelas/meta/Alcance.csv',skiprows=2,encoding='utf-16',nrows=final_alcanceFB-5)
#dados_FB_alcance = pd.read_csv('tabelas/meta/AlcanceFB.csv',encoding='utf-16')

final_visitasFB = encontrar_frase_em_csv_meta('tabelas/meta/Visitas.csv', 'Visitas ao perfil do Instagram')

visitasFB = pd.read_csv('tabelas/meta/Visitas.csv', skiprows=2, encoding='utf-16', nrows=final_visitasFB-5)

final_seguidoresFB = encontrar_frase_em_csv_meta('tabelas/meta/Seguidores.csv', 'Seguidores no Instagram')

seguidoresFB = pd.read_csv('tabelas/meta/Seguidores.csv', skiprows=2, encoding='utf-16', nrows=final_seguidoresFB-5)


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
    #FILTRO ALCANCE
    dados_FB_alcance_FILTRADAS = dados_FB_alcance.copy()
    
    dados_FB_alcance_FILTRADAS = dados_FB_alcance_FILTRADAS.loc[(dados_FB_alcance_FILTRADAS['Data']>start_date) & (dados_FB_alcance_FILTRADAS['Data']<end_date)]
    
    dados_FB_alcance_ANTERIOR = dados_FB_alcance.copy()
    
    dados_FB_alcance_ANTERIOR = dados_FB_alcance_ANTERIOR.loc[(dados_FB_alcance_ANTERIOR['Data']>start_date_b4) & (dados_FB_alcance_ANTERIOR['Data']<end_date_b4)]

    #FILTRO VISITAS
    visitasFB_FILTRADO = visitasFB.copy()

    visitasFB_FILTRADO = visitasFB_FILTRADO.loc[(visitasFB_FILTRADO['Data']>start_date) & (visitasFB_FILTRADO['Data']<end_date)]

    visitasFB_ANTERIOR = visitasFB.copy()

    visitasFB_ANTERIOR = visitasFB_ANTERIOR.loc[(visitasFB_ANTERIOR['Data']>start_date_b4) & (visitasFB_ANTERIOR['Data']<end_date_b4)]

    #FILTRO SEGUIDOORES
    seguidoresFB_FILTRADO = seguidoresFB.copy()

    seguidoresFB_FILTRADO = seguidoresFB_FILTRADO.loc[(seguidoresFB_FILTRADO['Data']>start_date) & (seguidoresFB_FILTRADO['Data']<end_date)]

    seguidoresFB_ANTERIOR = seguidoresFB.copy()

    seguidoresFB_ANTERIOR = seguidoresFB_ANTERIOR.loc[(seguidoresFB_ANTERIOR['Data']>start_date_b4) & (seguidoresFB_ANTERIOR['Data']<end_date_b4)]

    
    return dados_FB_alcance_ANTERIOR,dados_FB_alcance_FILTRADAS,visitasFB_ANTERIOR,visitasFB_FILTRADO,seguidoresFB_ANTERIOR,seguidoresFB_FILTRADO

inicio_alcanceIG = encontrar_frase_em_csv_meta('tabelas/meta/Alcance.csv', 'Alcance do Instagram')

alcanceIG = pd.read_csv('tabelas/meta/Alcance.csv', skiprows=inicio_alcanceIG, encoding='utf-16')

inicio_visitasIG = encontrar_frase_em_csv_meta('tabelas/meta/Visitas.csv', 'Visitas ao perfil do Instagram')

visitasIG = pd.read_csv('tabelas/meta/Alcance.csv', skiprows=inicio_visitasIG, encoding='utf-16')

inicio_seguidoresIG = encontrar_frase_em_csv_meta('tabelas/meta/Seguidores.csv', 'Seguidores no Instagram')

seguidoresIG = pd.read_csv('tabelas/meta/Seguidores.csv', skiprows=inicio_seguidoresIG, encoding='utf-16')

def filtrosDatasINSTAGRAM(start_date, end_date, start_date_b4, end_date_b4):
    #FILTRO ALCANCE
    dados_IG_alcance_FILTRADAS = alcanceIG.copy()
    
    dados_IG_alcance_FILTRADAS = dados_IG_alcance_FILTRADAS.loc[(dados_IG_alcance_FILTRADAS['Data']>start_date) & (dados_IG_alcance_FILTRADAS['Data']<end_date)]
    
    dados_IG_alcance_ANTERIOR = alcanceIG.copy()
    
    dados_IG_alcance_ANTERIOR = dados_IG_alcance_ANTERIOR.loc[(dados_IG_alcance_ANTERIOR['Data']>start_date_b4) & (dados_IG_alcance_ANTERIOR['Data']<end_date_b4)]

    #FILTRO VISITAS
    visitasIG_FILTRADO = visitasIG.copy()

    visitasIG_FILTRADO = visitasIG_FILTRADO.loc[(visitasIG_FILTRADO['Data']>start_date) & (visitasIG_FILTRADO['Data']<end_date)]

    visitasIG_ANTERIOR = visitasIG.copy()

    visitasIG_ANTERIOR = visitasIG_ANTERIOR.loc[(visitasIG_ANTERIOR['Data']>start_date_b4) & (visitasIG_ANTERIOR['Data']<end_date_b4)]

    #FILTRO SEGUIDOORES
    seguidoresIG_FILTRADO = seguidoresIG.copy()

    seguidoresIG_FILTRADO = seguidoresIG_FILTRADO.loc[(seguidoresIG_FILTRADO['Data']>start_date) & (seguidoresIG_FILTRADO['Data']<end_date)]

    seguidoresIG_ANTERIOR = seguidoresIG.copy()

    seguidoresIG_ANTERIOR = seguidoresIG_ANTERIOR.loc[(seguidoresIG_ANTERIOR['Data']>start_date_b4) & (seguidoresIG_ANTERIOR['Data']<end_date_b4)]

    
    return dados_IG_alcance_ANTERIOR,dados_IG_alcance_FILTRADAS,visitasIG_ANTERIOR,visitasIG_FILTRADO,seguidoresIG_ANTERIOR,seguidoresIG_FILTRADO

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
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=dados_FB_alcance_FILTRADAS['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#2f55a4')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=dados_FB_alcance_ANTERIOR['Dia'],
    y=dados_FB_alcance_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
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

def FB_alcance_cumsum(dados_FB_alcance_ANTERIOR, dados_FB_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4):
    
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
    y=dados_FB_alcance_FILTRADAS['Primary'].cumsum(),
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=dados_FB_alcance_FILTRADAS['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#2f55a4')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=dados_FB_alcance_ANTERIOR['Dia'],
    y=dados_FB_alcance_ANTERIOR['Primary'].cumsum(),
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
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

def FB_visitas(visitasFB_ANTERIOR, visitasFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    visitasFB_FILTRADO['Data'] = pd.to_datetime(visitasFB_FILTRADO['Data'])
    visitasFB_ANTERIOR['Data'] = pd.to_datetime(visitasFB_ANTERIOR['Data'])

    # Manter as datas originais
    visitasFB_FILTRADO['Data_Original'] = visitasFB_FILTRADO['Data']
    visitasFB_ANTERIOR['Data_Original'] = visitasFB_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = visitasFB_FILTRADO['Data'].min() - visitasFB_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    visitasFB_ANTERIOR['Data'] = visitasFB_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    visitasFB_FILTRADO['Dia'] = range(1, len(visitasFB_FILTRADO) + 1)
    visitasFB_ANTERIOR['Dia'] = range(1, len(visitasFB_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=visitasFB_FILTRADO['Dia'],
    y=visitasFB_FILTRADO['Primary'],
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=visitasFB_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#3b5998')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=visitasFB_ANTERIOR['Dia'],
    y=visitasFB_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=visitasFB_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#7B94CC')
    ))

    # Configura o layout
    fig.update_layout(
    title='Visitas do FB - Comparação de Períodos',
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

def FB_visitas_cumsum(visitasFB_ANTERIOR, visitasFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    visitasFB_FILTRADO['Data'] = pd.to_datetime(visitasFB_FILTRADO['Data'])
    visitasFB_ANTERIOR['Data'] = pd.to_datetime(visitasFB_ANTERIOR['Data'])

    # Manter as datas originais
    visitasFB_FILTRADO['Data_Original'] = visitasFB_FILTRADO['Data']
    visitasFB_ANTERIOR['Data_Original'] = visitasFB_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = visitasFB_FILTRADO['Data'].min() - visitasFB_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    visitasFB_ANTERIOR['Data'] = visitasFB_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    visitasFB_FILTRADO['Dia'] = range(1, len(visitasFB_FILTRADO) + 1)
    visitasFB_ANTERIOR['Dia'] = range(1, len(visitasFB_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=visitasFB_FILTRADO['Dia'],
    y=visitasFB_FILTRADO['Primary'].cumsum(),
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=visitasFB_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#3b5998')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=visitasFB_ANTERIOR['Dia'],
    y=visitasFB_ANTERIOR['Primary'].cumsum(),
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=visitasFB_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#7B94CC')
    ))

    # Configura o layout
    fig.update_layout(
    title='Visitas do FB - Comparação de Períodos',
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

def FB_seguidores(seguidoresFB_ANTERIOR, seguidoresFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    seguidoresFB_FILTRADO['Data'] = pd.to_datetime(seguidoresFB_FILTRADO['Data'])
    seguidoresFB_ANTERIOR['Data'] = pd.to_datetime(seguidoresFB_ANTERIOR['Data'])

    # Manter as datas originais
    seguidoresFB_FILTRADO['Data_Original'] = seguidoresFB_FILTRADO['Data']
    seguidoresFB_ANTERIOR['Data_Original'] = seguidoresFB_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = seguidoresFB_FILTRADO['Data'].min() - seguidoresFB_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    seguidoresFB_ANTERIOR['Data'] = seguidoresFB_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    seguidoresFB_FILTRADO['Dia'] = range(1, len(seguidoresFB_FILTRADO) + 1)
    seguidoresFB_ANTERIOR['Dia'] = range(1, len(seguidoresFB_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=seguidoresFB_FILTRADO['Dia'],
    y=seguidoresFB_FILTRADO['Primary'],
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=seguidoresFB_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#5874af')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=seguidoresFB_ANTERIOR['Dia'],
    y=seguidoresFB_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=seguidoresFB_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#ACB9D7')
    ))

    # Configura o layout
    fig.update_layout(
    title='Seguidores do FB - Comparação de Períodos',
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

def FB_seguidores_cumsum(seguidoresFB_ANTERIOR, seguidoresFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    seguidoresFB_FILTRADO['Data'] = pd.to_datetime(seguidoresFB_FILTRADO['Data'])
    seguidoresFB_ANTERIOR['Data'] = pd.to_datetime(seguidoresFB_ANTERIOR['Data'])

    # Manter as datas originais
    seguidoresFB_FILTRADO['Data_Original'] = seguidoresFB_FILTRADO['Data']
    seguidoresFB_ANTERIOR['Data_Original'] = seguidoresFB_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = seguidoresFB_FILTRADO['Data'].min() - seguidoresFB_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    seguidoresFB_ANTERIOR['Data'] = seguidoresFB_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    seguidoresFB_FILTRADO['Dia'] = range(1, len(seguidoresFB_FILTRADO) + 1)
    seguidoresFB_ANTERIOR['Dia'] = range(1, len(seguidoresFB_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=seguidoresFB_FILTRADO['Dia'],
    y=seguidoresFB_FILTRADO['Primary'].cumsum(),
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=seguidoresFB_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#5874af')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=seguidoresFB_ANTERIOR['Dia'],
    y=seguidoresFB_ANTERIOR['Primary'].cumsum(),
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=seguidoresFB_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#ACB9D7')
    ))

    # Configura o layout
    fig.update_layout(
    title='Seguidores do FB - Comparação de Períodos',
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

def IG_alcance(dados_IG_alcance_ANTERIOR, dados_IG_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    dados_IG_alcance_FILTRADAS['Data'] = pd.to_datetime(dados_IG_alcance_FILTRADAS['Data'])
    dados_IG_alcance_ANTERIOR['Data'] = pd.to_datetime(dados_IG_alcance_ANTERIOR['Data'])

    # Manter as datas originais
    dados_IG_alcance_FILTRADAS['Data_Original'] = dados_IG_alcance_FILTRADAS['Data']
    dados_IG_alcance_ANTERIOR['Data_Original'] = dados_IG_alcance_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = dados_IG_alcance_FILTRADAS['Data'].min() - dados_IG_alcance_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    dados_IG_alcance_ANTERIOR['Data'] = dados_IG_alcance_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    dados_IG_alcance_FILTRADAS['Dia'] = range(1, len(dados_IG_alcance_FILTRADAS) + 1)
    dados_IG_alcance_ANTERIOR['Dia'] = range(1, len(dados_IG_alcance_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=dados_IG_alcance_FILTRADAS['Dia'],
    y=dados_IG_alcance_FILTRADAS['Primary'],
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=dados_IG_alcance_FILTRADAS['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#FCAF45')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=dados_IG_alcance_ANTERIOR['Dia'],
    y=dados_IG_alcance_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=dados_IG_alcance_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#FDCC86')
    ))

    # Configura o layout
    fig.update_layout(
    title='Alcance do IG - Comparação de Períodos',
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

def IG_alcance_cumsum(dados_IG_alcance_ANTERIOR, dados_IG_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    dados_IG_alcance_FILTRADAS['Data'] = pd.to_datetime(dados_IG_alcance_FILTRADAS['Data'])
    dados_IG_alcance_ANTERIOR['Data'] = pd.to_datetime(dados_IG_alcance_ANTERIOR['Data'])

    # Manter as datas originais
    dados_IG_alcance_FILTRADAS['Data_Original'] = dados_IG_alcance_FILTRADAS['Data']
    dados_IG_alcance_ANTERIOR['Data_Original'] = dados_IG_alcance_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = dados_IG_alcance_FILTRADAS['Data'].min() - dados_IG_alcance_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    dados_IG_alcance_ANTERIOR['Data'] = dados_IG_alcance_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    dados_IG_alcance_FILTRADAS['Dia'] = range(1, len(dados_IG_alcance_FILTRADAS) + 1)
    dados_IG_alcance_ANTERIOR['Dia'] = range(1, len(dados_IG_alcance_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=dados_IG_alcance_FILTRADAS['Dia'],
    y=dados_IG_alcance_FILTRADAS['Primary'].cumsum(),
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=dados_IG_alcance_FILTRADAS['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#FCAF45')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=dados_IG_alcance_ANTERIOR['Dia'],
    y=dados_IG_alcance_ANTERIOR['Primary'].cumsum(),
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=dados_IG_alcance_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#FDCC86')
    ))

    # Configura o layout
    fig.update_layout(
    title='Alcance do IG - Comparação de Períodos',
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

def IG_visitas(visitasIG_ANTERIOR, visitasIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    visitasIG_FILTRADO['Data'] = pd.to_datetime(visitasIG_FILTRADO['Data'])
    visitasIG_ANTERIOR['Data'] = pd.to_datetime(visitasIG_ANTERIOR['Data'])

    # Manter as datas originais
    visitasIG_FILTRADO['Data_Original'] = visitasIG_FILTRADO['Data']
    visitasIG_ANTERIOR['Data_Original'] = visitasIG_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = visitasIG_FILTRADO['Data'].min() - visitasIG_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    visitasIG_ANTERIOR['Data'] = visitasIG_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    visitasIG_FILTRADO['Dia'] = range(1, len(visitasIG_FILTRADO) + 1)
    visitasIG_ANTERIOR['Dia'] = range(1, len(visitasIG_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=visitasIG_FILTRADO['Dia'],
    y=visitasIG_FILTRADO['Primary'],
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=visitasIG_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#E1306C')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=visitasIG_ANTERIOR['Dia'],
    y=visitasIG_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=visitasIG_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#EB7099')
    ))

    # Configura o layout
    fig.update_layout(
    title='Visitas do IG - Comparação de Períodos',
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

def IG_visitas_cumsum(visitasIG_ANTERIOR, visitasIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    visitasIG_FILTRADO['Data'] = pd.to_datetime(visitasIG_FILTRADO['Data'])
    visitasIG_ANTERIOR['Data'] = pd.to_datetime(visitasIG_ANTERIOR['Data'])

    # Manter as datas originais
    visitasIG_FILTRADO['Data_Original'] = visitasIG_FILTRADO['Data']
    visitasIG_ANTERIOR['Data_Original'] = visitasIG_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = visitasIG_FILTRADO['Data'].min() - visitasIG_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    visitasIG_ANTERIOR['Data'] = visitasIG_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    visitasIG_FILTRADO['Dia'] = range(1, len(visitasIG_FILTRADO) + 1)
    visitasIG_ANTERIOR['Dia'] = range(1, len(visitasIG_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=visitasIG_FILTRADO['Dia'],
    y=visitasIG_FILTRADO['Primary'].cumsum(),
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=visitasIG_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#E1306C')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=visitasIG_ANTERIOR['Dia'],
    y=visitasIG_ANTERIOR['Primary'].cumsum(),
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=visitasIG_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#EB7099')
    ))

    # Configura o layout
    fig.update_layout(
    title='Visitas do IG - Comparação de Períodos',
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

def IG_seguidores(seguidoresIG_ANTERIOR, seguidoresIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    seguidoresIG_FILTRADO['Data'] = pd.to_datetime(seguidoresIG_FILTRADO['Data'])
    seguidoresIG_ANTERIOR['Data'] = pd.to_datetime(seguidoresIG_ANTERIOR['Data'])

    # Manter as datas originais
    seguidoresIG_FILTRADO['Data_Original'] = seguidoresIG_FILTRADO['Data']
    seguidoresIG_ANTERIOR['Data_Original'] = seguidoresIG_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = seguidoresIG_FILTRADO['Data'].min() - seguidoresIG_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    seguidoresIG_ANTERIOR['Data'] = seguidoresIG_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    seguidoresIG_FILTRADO['Dia'] = range(1, len(seguidoresIG_FILTRADO) + 1)
    seguidoresIG_ANTERIOR['Dia'] = range(1, len(seguidoresIG_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=seguidoresIG_FILTRADO['Dia'],
    y=seguidoresIG_FILTRADO['Primary'],
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=seguidoresIG_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#833AB4')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=seguidoresIG_ANTERIOR['Dia'],
    y=seguidoresIG_ANTERIOR['Primary'],
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=seguidoresIG_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#B684D7')
    ))

    # Configura o layout
    fig.update_layout(
    title='Seguidores do IG - Comparação de Períodos',
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

def IG_seguidores_cumsum(seguidoresIG_ANTERIOR, seguidoresIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4):
    
    # Supor que 'Data' é a coluna de datas e que estas estão no tipo datetime
    seguidoresIG_FILTRADO['Data'] = pd.to_datetime(seguidoresIG_FILTRADO['Data'])
    seguidoresIG_ANTERIOR['Data'] = pd.to_datetime(seguidoresIG_ANTERIOR['Data'])

    # Manter as datas originais
    seguidoresIG_FILTRADO['Data_Original'] = seguidoresIG_FILTRADO['Data']
    seguidoresIG_ANTERIOR['Data_Original'] = seguidoresIG_ANTERIOR['Data']

    # Calcular a diferença de dias entre o início dos dois períodos
    delta = seguidoresIG_FILTRADO['Data'].min() - seguidoresIG_ANTERIOR['Data'].min()

    # Ajustar as datas do período anterior para sobrepor ao período atual
    seguidoresIG_ANTERIOR['Data'] = seguidoresIG_ANTERIOR['Data'] + delta

    # Criar a coluna de sequência de números
    seguidoresIG_FILTRADO['Dia'] = range(1, len(seguidoresIG_FILTRADO) + 1)
    seguidoresIG_ANTERIOR['Dia'] = range(1, len(seguidoresIG_ANTERIOR) + 1)

    # Cria a figura
    fig = go.Figure()

    # Adiciona a linha do período atual
    fig.add_trace(go.Scatter(
    x=seguidoresIG_FILTRADO['Dia'],
    y=seguidoresIG_FILTRADO['Primary'].cumsum(),
    mode='lines+markers',
    name=f'Selecionado: {transformaData_inicio(start_date)} a {transformaData_final(end_date)}',
    text=seguidoresIG_FILTRADO['Data_Original'].dt.strftime('%Y-%m-%d'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#833AB4')
    ))

    # Adiciona a linha do período anterior
    fig.add_trace(go.Scatter(
    x=seguidoresIG_ANTERIOR['Dia'],
    y=seguidoresIG_ANTERIOR['Primary'].cumsum(),
    mode='lines+markers',
    name=f"Anterior: {start_date_b4.strftime('%d-%m-%Y')} a {(end_date_b4 - pd.DateOffset(days=1)).strftime('%d-%m-%Y')}",
    text=seguidoresIG_ANTERIOR['Data_Original'].dt.strftime('%d-%m-%Y'),
    hovertemplate='<br>Data Original: %{text}<br>Valor: %{y}',
    line=dict(color='#B684D7')
    ))

    # Configura o layout
    fig.update_layout(
    title='Seguidores do IG - Comparação de Períodos',
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