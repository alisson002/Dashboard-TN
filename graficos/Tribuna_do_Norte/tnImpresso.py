import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Raios para os gráficos de rosca
raio_interno = 0.7
raio_half = 0.2

# Função para tentar múltiplos formatos
def try_parsing_date(text):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"):
        try:
            return pd.to_datetime(text, format=fmt)
        except ValueError:
            continue
    return pd.NaT

'''RECEBENDO OS DF'''
# Recebe a tabela com as notícias do impresso
# low_memory=False por a tabela ser grande
df_noticias_impresso = pd.read_csv('tabelas/impresso/dados_impresso.csv', low_memory=False)
df_noticias_impresso['data'] = pd.to_datetime(df_noticias_impresso['data'].apply(try_parsing_date))#VERIFICAR

df_noticias_impresso = df_noticias_impresso.dropna(subset=['data']) #VERIFICAR

# Recebe a tabela com as notícias do impresso
# low_memory=False por a tabela ser grande
df_editorias_impresso = pd.read_csv('tabelas/impresso/EDI_impresso.csv', low_memory=False)
df_editorias_impresso['data'] = pd.to_datetime(df_editorias_impresso['data'].apply(try_parsing_date))#VERIFICAR

df_editorias_impresso = df_editorias_impresso.dropna(subset=['data'])#VERIFICAR
'''
MANIPULANDO OS DFs
'''
def filtroDeDatasImpresso(start_date, end_date):
    
    # Copia do df
    df_noticias_impresso_FILTRADAS = df_noticias_impresso.copy()

    # Selecionando dados de acordo com o periodo
    df_NOTICIAS_impresso_filtrado = df_noticias_impresso_FILTRADAS.loc[(df_noticias_impresso_FILTRADAS['data'] > start_date) & (df_noticias_impresso_FILTRADAS['data'] < end_date)]

    df_editorias_impresso_FILTRADAS = df_editorias_impresso.copy()

    df_editorias_impresso_filtrado = df_editorias_impresso_FILTRADAS.loc[(df_editorias_impresso_FILTRADAS['data'] > start_date) & (df_editorias_impresso_FILTRADAS['data'] < end_date)]

    # Recebe o Series df_noticias_impresso['reporter_fotografo'] do df
    # value_counts().reset_index() conta a freqeuncia de cada informação na coluna de reporter_fotografo e organiza em ordem decrescente de acordo com a coluna que conta a freqência de cada informação
    # .replace() renomea linhas da coluna reporter_fotografo
    reporteres_impresso = df_NOTICIAS_impresso_filtrado['reporter_fotografo'].value_counts().reset_index().replace({'icarocesarcarvalho':'Icaro Cesar Carvalho', 'Fernandasouzajh': 'Fernanda Souza', 'adenilson_costa': 'Adenilson Costa'})

    # Renomeando as colunas por conta do .reset_index().replace que criou uma nova com as contagens de cada linha de reporter_fotografo
    reporteres_impresso.columns = ['reporter_fotografo', 'freq']

    # Recebe a coluna 'editoria' do df df_editorias_impresso
    noticias_edi = df_editorias_impresso_filtrado[['editoria', 'freq_edi']]
    
    editorias_impresso = noticias_edi['editoria'].value_counts().reset_index()
    
    editorias_impresso.columns = ['editorias', 'freq']

    # Nesse caso vai sem ['editoria'] por ser um tipo Series e só ter aquela coluna
    noticias_edi_uniRow = noticias_edi.drop_duplicates()

    # Agrupa o DataFrame pelo valor da coluna 'editoria' e soma os valores em cada grupo
    noticias_edi_somado = noticias_edi.drop_duplicates().groupby('editoria')['freq_edi'].sum().reset_index()

    # Foi feita da forma acima por a API do Trello já tinha a contagem de cada editoria disponível e, nesse caso, o calor não estaria correto se fosse usado .value_counts()

    # conta as aparições da linha 'Pauta sem editoria' em editoria
    if 'Pauta sem editoria' in df_editorias_impresso_filtrado['editoria'].values:
        freq_pauta_sem_editoria = df_editorias_impresso_filtrado['editoria'].value_counts()['Pauta sem editoria']
    else:
        freq_pauta_sem_editoria = 0  # Ou qualquer valor padrão desejado

    # Adiciona uma nova linha com com a contagem de Pauta sem editoria
    noticias_edi_somado.loc[len(noticias_edi_somado)] = ['Pautas sem editorias', freq_pauta_sem_editoria]

    # Organiza em ordem decrescente de acordo com a coluna freq_edi
    noticias_edi_somado = noticias_edi_somado.sort_values(by= 'freq_edi',ascending=False)
    
    #remove a ultima linha
    noticias_edi_somado = noticias_edi_somado[:len(noticias_edi_somado)-1]
    
    return noticias_edi_somado, df_NOTICIAS_impresso_filtrado, reporteres_impresso, noticias_edi_somado, editorias_impresso

