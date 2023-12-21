import pygal
import pandas as pd
import streamlit as st

"""
    Descrição da função.
    
    Args:
        parametro: Descrição do parâmetro.
    
    Returns:
        Tipo de retorno: Descrição do que a função retorna.
"""

# Raios para os gráficos de rosca
raio_interno = 0.7
raio_half = 0.2

# Recebe a tabela com as notícias do online
# low_memory=False por a tabela ser grande
df_noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)


def filtroDeDatas(start_date, end_date):
    
    """DADOS POR PERIODO SELECIONADO"""
    
    # Recebe uma cópia do df das notícias
    df_noticias_FILTRADAS_POR_DATAS = df_noticias.copy()

    # Manipulação da coluna com data e horário de publicação
    # Remove o horário e mantem somente a data
    # data inicialmente no formato '%m-%d-%y' para que em seguida seja feita a comparação de datas, no formato '%d-%m-%y' a comparação não ocorria corretamente
    df_noticias_FILTRADAS_POR_DATAS['not_datapub'] = pd.to_datetime(df_noticias_FILTRADAS_POR_DATAS['not_datapub']).dt.strftime('%m-%d-%y')

    # Agrupa todos os dados do df de acordo com o periodo selecionado e as datas na coluna de datas
    df_NOTICIAS_filtrado = df_noticias_FILTRADAS_POR_DATAS.loc[(df_noticias_FILTRADAS_POR_DATAS['not_datapub'] > start_date) & (df_noticias_FILTRADAS_POR_DATAS['not_datapub'] < end_date)]

    # Altera o formato da data para '%d-%m-%y' após o filtro
    df_NOTICIAS_filtrado['not_datapub'] = pd.to_datetime(df_NOTICIAS_filtrado['not_datapub']).dt.strftime('%d-%m-%y')
    
    '''FIM NOTICIAS FILTRADAS'''

    # Recebe a tabela com os usuários e os respectivos ids
    df_reporter = pd.read_csv('tabelas/noticias online/usuarios.csv')

    # Manipulando dfs para os gráficos
    # Recebe apenas a coluna de id de usuários do df de notícias
    ids_noticias = df_NOTICIAS_filtrado['usu_id_fk']

    # Recebe as colunas de ids e nomes de usuários do df de reporteres
    ids_reporter = df_reporter[['usu_id', 'usu_nome']]

    # Recebe as colunas de ids e os tipos de editoria do df de noticias
    editoria = df_NOTICIAS_filtrado[['usu_id_fk', 'edi_descricao']]

    # Renomeia a coluna usu_id_fk -> usu_id para ser usada no merge, já que devem ser iguais para a mesclagem e uma coluna com os nomes de usuários ser criada possuindo o mesmo tamanho do restante das colunas do df de notícias
    ids_noticias = ids_noticias.rename('usu_id')
    editoria = editoria.rename(columns={'usu_id_fk': 'usu_id'})

    # Da merge nos dataframes ids_noticias e ids_reporter com base nos ids de usuários. 
    # O primeiro possui apenas a coluna dos ids com repetições para cada uma das notícias. 
    # O segundo tanto a coluna dos ids quanto a dos usuários, mas sem repetições.
    # A saída será um novo data frame contendo duas colunas, onde os nome dos usuários serão replicados para seus repesctivos ids.
    merge_ids_noticias_reporters = pd.merge(ids_noticias, ids_reporter, on='usu_id', how='left')

    # Series com os nomes dos reporters sem repetições
    filtred_merge_reporteres = merge_ids_noticias_reporters.copy()
    filtred_merge_reporteres = filtred_merge_reporteres.loc[~filtred_merge_reporteres['usu_nome'].isin(['Flávio Pantoja Monteiro', 'Wagner Guerra', 'Iva Kareninna da Silva Câmara', 'Jerusa Vieira do Nascimento'])]
    reporter_unique = filtred_merge_reporteres['usu_nome'].unique()
    #.isin(['Flávio Pantoja Monteiro', 'Wagner Guerra', 'Iva Kareninna da Silva Câmara', 'Jerusa Vieira do Nascimento'])

    # Da merge nos dataframes editoria e ids_reporter com base nos ids de usuários. 
    # O primeiro possui as colunas dos ids e tipos de editoria com repetições para cada uma das notícias.
    # O segundo possui tanto a coluna dos ids quanto a dos usuários, mas sem repetições.
    # A saída será um novo data frame contendo três colunas, onde os nome dos usuários e as editorias seram replicados para seus repesctivos ids.
    merge_ids_rep_noticias_editoria = pd.merge(editoria, ids_reporter, on='usu_id', how='left')

    # Recebe uma cópia do merge de editoria e ids_reporter
    # value_counts().reset_index() conta a freqeuncia de cada informação na coluna de editoria e organiza em ordem decrescente de acordo com a coluna que conta a freqência de cada informação
    editoria_freq = merge_ids_rep_noticias_editoria.copy()['edi_descricao'].value_counts().reset_index()

    # Renomeia as colunas
    # 'Freq' é para a coluna criada com a contagem das informações que é criada como 'count'
    editoria_freq.columns = ['edi_descricao', 'Freq']

    # Recebe uma cópia do merge de ids_noticias e ids_reporter, conta a freqeuncia de cada informação na coluna de nome dos usuários e organiza em ordem decrescente de acordo com a coluna que conta a freqência de cada informação
    reporter_freq = merge_ids_noticias_reporters.copy()['usu_nome'].value_counts().reset_index()

    # Renomeia as colunas
    # 'Freq' é para a coluna criada com a contagem das informações que é criada como 'count'
    reporter_freq.columns = ['usu_nome', 'Freq']

    # Remove determinados caracteres
    def remover_caracteres(s):
        caracteres_a_remover = [".", ",", "-", "_"]
        for c in caracteres_a_remover:
            s = s.replace(c, '')
        return s


    '''
    MANIPULANDO O DF DOS FOTÓGRAFOS
    '''
    # Recebe uma cópia da coluna dos fotógrafos do df de notícias
    # dropna(how='all') remove todas as linhas com NaN ou NA
    # .astype(str) transforma em string
    # .str.split('/') remove tudo que vier depois de uma barra. p.ex. /Agência Brasil
    # .str[0] Seleciona somente o texto de antes da barra, pois foram separados em duas partes
    # .str.lower() Deixa todas as primeiras letras minúsculas
    # .replace('marcelo casal jr','marcello casal jr') substitui uma string

    fotografos = df_NOTICIAS_filtrado.copy()['fot_credito']\
        .dropna(how='all')\
        .astype(str).str\
        .split('/')\
        .str[0]\
        .str.lower()\
        .replace('marcelo casal jr','marcello casal jr')

    # Remove determinados caracteres de acordo com a função remover_caracteres
    # .str.title() Deixa todas as primeiras letras maiúsculas
    # .str.replace(r'(?<=/)\s+', '', regex=True) remove o espaço dps da barra
    fotografos = fotografos.apply(remover_caracteres).str.title()
    #.str.replace(r'(?<=/)\s+', '', regex=True)

    # Determina as informações que são 'imprimiveis'
    fotografos = fotografos.apply(lambda x: ''.join(filter(lambda char: char.isprintable(), x)))

    # Remove as repetições, deixa apenas informações únicas, conta quantas vezes cada informação se repete e organiza da maior freqência para a menor
    fotografos = fotografos.value_counts().reset_index()

    # Renomeia a coluna com a contagem de cada string única
    # 'Freq' é para a coluna criada com a contagem das informações que é criada como 'count'
    fotografos.columns = ['fot_credito', 'Freq']

    '''
    MESMA LÓGICA, MAS PARA DUAS COLUNAS

    Será usada para a criação da tab com o gráfico interativo de editorias por fotógrafo, que seria parecido com o criado para editoria por repórter.

    Tb é necessário resolver o problema das linhas com strings repetidas, mas com pequenas diferenças que fazem com que sejam contabilizadas separadamente.
    '''
    # Aplica a lógica para as duas colunas simultaneamente
    # TESTAR COM .MAP()
    # fotografos_edi = df_noticias[['fot_credito', 'edi_descricao']].copy()\
    # .astype(str)\
    # .applymap(lambda x: x.lower() if pd.notna(x) else x)\
    # .applymap(lambda x: x.replace('marcelo casal jr', 'marcello casal jr') if pd.notna(x) else x)\
    # .applymap(remover_caracteres)\
    # .applymap(lambda x: ''.join(filter(lambda char: char.isprintable(), x)) if pd.notna(x) else x)

    #.applymap(lambda x: x.split('/')[0] if pd.notna(x) else x)\
    
    return df_NOTICIAS_filtrado, editoria_freq, reporter_freq, reporter_unique, merge_ids_rep_noticias_editoria, fotografos

