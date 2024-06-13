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

def formataNumero(numero):
    numero_formatado = '{:,}'.format(numero).replace(',', '.')
    return numero_formatado

def crescimento(atual, antigo):
    taxa = ((atual - antigo) / abs(antigo))
    if taxa > 0:
        return f'+{str(round((taxa*100),2)).replace('.', ',')}%'
    return f'{str(round(taxa*100,2)).replace('.', ',')}%'

def fbMetrics(dados_FB_alcance_ANTERIOR,dados_FB_alcance_FILTRADAS,visitasFB_ANTERIOR,visitasFB_FILTRADO,seguidoresFB_ANTERIOR,seguidoresFB_FILTRADO):
    
    total_igAlcance_selecionado = dados_FB_alcance_FILTRADAS['Primary'].sum()
    total_igAlcance_anterior = dados_FB_alcance_ANTERIOR['Primary'].sum()
    
    total_igVisitas_selecionado = visitasFB_FILTRADO['Primary'].sum()
    total_igVisitas_anterior = visitasFB_ANTERIOR['Primary'].sum()
    
    total_igSeguidores_selecionado = seguidoresFB_FILTRADO['Primary'].sum()
    total_igSeguidores_anterior = seguidoresFB_ANTERIOR['Primary'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Alcance", formataNumero(total_igAlcance_selecionado), crescimento(total_igAlcance_selecionado, total_igAlcance_anterior))
    col2.metric("Visitas", formataNumero(total_igVisitas_selecionado), crescimento(total_igVisitas_selecionado, total_igVisitas_anterior))
    col3.metric("Seguidores", formataNumero(total_igSeguidores_selecionado), crescimento(total_igSeguidores_selecionado, total_igSeguidores_anterior))
    st.write("Obs.: Os dados de **Alcance** exibidos aqui são cerca de 35% a 55% maiores que os exibidos diretamente na plataforma do Meta Busines. O motivo dos dados (apenas para a métrica de **Alcance**) serem tão diferentes talvez seja algum filtro que a Meta utiliza em sua exibição na plataforma, com os dados que são fornecidos para download/analises sendo, possívelmente, dados não tratados.")
    st.write("Pesquisei sobre essa diferença nos números, mas não foi informado nenhum motivo pela Meta.")
    st.write("Apesar das diferenças nos número, o gráfico segue um padrão de comportamento praticamente idêntico.")

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
