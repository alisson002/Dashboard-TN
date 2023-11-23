import pygal
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


raio_interno = 0.7
raio_half = 0.2

# Recebe a tabela com as notícias
df_noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)

# Recebe a tabela com os usuários e os respectivos ids
df_reporter = pd.read_csv('tabelas/noticias online/usuarios.csv')

# Manipulando as tabelas para fazer o gráfico dos reporters
# Recebe apenas a coluna de id de usuários
ids_noticias = df_noticias['usu_id_fk']

# Recebe as colunas de ids e nomes de usuários
ids_reporter = df_reporter[['usu_id', 'usu_nome']]

# Recebe as colunas de ids e os tipos de editoria
editoria = df_noticias[['usu_id_fk', 'edi_descricao']]

# Renomeia a coluna usu_id_fk -> usu_id para ser usada no merge
ids_noticias = ids_noticias.rename('usu_id')
editoria = editoria.rename(columns={'usu_id_fk': 'usu_id'})

# Da merge nos dataframes ids_noticias e ids_reporter com base nos ids de usuários. 
# O primeiro possui apenas a coluna dos ids com repetições para cada uma das notícias. 
# O segundo tanto a coluna dos ids quanto a dos usuários, massem repetições.
# A saída será um novo data frame contendo duas colunas, onde os nome dos usuários seram replicados para seus repesctivos ids.
merge_ids_noticias_reporters = pd.merge(ids_noticias, ids_reporter, on='usu_id', how='left')

# Lista com os nomes dos reporters sem repetições
reporter_unique = merge_ids_noticias_reporters['usu_nome'].unique()

# Da merge nos dataframes editoria e ids_reporter com base nos ids de usuários. 
# O primeiro possui apenas a coluna dos ids e tipos de editoria com repetições para cada uma das notícias.
# O segundo possui tanto a coluna dos ids quanto a dos usuários, massem repetições.
# A saída será um novo data frame contendo três colunas, onde os nome dos usuários e as editorias seram replicados para seus repesctivos ids.
merge_ids_rep_noticias_editoria = pd.merge(editoria, ids_reporter, on='usu_id', how='left')

# Recebe uma cópia de um dos merges, conta a freqeuncia de cada informação na coluna de editoria e organiza em ordem decrescente
editoria_freq = merge_ids_rep_noticias_editoria.copy()['edi_descricao'].value_counts().reset_index()

editoria_freq.columns = ['edi_descricao', 'Freq']

# Recebe uma cópia de um dos merges, conta a freqeuncia de cada informação na coluna de nome dos usuários e organiza em ordem decrescente
reporter_freq = merge_ids_noticias_reporters.copy()['usu_nome'].value_counts().reset_index()

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
# Recebe uma cópia da coluna dos fotógrafos 
# dropna(how='all') remove todas as linhas com NaN ou NA
# .astype(str) transforma em string
# .str.split('/') remove tudo que vier depois de uma barra. p.ex. /Agência Brasil
# .str[0] Seleciona somente o texto de antes da barra, pois foram separados em duas partes
# .str.lower() Deixa todas as primeiras letras maiúsculas
# .replace('marcelo casal jr','marcello casal jr') substitui uma string
fotografos = df_noticias.copy()['fot_credito']\
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

# Remove as repetições, deixa apenas inofrmações únicas, conta quantas vezes cada informação se repete e organiza da maior freqência para a menor
fotografos = fotografos.value_counts().reset_index()

# Renomeia a coluna com a contagem de cada string única
fotografos.columns = ['fot_credito', 'Freq']

'''
MESMA LÓGICA, MAS PARA DUAS COLUNAS
'''
# Aplica a lógica para as duas colunas simultaneamente
# TESTAR COM .MAP()
fotografos_edi = df_noticias[['fot_credito', 'edi_descricao']].copy()\
.astype(str)\
.applymap(lambda x: x.lower() if pd.notna(x) else x)\
.applymap(lambda x: x.replace('marcelo casal jr', 'marcello casal jr') if pd.notna(x) else x)\
.applymap(remover_caracteres)\
.applymap(lambda x: ''.join(filter(lambda char: char.isprintable(), x)) if pd.notna(x) else x)