'''
GRÁFICOS DE ROSCA/PIZZA/MEIA PIZZA
'''
'''TOTAL: contagem de notícias online e fora do ar e notícias do online e impresso.'''
def noticiasToTal(df_NOTICIAS_filtrado):
    
    df_NOTICIAS_filtrado['not_datapub'] = pd.to_datetime(df_NOTICIAS_filtrado['not_datapub']).dt.strftime('%d-%m-%y')
    
    # Seletor para alternar entre os gráficos de Online (notícias do portal) e Por veículo, esse último que também inclui as notícias do impresso
    # Todas as notícias do impresso estão no online
    options4 = ["Online (notícias do portal)", "Por veículo"]
    selected_option4 = st.selectbox("Selecione o formato:", options4)
    
    # Contagem de notícias ainda acessíveis no site
    # Na coluna not_status do df de notícias informação é representada pelo número 1
    ativas = df_NOTICIAS_filtrado['not_status'].value_counts()[1]
    
    # Contagem de notícias fora do "ar" no site
    # Na coluna not_status do df de notícias informação é representada pelo número 0
    desonline = df_NOTICIAS_filtrado['not_status'].value_counts()[0]
    
    # Contagem total de notícias no site dentro do período disponívem no df
    total = df_NOTICIAS_filtrado['not_status'].count()
    
    # Condicional para selecionar o gráfico exibido
    if selected_option4 == "Online (notícias do portal)":
        # Criar meio gráfico de rosca
        pie_chart_total = pygal.Pie(inner_radius=raio_half, half_pie=True)

        # Adicionando os dados no gráfico
        # Nóticias ainda tivas
        pie_chart_total.add(f'Ativas: {ativas}', ativas)
        
        # Fora do "ar"
        pie_chart_total.add(f'Fora do "ar": {desonline}', desonline)
        
        # Total
        pie_chart_total.add(f'Total: {total}', 0)
        
        '''
        Os gráficos da biblioteca pygal são em formato SVG, o qual não é 'naturalmente' suportado pelo streamlit.
        
        p.ex.: Não é possível, com esse formato, apenas criar o gráfico e no final chamar a variável/objeto em que ele está armazenado, como pode ser visto abaixo.
        
        ex_plot ou st.write(ex_plot)
        
        Portanto foi utilizada a forma abaixo para renderiza-lo, já que o que recebemos de pie_chart_total.render_data_uri() é uma grande string com multiplos caracteres que formam a imagem, e isso deve ser interpretado para que o gráfico seja exibido e não a string.
        '''
        
        # Renderizaçãodo gráfico em formato SVG
        # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
        svg1 = pie_chart_total.render_data_uri()
        
        # Formatando uma string HTML usando f-strings
        # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
        # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
        st.markdown(f'<embed type="image/svg+xml" src="{svg1}" />', unsafe_allow_html=True)
        
        
    elif selected_option4 == "Por veículo":
        st.write("Obs: o total tem o mesmo valor que o online pois tudo que foi para o impresso está no online, mas o mesmo não vale para o contrario.")
        
        # Criar um gráfico de rosca
        pie_chart_total = pygal.Pie(inner_radius=raio_half, half_pie=True)

        # Adiciona os dados das notícias online e fora do ar para contabilizar o total de notícias do online
        pie_chart_total.add('Online', [ativas, desonline])
        
        # Recebe a contagem de notícias do impresso
        # Essa informação é representada pelo 0 na coluna not_veiculo do df de notícias
        impresso = df_NOTICIAS_filtrado['not_veiculo'].value_counts()[0]
        
        # Adiciona os dados do impresso ao gráfico
        pie_chart_total.add('Impresso', impresso)
        
        # Adiciona o valor total
        pie_chart_total.add(f'Total: {total}', 0)
        
        # Renderizaçãodo gráfico em formato SVG
        # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
        svg5 = pie_chart_total.render_data_uri()
        
        # Formatando uma string HTML usando f-strings
        # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
        # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
        st.markdown(f'<embed type="image/svg+xml" src="{svg5}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorEditoria(editoria_freq):
    # Cria o gráfico de rosca
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    # Adiciona cada item no gráfico e seu respectivo valor
    for edi, freq in zip(editoria_freq['edi_descricao'], editoria_freq['Freq']):
        pie_chart.add(edi, freq)
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg = pie_chart.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR REPORTER: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorReporter(reporter_freq):
    # Cria o gráfico de rosca
    pie_chart_reporter = pygal.Pie(inner_radius=raio_interno)
    
    # Adiciona cada reporter no gráfico e seu respectivo valor referente ao número de notícias
    for nome, freq in zip(reporter_freq['usu_nome'],reporter_freq['Freq']):
        if nome in ['Flávio Pantoja Monteiro', 'Wagner Guerra', 'Iva Kareninna da Silva Câmara', 'Jerusa Vieira do Nascimento']:
            continue
        else:
            pie_chart_reporter.add(nome, freq)
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg3 = pie_chart_reporter.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg3}" />', unsafe_allow_html=True)