'''
GRÁFICOS DE ROSCA/PIZZA/MEIA PIZZA
'''

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorEditoria(editorias_impresso,df_NOTICIAS_impresso_filtrado):
    
    filtro = ['Bruno Vital', 'Líria Paz', 'Ícaro Carvalho', 'Felipe Salustino', 'Matteus Fernandes', 'Cláudio Oliveira', 'P.H.','MAGNUS NASCIMENTO', 'ALEX RÉGIS', 'ADRIANO ABREU']
    
    # Filtrando os dados
    # editorias_filtradas = [ed for ed in editorias_impresso['editorias'] if ed not in filtro]
    # frequencias_filtradas = [freq for ed, freq in zip(editorias_impresso['editorias'], editorias_impresso['freq']) if ed not in filtro]
    
    editorias_filtradas = editorias_impresso[~editorias_impresso['editorias'].isin(filtro)]
    
    fig = go.Figure(data=[go.Pie(labels=editorias_filtradas['editorias'], values=editorias_filtradas['freq'])])
    fig.update_traces(hole=0.3,textinfo='value+label', hoverinfo='percent+label',marker=dict(colors=px.colors.sequential.Blues, line=dict(color='#66533D', width=1.5)))
    
    # Atualizando o layout do gráfico
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),  # Remover margens desnecessárias
        height=800,  # Aumentar a altura do gráfico
        width=800,  # Aumentar a largura do gráfico
        legend=dict(
            orientation="v",  # Legenda horizontal
            yanchor="top",  # Ancorar ao fundo
            y=0,  # Posição vertical da legenda
            xanchor="left",  # Ancorar ao centro
            x=1  # Posição horizontal da legenda
        )
    )
    
    st.plotly_chart(fig)

'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
def noticiasPorReporter(reporteres_impresso):

    fig = go.Figure(data=[go.Pie(labels=reporteres_impresso['reporter_fotografo'], values=reporteres_impresso['freq'])])
    
    fig.update_traces(textinfo='value+label', hoverinfo='percent',marker=dict(colors=px.colors.sequential.Oranges, line=dict(color='#66533D', width=1.5)))
    
    st.plotly_chart(fig)

'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos(reporteres_impresso,editorias_impresso):
    
    filtro = ['MAGNUS NASCIMENTO', 'ALEX RÉGIS', 'ADRIANO ABREU']
    
    # Filtrando os dados
    # editorias_filtradas = [ed for ed in editorias_impresso['editorias'] if ed not in filtro]
    # frequencias_filtradas = [freq for ed, freq in zip(editorias_impresso['editorias'], editorias_impresso['freq']) if ed not in filtro]
    
    editorias_filtradas = editorias_impresso[editorias_impresso['editorias'].isin(filtro)]
    
    # Definindo as cores
    # As cores no gráfico de barras iniciam de baixo para cima, portando, quando o gráfico é colocado na ordem decrescente as cores não correspondem. A intenção do trecho abaixo é inverter a ordem das cores.
    num_barras = len(editorias_filtradas)
    cores = px.colors.sequential.Greens[::-1]  # Reverter a paleta de cores
    cores_personalizadas = [cores[i % len(cores)] for i in range(num_barras)]
    
    fig = go.Figure(data=[go.Pie(labels=editorias_filtradas['editorias'], values=editorias_filtradas['freq'])])
    fig.update_traces(hole=0.3,textinfo='value+label', hoverinfo='percent+label',marker=dict(colors=cores_personalizadas, line=dict(color='#66533D', width=1.5)))
    
    st.plotly_chart(fig)

'''
DFs PARA O STREAMLIT
'''
'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
# Recebe um cópia de noticias_edi_somado
def tableEdiImpresso(noticias_edi_somado):
    teble_ediImpresso = noticias_edi_somado.copy()

    # Recebe um Series com volores booleanos de acordo com as informação que quero ou não no df
    # Filtra as informação para não tem nomes de reporteres nas editorias
    condicao_para_manter = ~teble_ediImpresso['editorias'].isin(['Bruno Vital', 'Líria Paz', 'Ícaro Carvalho', 'Felipe Salustino', 'Matteus Fernandes', 'Cláudio Oliveira', 'P.H.'])

    # Df filtrado
    teble_ediImpresso = teble_ediImpresso[condicao_para_manter]
    
    return teble_ediImpresso

def tableRepImpresso(reporteres_impresso):
    '''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
    # Recebe um cópia de reporteres_impresso
    table_reporteres_impresso = reporteres_impresso.copy()

    # Filtra as informações para receber apenas os nomes dos reporteres
    # ~ nega a condição, fazendo com que ela funcione da forma inversa
    table_reporteres_impresso = table_reporteres_impresso.loc[~table_reporteres_impresso['reporter_fotografo'].isin(['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷', 'Líria Paz', 'Margareth Grilo', 'Isaac Lira', 'Fernanda Souza'])]

    # deixa as primeiras letras maiusculas
    table_reporteres_impresso['reporter_fotografo'] = table_reporteres_impresso['reporter_fotografo'].str.title()
    
    return table_reporteres_impresso

def tableFotografosImpresso(reporteres_impresso,editorias_impresso):
    '''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
    # Recebe um cópia de reporteres_impresso
    filtro = ['MAGNUS NASCIMENTO', 'ALEX RÉGIS', 'ADRIANO ABREU']
    
    # Filtrando os dados
    # editorias_filtradas = [ed for ed in editorias_impresso['editorias'] if ed not in filtro]
    # frequencias_filtradas = [freq for ed, freq in zip(editorias_impresso['editorias'], editorias_impresso['freq']) if ed not in filtro]
    
    editorias_filtradas = editorias_impresso[editorias_impresso['editorias'].isin(filtro)]
    
    return editorias_filtradas