#.applymap(lambda x: x.split('/')[0] if pd.notna(x) else x)\
    
'''
GRÁFICOS DE ROSCA/PIZZA/MEIA PIZZA
'''
'''TOTAL: contagem de notícias online e fora do ar e notícias do online e impresso.'''
def noticiasToTal():
    
    options4 = ["Online (notícias do portal)", "Por veículo"]
    selected_option4 = st.selectbox("Selecione o formato:", options4)
    
    ativas = df_noticias['not_status'].value_counts()[1]
    
    desonline = df_noticias['not_status'].value_counts()[0]
    
    total = df_noticias['not_status'].count()
    
    if selected_option4 == "Online (notícias do portal)":
        # Criar um gráfico de pizza
        pie_chart_total = pygal.Pie(inner_radius=raio_half, half_pie=True)

        pie_chart_total.add(f'Ativas: {ativas}', ativas)
        
        pie_chart_total.add(f'Fora do "ar": {desonline}', desonline)
        
        pie_chart_total.add(f'Total: {total}', 0)
        
        svg1 = pie_chart_total.render_data_uri()
        
        # Renderizar o gráfico e incorporar no Streamlit
        st.markdown(f'<embed type="image/svg+xml" src="{svg1}" />', unsafe_allow_html=True)
    elif selected_option4 == "Por veículo":
        
        st.write("Obs: o total tem o mesmo valor que o online pois tudo que foi para o impresso está no online, mas o mesmo não vale para o contrario.")
        
        # Criar um gráfico de pizza
        pie_chart_total = pygal.Pie(inner_radius=raio_half, half_pie=True)

        pie_chart_total.add('Online', [ativas, desonline])
        
        impresso = df_noticias['not_veiculo'].value_counts()[0]
        pie_chart_total.add('Impresso', impresso)
        
        pie_chart_total.add(f'Total: {total}', 0)
        
        svg5 = pie_chart_total.render_data_uri()
        
        # Renderizar o gráfico e incorporar no Streamlit
        st.markdown(f'<embed type="image/svg+xml" src="{svg5}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorEditoria():

    # Cria o gráfico de rosca
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    # Adiciona cada item no gráfico e seu respectivo valor
    for edi, freq in zip(editoria_freq['edi_descricao'], editoria_freq['Freq']):
        pie_chart.add(edi, freq)
    
    # Recebe e 'escreve' o gráfico em svg na dashboard
    svg = pie_chart.render_data_uri()
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)

'''NOTÍCIAS POR REPORTER: contagem de noticias por editoria (organizado do maior para o menor)'''
def noticiasPorReporter():
    pie_chart_reporter = pygal.Pie(inner_radius=raio_interno)
        
    for nome, freq in zip(reporter_freq['usu_nome'],reporter_freq['Freq']):
        pie_chart_reporter.add(nome, freq)
    
    
    # Recebe a o gráfico em svg
    svg3 = pie_chart_reporter.render_data_uri()
    
    # Renderizar o gráfico e incorporar no Streamlit
    st.markdown(f'<embed type="image/svg+xml" src="{svg3}" />', unsafe_allow_html=True)

'''função para selecionar os reporters'''
def reporterSelector():
    # Recebe lista de reporters para o seletor
    options = reporter_unique
    selected_option = st.selectbox("Selecione um reporter:", options)
    
    # Recebe um dataframe com a editorias do reporter selecionado de acordo com o seletor selected_option3
    df_loc_repEdi = merge_ids_rep_noticias_editoria.loc[merge_ids_rep_noticias_editoria.usu_nome == f'{selected_option}']
    
    df_repEdi =  df_loc_repEdi[['usu_nome', 'edi_descricao']]
    
    # Organizando de acordo com a editoria que mais aparece
    df_repEdi['Freq'] = df_repEdi.groupby('edi_descricao')['edi_descricao'].transform('count')
    # Dataframe organizado
    df_repEdi_Organizado = df_repEdi.sort_values(by='Freq', ascending=False)
    
    return df_repEdi_Organizado