'''função para selecionar os reporters'''
def reporterSelector(reporter_unique, merge_ids_rep_noticias_editoria):
    # Recebe series de reporteres para o seletor
    options = reporter_unique
    
    #.isin(['Flávio Pantoja Monteiro', 'Wagner Guerra', 'Iva Kareninna da Silva Câmara', 'Jerusa Vieira do Nascimento'])
    
    # Seletor que vai ser utilizado para filtrar os dados da tabela de acordo com o reporter selecionado
    selected_option = st.selectbox("Selecione um reporter:", options)
    
    # Recebe um dataframe com a editorias do reporter selecionado de acordo com o seletor
    df_loc_repEdi = merge_ids_rep_noticias_editoria.loc[merge_ids_rep_noticias_editoria.usu_nome == f'{selected_option}']
    
    # Recebe apenas duas colunas do df
    df_repEdi =  df_loc_repEdi[['usu_nome', 'edi_descricao']]
    
    # Organizando de acordo com a editoria que mais aparece e recebendo as informações em uma nova coluna
    '''
    testar com .values_count().reset_index()
    
    Foi feito da forma abaixo por ser com mais colunas
    '''
    df_repEdi['Freq'] = df_repEdi.groupby('edi_descricao')['edi_descricao'].transform('count')
    
    # Dataframe organizado
    df_repEdi_Organizado = df_repEdi.sort_values(by='Freq', ascending=False)
    
    return df_repEdi_Organizado

