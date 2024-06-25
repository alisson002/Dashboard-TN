import pygal
import pandas as pd
import streamlit as st
from graficos.Tribuna_do_Norte import tnPortal
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
    
    df_noticias_impresso_FILTRADAS = df_noticias_impresso.copy()

    #df_noticias_impresso_FILTRADAS['data'] = pd.to_datetime(df_noticias_impresso_FILTRADAS['data']).dt.strftime('%m-%d-%y')

    df_NOTICIAS_impresso_filtrado = df_noticias_impresso_FILTRADAS.loc[(df_noticias_impresso_FILTRADAS['data'] > start_date) & (df_noticias_impresso_FILTRADAS['data'] < end_date)]

    # Altera o formato da data para '%d-%m-%y' após o filtro
    #df_NOTICIAS_impresso_filtrado['data'] = pd.to_datetime(df_NOTICIAS_impresso_filtrado['data'], format='mixed').dt.strftime('%d-%m-%y')
    
    
    
    df_editorias_impresso_FILTRADAS = df_editorias_impresso.copy()

    #df_editorias_impresso_FILTRADAS['data'] = pd.to_datetime(df_editorias_impresso_FILTRADAS['data']).dt.strftime('%m-%d-%y')

    df_editorias_impresso_filtrado = df_editorias_impresso_FILTRADAS.loc[(df_editorias_impresso_FILTRADAS['data'] > start_date) & (df_editorias_impresso_FILTRADAS['data'] < end_date)]

    # Altera o formato da data para '%d-%m-%y' após o filtro
    #df_editorias_impresso_filtrado['data'] = pd.to_datetime(df_editorias_impresso_filtrado['data'], format='mixed').dt.strftime('%d-%m-%y')
    
    
    
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

    # conta as aparições da linha Pauta sem editoria em editoria
    if 'Pauta sem editoria' in df_editorias_impresso_filtrado['editoria'].values:
        freq_pauta_sem_editoria = df_editorias_impresso_filtrado['editoria'].value_counts()['Pauta sem editoria']
    else:
        freq_pauta_sem_editoria = 0  # Ou qualquer valor padrão desejado

    #freq_pauta_sem_editoria = df_editorias_impresso_filtrado['editoria'].value_counts()['Pauta sem editoria']

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
    
    # Cria o gráfico de rosca
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    # Adiciona as informações ao gráfico
    for edi, freq in zip(editorias_impresso['editorias'],editorias_impresso['freq']):
        
        # Filtra as informações para que nomes de reporteres não sejam adicionados as editorias
        if edi not in ['Bruno Vital', 'Líria Paz', 'Ícaro Carvalho', 'Felipe Salustino', 'Matteus Fernandes', 'Cláudio Oliveira', 'P.H.']:
            
            pie_chart.add(edi, freq)
            
    # pie_chart.add(f"Total: {df_NOTICIAS_impresso_filtrado['pauta'].drop_duplicates().count()}", 0)
    
        
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg = pie_chart.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
def noticiasPorReporter(reporteres_impresso):
    # # Cria o gráfico de rosca
    # pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    # # Adiciona as informações ao gráfico
    # for rep_fot,freq in zip(reporteres_impresso['reporter_fotografo'], reporteres_impresso['freq']):
        
    #     # Filtra as informações para separar reporteres e fotógrafos
    #     if rep_fot in ['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷', 'Líria Paz', 'Margareth Grilo', 'Isaac Lira', 'Fernanda Souza']:
    #         continue # Vai para a próxima iteração do loop
    #     else:
    #         pie_chart.add(rep_fot.title(), freq)
        
    # # pie_chart.add(f"total: {reporteres_impresso['freq'].sum()}", 0)
    
    
    # # Renderizaçãodo gráfico em formato SVG
    # # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    # svg = pie_chart.render_data_uri()
    
    # # Formatando uma string HTML usando f-strings
    # # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    # st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

    fig = go.Figure(data=[go.Pie(labels=reporteres_impresso['reporter_fotografo'], values=reporteres_impresso['freq'])])
    fig.update_traces(textinfo='value+label', hoverinfo='percent',marker=dict(colors=px.colors.sequential.Oranges, line=dict(color='#66533D', width=1.5)))
    st.plotly_chart(fig)