'''EDITORIA POR REPORTER: contagem de editoria por reporter (organizado do maior para o menor)'''
def editoriaPorReporter():
    df_repEdi_Organizado = reporterSelector()
    
    pie_chart_repEdi = pygal.Pie(inner_radius=raio_interno)
    
    for item in df_repEdi_Organizado['edi_descricao'].unique():
        pie_chart_repEdi.add(item, df_repEdi_Organizado['edi_descricao'].value_counts()[item])
    
    total_ediRep = df_repEdi_Organizado['edi_descricao'].count()
    pie_chart_repEdi.add(f'Total: {total_ediRep}', 0)
    
    svg4 = pie_chart_repEdi.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg4}" />', unsafe_allow_html=True)
    
    
def credfotografos():
    # Cria o gráfico
    pie_chart_fot = pygal.Pie(inner_radius=raio_interno)
    
    # Slider para selecionar quais informações vão aparecer
    values = st.slider(
        'Selecione um intervalo:',
        0, len(fotografos['fot_credito']), (0, 24))
    
    # Inicio e fim do slider para serem usados no plot do gráfico
    inicio = values[0]
    fim = values[1]
    
    # Add as informações do df fotografos de acordo com o slider
    for fotografo, freq in zip(fotografos['fot_credito'][inicio:fim],fotografos['Freq'][inicio:fim]):
        pie_chart_fot.add(fotografo, freq)
        
    #st.write(fotografos)
    
    # recebe as informações do gráfico em svg
    svg6 = pie_chart_fot.render_data_uri()
    
    # Renderiza o gráfico
    st.markdown(f'<embed type="image/svg+xml" src="{svg6}" />', unsafe_allow_html=True)

def fotPorEditoria():
    
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
TABELAS
'''
'''TOTAL: contagem de notícias online e fora do ar e notícias do online e impresso.'''
# Recebendo as colunas e contando os calores únicos de cada informação
table_noticias_on = df_noticias['not_status'].value_counts().reset_index()

table_noticias_veiculo = df_noticias['not_veiculo'].value_counts().reset_index()

# Renomeando as colunas
table_noticias_on.columns = ['Status da notícia', 'Contagem']

table_noticias_veiculo.columns = ['Veículo', 'Contagem']

# Alterando as linhas pois estavam como 0 e 1
table_noticias_on['Status da notícia'] = table_noticias_on['Status da notícia'].map({1: "online", 0: "fora do 'ar'"})

table_noticias_veiculo['Veículo'] = table_noticias_veiculo['Veículo'].map({1: "online", 0: "impresso"})

# Alterando o valor das notícias online para o valor total, que é o correto
table_noticias_veiculo['Contagem'][0] = df_noticias['not_status'].count()


'''NOTÍCIAS POR EDITORIA: contagem de noticias por editoria (organizado do maior para o menor)'''
# Recebe um cópia do df utilizado
table_noticias_edi = editoria_freq.copy()

# Renomeia as colunas
table_noticias_edi.columns = ['Editorias', 'Contagem']


'''NOTÍCIAS POR REPORTER: contagem de noticias por reporter (organizado do maior para o menor)'''
# Recebe um cópia do df utilizado
table_noticias_rep = reporter_freq.copy()

# Renomeia as colunas
table_noticias_rep.columns = ['Repórteres', 'Contagem']


'''EDITORIA POR REPORTER: contagem de editoria por reporter (organizado do maior para o menor)'''
def tableEditoriaPorReporter():
    df_repEdi_Organizado = reporterSelector()
    
    table_edi_rep = df_repEdi_Organizado[['edi_descricao', 'Freq']].copy()
    
    table_edi_rep.columns = ['Editorias do repórter selecionado', 'Contagem']
    
    #table_edi_rep = table_edi_rep['edi_descricao'].value_counts()
    
    st.dataframe(table_edi_rep.drop_duplicates(), use_container_width = True)