'''EDITORIA POR REPORTER: contagem de editoria por reporter (organizado do maior para o menor)'''
def editoriaPorReporter(reporter_unique, merge_ids_rep_noticias_editoria):
    # Recebe o df já organizado e somente com os dados do reporter selecionado
    df_repEdi_Organizado = reporterSelector(reporter_unique, merge_ids_rep_noticias_editoria)
    
    # Cria o gráfico de rosca
    pie_chart_repEdi = pygal.Pie(inner_radius=raio_interno)
    
    # Adiciona ao gráfico as editorias do reporter selecionado e seus respectivos valores
    for item in df_repEdi_Organizado['edi_descricao'].unique():
        pie_chart_repEdi.add(item, df_repEdi_Organizado['edi_descricao'].value_counts()[item])
    
    # Adiciona o valor total de editorias de cada reporter de acordo com o selecionado
    total_ediRep = df_repEdi_Organizado['edi_descricao'].count()
    pie_chart_repEdi.add(f'Total: {total_ediRep}', 0)
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg4 = pie_chart_repEdi.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg4}" />', unsafe_allow_html=True)
    
'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos(fotografos):
    # Cria o gráfico
    pie_chart_fot = pygal.Pie(inner_radius=raio_interno)
    
    # Slider para selecionar quais informações vão aparecer, já que as fotos vem de muitas origens diferentes
    # Values vai receber o intervalo selecionado e vai armazena-lo em um vetor de tamanho 2
    values = st.slider(
        'Selecione um intervalo:',
        0, len(fotografos['fot_credito']), (0, 24))
    
    # Inicio e fim do slider para serem usados no plot do gráfico
    inicio = values[0]
    fim = values[1]
    
    # Add ao grafico as informações do df fotografos de acordo com o intervalo do slider
    # Serão adicionados os nomes dos fotógrafos/origem da imgem e a contagem de cada um
    for fotografo, freq in zip(fotografos['fot_credito'][inicio:fim],fotografos['Freq'][inicio:fim]):
        pie_chart_fot.add(fotografo, freq)
        
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg6 = pie_chart_fot.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg6}" />', unsafe_allow_html=True)

