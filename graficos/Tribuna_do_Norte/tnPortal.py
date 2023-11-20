import pygal
import pandas as pd
import streamlit as st

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
merge_ids_reporterNoticias = pd.merge(ids_noticias, ids_reporter, on='usu_id', how='left')

# Lista com os nomes dos reporters sem repetições
reporter_unique = merge_ids_reporterNoticias['usu_nome'].unique()

# Da merge nos dataframes editoria e ids_reporter com base nos ids de usuários. 
# O primeiro possui apenas a coluna dos ids e tipos de editoria com repetições para cada uma das notícias.
# O segundo possui tanto a coluna dos ids quanto a dos usuários, massem repetições.
# A saída será um novo data frame contendo três colunas, onde os nome dos usuários e as editorias seram replicados para seus repesctivos ids.
merge2_ids_reporterNoticias_ediDescricao = pd.merge(editoria, ids_reporter, on='usu_id', how='left')


def noticiasPorEditoria():
    # Recebe uma cópia de um dos merges, conta a freqeuncia de cada informação na coluna de editoria e organiza em ordem decrescente
    editoria_freq = merge2_ids_reporterNoticias_ediDescricao.copy()['edi_descricao'].value_counts().reset_index()

    editoria_freq.columns = ['edi_descricao', 'Freq']

    # Cria o gráfico de rosca
    pie_chart = pygal.Pie(inner_radius = raio_interno)
    
    # Titulo do gráfico
    pie_chart.title = "Notícias online"
    
    # Adiciona cada item no gráfico e seu respectivo valor
    for edi, freq in zip(editoria_freq['edi_descricao'], editoria_freq['Freq']):
        pie_chart.add(edi, freq)
    
    # Recebe e 'escreve' o gráfico em svg na dashboard
    svg = pie_chart.render_data_uri()
    st.markdown(f'<embed type="image/svg+xml" src="{svg}" />', unsafe_allow_html=True)
    

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

def noticiasPorReporter():
    pie_chart_reporter = pygal.Pie(inner_radius=raio_interno)
    
    # # Recebe uma cópia de um dos merges, conta a freqeuncia de cada informação na coluna de nome dos usuários e organiza em ordem decrescente
    reporter_freq = merge_ids_reporterNoticias.copy()['usu_nome'].value_counts().reset_index()

    reporter_freq.columns = ['usu_nome', 'Freq']
    
    for nome, freq in zip(reporter_freq['usu_nome'],reporter_freq['Freq']):
        pie_chart_reporter.add(nome, freq)
    
    
    # Recebe a o gráfico em svg
    svg3 = pie_chart_reporter.render_data_uri()
    
    # Renderizar o gráfico e incorporar no Streamlit
    st.markdown(f'<embed type="image/svg+xml" src="{svg3}" />', unsafe_allow_html=True)


def reporterPorEditoria():
    # Recebe lista de reporters para o seletor
    options3 = reporter_unique
    selected_option3 = st.selectbox("Selecione um reporter:", options3)
    
    pie_chart_repEdi = pygal.Pie(inner_radius=raio_interno)
    
    # Recebe um dataframe com a editorias do reporter selecionado de acordo com o seletor selected_option3
    df_loc_repEdi = merge2_ids_reporterNoticias_ediDescricao.loc[merge2_ids_reporterNoticias_ediDescricao.usu_nome == f'{selected_option3}']
    
    df_repEdi =  df_loc_repEdi[['usu_nome', 'edi_descricao']]
    
    # Organizando de acordo com a editoria que mais aparece
    df_repEdi['Freq'] = df_repEdi.groupby('edi_descricao')['edi_descricao'].transform('count')
    # Dataframe organizado
    df_repEdi_Organizado = df_repEdi.sort_values(by='Freq', ascending=False)
    
    for item in df_repEdi_Organizado['edi_descricao'].unique():
        pie_chart_repEdi.add(item, df_repEdi['edi_descricao'].value_counts()[item])
    
    total_ediRep = df_repEdi['edi_descricao'].count()
    pie_chart_repEdi.add(f'Total: {total_ediRep}', 0)
    
    svg4 = pie_chart_repEdi.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg4}" />', unsafe_allow_html=True)
    
def fotografos():
    fotografos = df_noticias.copy()['fot_credito'].value_counts().reset_index()

    fotografos.columns = ['fot_credito', 'Freq']
    
    pie_chart_fot = pygal.Pie(inner_radius=raio_interno)
    
    for fotografo, freq in zip(fotografos['fot_credito'],fotografos['Freq']):
        pie_chart_fot.add(fotografo, freq)
    
    svg6 = pie_chart_fot.render_data_uri()
    
    st.markdown(f'<embed type="image/svg+xml" src="{svg6}" />', unsafe_allow_html=True)