'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos(reporteres_impresso):
    # Cria o gráfico de rosca
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    # Adiciona as informações ao gráfico
    for rep_fot,freq in zip(reporteres_impresso['reporter_fotografo'], reporteres_impresso['freq']):
        
        # Filtra as informações para deixar somente os fotógrafos
        if rep_fot in ['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷']:
            pie_chart.add(rep_fot.title(), freq)
        else:
            continue # Vai para a próxima iteração do loop
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg = pie_chart.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro.
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

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

def tableFotografosImpresso(reporteres_impresso):
    '''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
    # Recebe um cópia de reporteres_impresso
    table_fotografos = reporteres_impresso.copy()

    # Filtra as informações para receber apenas os nomes dos fotógrafos
    # Mesma coisa do caso acima, mas sem ~
    table_fotografos = table_fotografos.loc[table_fotografos['reporter_fotografo'].isin(['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷'])]

    # Deixa as primeiras letras maiusculas
    table_fotografos['reporter_fotografo'] = table_fotografos['reporter_fotografo'].str.title()
    
    return table_fotografos

'''GRÁFICOS DE BARRA'''

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorEditoria_bc(editorias_impresso,df_NOTICIAS_impresso_filtrado):
    
    # Cria o gráfico de rosca
    bar_chart = pygal.HorizontalBar()
    
    # Adiciona as informações ao gráfico
    for edi, freq in zip(editorias_impresso['editorias'],editorias_impresso['freq']):
        
        # Filtra as informações para que nomes de reporteres não sejam adicionados as editorias
        if edi not in ['Bruno Vital', 'Líria Paz', 'Ícaro Carvalho', 'Felipe Salustino', 'Matteus Fernandes', 'Cláudio Oliveira', 'P.H.']:
            
            bar_chart.add(edi, freq)
            
    bar_chart.add(f"Total: {df_NOTICIAS_impresso_filtrado['pauta'].drop_duplicates().count()}", 0)
        
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg = bar_chart.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
def noticiasPorReporter_bc(reporteres_impresso):
    # # Cria o gráfico de rosca
    # bar_chart = pygal.HorizontalBar()
    
    # # Adiciona as informações ao gráfico
    # for rep_fot,freq in zip(reporteres_impresso['reporter_fotografo'], reporteres_impresso['freq']):
        
    #     # Filtra as informações para separar reporteres e fotógrafos
    #     if rep_fot in ['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷', 'Líria Paz', 'Margareth Grilo', 'Isaac Lira', 'Fernanda Souza']:
    #         continue # Vai para a próxima iteração do loop
    #     else:
    #         bar_chart.add(rep_fot.title(), freq)
    
    # # Renderizaçãodo gráfico em formato SVG
    # # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    # svg = bar_chart.render_data_uri()
    
    # # Formatando uma string HTML usando f-strings
    # # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    # st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

    reporteres_impresso = reporteres_impresso.sort_values(by='freq', ascending=True)
    fig = go.Figure(data=[go.Bar(x=reporteres_impresso['freq'], y=reporteres_impresso['reporter_fotografo'], orientation='h')])
    fig.update_traces(marker_color=px.colors.sequential.Oranges, marker_line_color='#66533D', marker_line_width=1.5)
    st.plotly_chart(fig)

'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos_bc(reporteres_impresso):
    # Cria o gráfico de rosca
    bar_chart = pygal.HorizontalBar()
    
    # Adiciona as informações ao gráfico
    for rep_fot,freq in zip(reporteres_impresso['reporter_fotografo'], reporteres_impresso['freq']):
        
        # Filtra as informações para deixar somente os fotógrafos
        if rep_fot in ['Magnus Nascimento📷', 'adriano abreu📷', 'Alex Regis📷']:
            bar_chart.add(rep_fot.title(), freq)
        else:
            continue # Vai para a próxima iteração do loop
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg = bar_chart.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro.
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