'''estudar uma forma de corrigir os dados no df para fazer essa parte'''
def fotPorEditoria(fotografos):
    
    input_text = st.text_input("Digite um nome:")
    
    if input_text:
        
        options = fotografos[fotografos['fot_credito'].str.startswith(input_text)]['fot_credito'].unique().tolist()
        
        # Exibir um menu suspenso (selectbox) com as opções de autocompletar
        selected_name = st.selectbox("Escolha um nome:", options)
        
        # Exibir o nome selecionado
        st.write("Você escolheu:", selected_name)
    
    # # Slider para selecionar quais informações vão aparecer
    # values = st.slider(
    #     'Selecione um intervalo:',
    #     0, len(fotografos['fot_credito']), (0, 24))
    
    # # Inicio e fim do slider para serem usados no plot do gráfico
    # inicio = values[0]
    # fim = values[1]
    
    # options = fotografos_edi['fot_credito'].unique()[inicio:fim]
    # selected_option = st.selectbox("Fotógrafo/Origem da foto", options)
    
    # pie_chart_fotEdi = pygal.Pie(inner_radius=raio_interno)
    
    # df_loc_fotEdi = fotografos_edi.loc[fotografos_edi.fot_credito == f'{selected_option}']

'''
DFs PARA O STREAMLIT
'''
'''TOTAL: contagem de notícias online e fora do ar e notícias do online e impresso.'''
def tabelaNoticiasOnline(df_NOTICIAS_filtrado):
    # Recebendo as colunas e contando os calores únicos de cada informação
    table_noticias_on = df_NOTICIAS_filtrado['not_status'].value_counts().reset_index()

    # Renomeando as colunas
    table_noticias_on.columns = ['Status da notícia', 'Contagem']

    # Alterando as linhas pois estavam como 0 e 1
    table_noticias_on['Status da notícia'] = table_noticias_on['Status da notícia'].map({1: "online", 0: "fora do 'ar'"})
    
    return table_noticias_on


def tabelaNoticiasVeiculo(df_NOTICIAS_filtrado):
    
    table_noticias_veiculo = df_NOTICIAS_filtrado['not_veiculo'].value_counts().reset_index()  
    
    table_noticias_veiculo.columns = ['Veículo', 'Contagem']
    
    table_noticias_veiculo['Veículo'] = table_noticias_veiculo['Veículo'].map({1: "online", 0: "impresso"})

    # Alterando o valor das notícias online para o valor total, que é o correto
    table_noticias_veiculo['Contagem'][0] = df_NOTICIAS_filtrado['not_status'].count()
    
    return table_noticias_veiculo

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''

def tabelaNoticiasEditoria(editoria_freq):
    # Recebe um cópia do df utilizado
    table_noticias_edi = editoria_freq.copy()

    # Renomeia as colunas
    table_noticias_edi.columns = ['Editorias', 'Contagem']
    
    return table_noticias_edi


'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
def tabelaNoticiasReporter(reporter_freq):
    # Recebe um cópia do df utilizado
    table_noticias_rep = reporter_freq.copy()

    # Renomeia as colunas
    table_noticias_rep.columns = ['Repórteres', 'Contagem']
    
    cond = ~table_noticias_rep['Repórteres'].isin(['Flávio Pantoja Monteiro', 'Wagner Guerra', 'Iva Kareninna da Silva Câmara', 'Jerusa Vieira do Nascimento'])
    
    table_noticias_rep = table_noticias_rep[cond]
    
    return table_noticias_rep


'''EDITORIA POR REPORTER: contagem de editoria por reporter (organizado do maior para o menor)'''
def tableEditoriaPorReporter(reporter_unique, merge_ids_rep_noticias_editoria):
    # Recebe o df já organizado e com os dados de acordo com o reporter selecionado
    df_repEdi_Organizado = reporterSelector(reporter_unique, merge_ids_rep_noticias_editoria)
    
    # Recebe uma cópia de duas colunas do df
    table_edi_rep = df_repEdi_Organizado[['edi_descricao', 'Freq']].copy()
    
    # Renomeia as colunas
    table_edi_rep.columns = ['Editorias do repórter selecionado', 'Contagem']
    
    #table_edi_rep = table_edi_rep['edi_descricao'].value_counts()
    return table_edi_rep
    