'''GRÁFICOS DE BARRA'''

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorEditoria_bc(editorias_impresso,df_NOTICIAS_impresso_filtrado):
    
    filtro = ['Bruno Vital', 'Líria Paz', 'Ícaro Carvalho', 'Felipe Salustino', 'Matteus Fernandes', 'Cláudio Oliveira', 'P.H.', 'MAGNUS NASCIMENTO', 'ALEX RÉGIS', 'ADRIANO ABREU']
    
    # Filtrando os dados
    # editorias_filtradas = [ed for ed in editorias_impresso['editorias'] if ed not in filtro]
    # frequencias_filtradas = [freq for ed, freq in zip(editorias_impresso['editorias'], editorias_impresso['freq']) if ed not in filtro]
    
    editorias_filtradas = editorias_impresso[~editorias_impresso['editorias'].isin(filtro)]
    
    edit_impresso = editorias_filtradas.sort_values(by='freq', ascending=True)
    
    # Definindo as cores
    # As cores no gráfico de barras iniciam de baixo para cima, portando, quando o gráfico é colocado na ordem decrescente as cores não correspondem. A intenção do trecho abaixo é inverter a ordem das cores.
    num_barras = len(edit_impresso)
    cores = px.colors.sequential.Blues[::-1]  # Reverter a paleta de cores
    cores_personalizadas = [cores[i % len(cores)] for i in range(num_barras)]
    
    fig = go.Figure(data=[go.Bar(x=edit_impresso['freq'], y=edit_impresso['editorias'], orientation='h',text=edit_impresso['freq'])])
    
    fig.update_traces(marker_color=cores_personalizadas, marker_line_color='#66533D', marker_line_width=1.5)
    
    # Atualizando o layout do gráfico
    fig.update_layout(
        # margin=dict(t=0, b=0, l=0, r=0),  # Remover margens desnecessárias
        height=800,  # Aumentar a altura do gráfico
        width=800  # Aumentar a largura do gráfico
    )
    st.plotly_chart(fig)

'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
def noticiasPorReporter_bc(reporteres_impresso):
    
    reporteres_impresso = reporteres_impresso.sort_values(by='freq', ascending=True)
    
    fig = go.Figure(data=[go.Bar(x=reporteres_impresso['freq'], y=reporteres_impresso['reporter_fotografo'], orientation='h',text=reporteres_impresso['freq'])])
    
    fig.update_traces(marker_color=px.colors.sequential.Oranges, marker_line_color='#66533D', marker_line_width=1.5)
    
    st.plotly_chart(fig)

'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos_bc(reporteres_impresso,editorias_impresso):
    
    filtro = ['MAGNUS NASCIMENTO', 'ALEX RÉGIS', 'ADRIANO ABREU']
    
    # Filtrando os dados
    # editorias_filtradas = [ed for ed in editorias_impresso['editorias'] if ed not in filtro]
    # frequencias_filtradas = [freq for ed, freq in zip(editorias_impresso['editorias'], editorias_impresso['freq']) if ed not in filtro]
    
    editorias_filtradas = editorias_impresso[editorias_impresso['editorias'].isin(filtro)]
    
    edit_impresso = editorias_filtradas.sort_values(by='freq', ascending=True)
    
    # Definindo as cores
    # As cores no gráfico de barras iniciam de baixo para cima, portando, quando o gráfico é colocado na ordem decrescente as cores não correspondem. A intenção do trecho abaixo é inverter a ordem das cores.
    num_barras = len(edit_impresso)
    cores = px.colors.sequential.Greens[::-1]  # Reverter a paleta de cores
    cores_personalizadas = [cores[i % len(cores)] for i in range(num_barras)]
    
    fig = go.Figure(data=[go.Bar(x=edit_impresso['freq'], y=edit_impresso['editorias'], orientation='h',text=edit_impresso['freq'])])
    
    fig.update_traces(marker_color=cores_personalizadas, marker_line_color='#66533D', marker_line_width=1.5)
    
    # # Atualizando o layout do gráfico
    # fig.update_layout(
    #     # margin=dict(t=0, b=0, l=0, r=0),  # Remover margens desnecessárias
    #     height=800,  # Aumentar a altura do gráfico
    #     width=800  # Aumentar a largura do gráfico
    # )
    
    st.plotly_chart(fig)