'''GRÁFICOS DE BARRA'''
'''TOTAL: contagem de notícias online e fora do ar e notícias do online e impresso.'''
def noticiasToTal_bc(df_NOTICIAS_filtrado):
    
    df_NOTICIAS_filtrado['not_datapub'] = pd.to_datetime(df_NOTICIAS_filtrado['not_datapub']).dt.strftime('%d-%m-%y')
    
    # Seletor para alternar entre os gráficos de Online (notícias do portal) e Por veículo, esse último que também inclui as notícias do impresso
    # Todas as notícias do impresso estão no online
    options4 = ["Online (notícias do portal)", "Por veículo"]
    selected_option4 = st.selectbox("Selecione o formato:", options4)
    
    # Contagem de notícias ainda acessíveis no site
    # Na coluna not_status do df de notícias informação é representada pelo número 1
    ativas = df_NOTICIAS_filtrado['not_status'].value_counts()[1]
    
    # Contagem de notícias fora do "ar" no site
    # Na coluna not_status do df de notícias informação é representada pelo número 0
    desonline = df_NOTICIAS_filtrado['not_status'].value_counts()[0]
    
    # Contagem total de notícias no site dentro do período disponívem no df
    total = df_NOTICIAS_filtrado['not_status'].count()
    
    # Condicional para selecionar o gráfico exibido
    if selected_option4 == "Online (notícias do portal)":
        # Criar meio gráfico de rosca
        bar_chart_total = pygal.HorizontalBar()

        # Adicionando os dados no gráfico
        # Nóticias ainda tivas
        bar_chart_total.add(f'Ativas: {ativas}', ativas)
        
        # Fora do "ar"
        bar_chart_total.add(f'Fora do "ar": {desonline}', desonline)
        
        # Total
        bar_chart_total.add(f'Total: {total}', 0)
        
        '''
        Os gráficos da biblioteca pygal são em formato SVG, o qual não é 'naturalmente' suportado pelo streamlit.
        
        p.ex.: Não é possível, com esse formato, apenas criar o gráfico e no final chamar a variável/objeto em que ele está armazenado, como pode ser visto abaixo.
        
        ex_plot ou st.write(ex_plot)
        
        Portanto foi utilizada a forma abaixo para renderiza-lo, já que o que recebemos de bar_chart_total.render_data_uri() é uma grande string com multiplos caracteres que formam a imagem, e isso deve ser interpretado para que o gráfico seja exibido e não a string.
        '''
        
        # Renderizaçãodo gráfico em formato SVG
        # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
        svg1 = bar_chart_total.render_data_uri()
        
        # Formatando uma string HTML usando f-strings
        # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
        # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
        st.markdown(f'<embed type="image/svg+xml" src="{svg1}" />', unsafe_allow_html=True)
        
        
    elif selected_option4 == "Por veículo":
        st.write("Obs: o total tem o mesmo valor que o online pois tudo que foi para o impresso está no online, mas o mesmo não vale para o contrario.")
        
        # Criar um gráfico de rosca
        bar_chart_total = pygal.HorizontalBar()

        # Adiciona os dados das notícias online e fora do ar para contabilizar o total de notícias do online
        bar_chart_total.add('Online', [ativas, desonline])
        
        # Recebe a contagem de notícias do impresso
        # Essa informação é representada pelo 0 na coluna not_veiculo do df de notícias
        impresso = df_NOTICIAS_filtrado['not_veiculo'].value_counts()[0]
        
        # Adiciona os dados do impresso ao gráfico
        bar_chart_total.add('Impresso', impresso)
        
        # Adiciona o valor total
        bar_chart_total.add(f'Total: {total}', 0)
        
        # Renderizaçãodo gráfico em formato SVG
        # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
        svg5 = bar_chart_total.render_data_uri()
        
        # Formatando uma string HTML usando f-strings
        # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
        # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
        st.markdown(f'<embed type="image/svg+xml" src="{svg5}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorEditoria_bc(editoria_freq):
    # Cria o gráfico de rosca
    bar_chart = pygal.HorizontalBar()
    
    # Adiciona cada item no gráfico e seu respectivo valor
    for edi, freq in zip(editoria_freq['edi_descricao'], editoria_freq['Freq']):
        bar_chart.add(edi, freq)
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg = bar_chart.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR REPORTER: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorReporter_bc(reporter_freq):
    # Cria o gráfico de rosca
    bar_chart_reporter = pygal.HorizontalBar()
    
    # Adiciona cada reporter no gráfico e seu respectivo valor referente ao número de notícias
    for nome, freq in zip(reporter_freq['usu_nome'],reporter_freq['Freq']):
        if nome in ['Flávio Pantoja Monteiro', 'Wagner Guerra', 'Iva Kareninna da Silva Câmara', 'Jerusa Vieira do Nascimento']:
            continue
        else:
            bar_chart_reporter.add(nome, freq)
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg3 = bar_chart_reporter.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg3}" />', unsafe_allow_html=True)

'''EDITORIA POR REPORTER: contagem de editoria por reporter (organizado do maior para o menor)'''
def editoriaPorReporter_bc(reporter_unique, merge_ids_rep_noticias_editoria):
    # Recebe o df já organizado e somente com os dados do reporter selecionado
    df_repEdi_Organizado = reporterSelector(reporter_unique, merge_ids_rep_noticias_editoria)
    
    # Cria o gráfico de rosca
    bar_chart_repEdi = pygal.HorizontalBar()
    
    # Adiciona ao gráfico as editorias do reporter selecionado e seus respectivos valores
    for item in df_repEdi_Organizado['edi_descricao'].unique():
        bar_chart_repEdi.add(item, df_repEdi_Organizado['edi_descricao'].value_counts()[item])
    
    # Adiciona o valor total de editorias de cada reporter de acordo com o selecionado
    total_ediRep = df_repEdi_Organizado['edi_descricao'].count()
    bar_chart_repEdi.add(f'Total: {total_ediRep}', 0)
    
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg4 = bar_chart_repEdi.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg4}" />', unsafe_allow_html=True)
    
'''FOTÓGRAFOS: contagem de noticias por fotógrafo (organizado do maior para o menor)'''
def credfotografos_bc(fotografos):
    # Cria o gráfico
    bar_chart_fot = pygal.HorizontalBar()
    
    # Slider para selecionar quais informações vão aparecer, já que as fotos vem de muitas origens diferentes
    # Values vai receber o intervalo selecionado e vai armazena-lo em um vetor de tamanho 2
    values = st.slider(
        'Selecione um intervalo:',
        0, len(fotografos['fot_credito']), (0, 24))
    
    # Inicio e fim do slider para serem usados no plot do gráfico
    inicio = values[0]
    fim = values[1]
    
    # Add ao grafico as informações do df fotografos de acordo com o intervalo do slider
    # Serão adicionados os nomes dos fotógrafos/origem da imgem e a contagem de cada um
    for fotografo, freq in zip(fotografos['fot_credito'][inicio:fim],fotografos['Freq'][inicio:fim]):
        bar_chart_fot.add(fotografo, freq)
        
    # Renderizaçãodo gráfico em formato SVG
    # .render_data_uri() gera a representação do gráfico em formato SVG e retorna um URI de dados (data URI)
    svg6 = bar_chart_fot.render_data_uri()
    
    # Formatando uma string HTML usando f-strings
    # A string resultante contém uma tag <embed> que está sendo usada para incorporar um conteúdo SVG na página.
    # unsafe_allow_html=True: permite que o Streamlit interprete e exiba o conteúdo HTML fornecido como seguro. 
    st.markdown(f'<embed type="image/svg+xml" src="{svg6}" />', unsafe_allow_html=True)

'''estudar uma forma de corrigir os dados no df para fazer essa parte'''
def fotPorEditoria(fotografos):
    
    input_text = st.text_input("Digite um nome:")
    
    if input_text:
        
        options = fotografos[fotografos['fot_credito'].str.startswith(input_text)]['fot_credito'].unique().tolist()
        
        # Exibir um menu suspenso (selectbox) com as opções de autocompletar
        selected_name = st.selectbox("Escolha um nome:", options)
        
        # Exibir o nome selecionado
        st.write("Você escolheu:", selected_name)
    
