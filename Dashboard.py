import streamlit as st
import pandas as pd
from datetime import datetime # Para pegar a data atual
from PIL import Image # Imagens da tn e jpn
from graficos.Tribuna_do_Norte import tnPortal
from graficos.Tribuna_do_Norte import tnImpresso
import importlib

# Cria um espaço reservado vazio onde vai receber as imagens
image_placeholder = st.empty()

# Caminho das imagens
TN_image_path = Image.open("imagens/tribunaLogo.png") 
JPN_image_path = Image.open("imagens/jpnnatalLogo3.png") 

# Criar seletor 1 na coluna à esquerda
options1 = ["Escolha uma opção","Tribuna do norte", "JP News - Natal"]
selected_option1 = st.sidebar.selectbox("Selecione a opção 1:", options1)

# if selected_option1 == "Tribuna do norte":
#     image_placeholder.image(TN_image_path, use_column_width=True)
# elif selected_option1 == "JP News - Natal":
#     image_placeholder.image(JPN_image_path, use_column_width=True)

# Criar seletor 2 na coluna à esquerda
if selected_option1 == "Tribuna do norte":
    options2 = ["Site/Portal", "Impresso","Instagram", "Facebook", "Twitter", "YouTube"]
    selected_option2 = st.sidebar.selectbox("Selecione a opção 2:", options2)
# Criar seletor 2 na coluna à esquerda
elif selected_option1 == "JP News - Natal":
    options2 = ["Instagram", "Twitter", "YouTube"]
    selected_option2 = st.sidebar.selectbox("Selecione a opção 2:", options2)
else:
    options2 = []
    selected_option2 = st.sidebar.selectbox("Selecione a opção 2:", options2)
    
# Definindo a data mínima e máxima
data_minima = pd.to_datetime('2023-01-01')
data_maxima = pd.to_datetime(tnPortal.df_noticias.iloc[-1]['not_datapub'])
    
# Adicionar seletor de períodos na coluna à esquerda
start_date = st.sidebar.date_input("Data de início", data_minima, min_value = data_minima, max_value = data_maxima, format="DD-MM-YYYY")

end_date = st.sidebar.date_input("Data de término", data_maxima, min_value = data_minima, max_value = data_maxima, format="DD-MM-YYYY") + pd.DateOffset(days=1)

start_date = start_date.strftime('%m-%d-%y') #'%d-%m-%Y'
end_date = end_date.strftime('%m-%d-%y')

# tnPortal.filtroDeDatas(start_date, end_date) é a função que recebe as datas de inicio e fim do período selecionado e atualiza os dfs
# retorna multiplos dfs que seram utilizados nas funções dos gráficos do portal
df_NOTICIAS_filtrado, editoria_freq, reporter_freq, reporter_unique, merge_ids_rep_noticias_editoria, fotografos = tnPortal.filtroDeDatas(start_date, end_date)

# Adicione seus gráficos de acordo com as opções selecionadas
if selected_option1 == "Tribuna do norte":
    # Adiciona a respectiva imagem ao topo da página
    image_placeholder.image(TN_image_path, use_column_width=True)
    
    # Gráficos referentes a cada categoria
    if selected_option2 == "Site/Portal":
        
        # Radio para selecionar a forma de visualização
        exib_type = st.radio("Selecione o tipo de exibição:", ['Gráficos de rosca/pizza', 'Gráficos de barra', "Tabelas"], horizontal=True)
        
        # Tabs para separar as áreas analisadas
        tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["Total", "Notícias por editoria", "Nóticias por repórter", "Editoria por repórter", "Créditos/origem das fotos", "Editoria por foto"])
        
        # Informações de cada tab
        with tab1:
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                # recebe o df df_NOTICIAS_filtrado com o período atualizado e exibe o gráfico na dashboard
                tnPortal.noticiasToTal(df_NOTICIAS_filtrado)
            elif exib_type == 'Tabelas':
                
                # retorna o df das noticias online
                table_noticias_on = tnPortal.tabelaNoticiasOnline(df_NOTICIAS_filtrado)
                # Exibindo os df com o width maximo
                st.dataframe(table_noticias_on[['Status da notícia', 'Contagem']], use_container_width = True, hide_index=True)
                
                # retorna o df das noticias por veiculo
                table_noticias_veiculo = tnPortal.tabelaNoticiasVeiculo(df_NOTICIAS_filtrado)
                st.dataframe(table_noticias_veiculo[['Veículo', 'Contagem']], use_container_width = True, hide_index=True)
                
        with tab2:
            
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                # recebe o df editoria_freq com o período atualizado e exibe o gráfico na dashboard
                tnPortal.noticiasPorEditoria(editoria_freq)
            elif exib_type == 'Tabelas':
                
                # retorna o df das noticias por editoria
                table_noticias_edi = tnPortal.tabelaNoticiasEditoria(editoria_freq)
                
                # Exibindo os df com o width maximo
                st.dataframe(table_noticias_edi, use_container_width = True, hide_index=True)
            
        with tab3:
            
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                # recebe o df reporter_freq com o período atualizado e exibe o gráfico na dashboard
                tnPortal.noticiasPorReporter(reporter_freq)
            elif exib_type == 'Tabelas':
                
                # retorna o df das noticias por reporter
                table_noticias_rep = tnPortal.tabelaNoticiasReporter(reporter_freq)
                
                # Exibindo df com o width maximo
                st.dataframe(table_noticias_rep, use_container_width = True, hide_index=True)
                
        with tab4:
            
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                # recebe o df reporter_unique e merge_ids_rep_noticias_editoria com o período atualizado e exibe o gráfico na dashboard
                tnPortal.editoriaPorReporter(reporter_unique, merge_ids_rep_noticias_editoria)
            elif exib_type == 'Tabelas':
                
                # retorna o df das editorias por reporter
                table_edi_rep = tnPortal.tableEditoriaPorReporter(reporter_unique, merge_ids_rep_noticias_editoria)
                
                # Exibindo df com o width maximo
                st.dataframe(table_edi_rep.drop_duplicates(), use_container_width = True, hide_index=True)
                
            
        with tab5:
            st.write("Obs: os números são referentes a quantidade de notícias associadas ao fotógrafo. É importante observar que várias fotos podem ter sido tiradas.")
            if exib_type == 'Gráficos de rosca/pizza':
                
                # Gráfico de rosca
                # recebe o df fotografos com o período atualizado e exibe o gráfico na dashboard
                tnPortal.credfotografos(fotografos)
                
            elif exib_type == 'Tabelas':
                
                # Exibindo df com o width maximo
                # retorna o df dos fotografos
                st.dataframe(fotografos, use_container_width = True, hide_index=True)
        with tab6:
            # INCOMPLETO
            tnPortal.fotPorEditoria(fotografos)
            

    elif selected_option2 == "Impresso":
        # Radio para selecionar a forma de visualização
        exib_type = st.radio("Selecione o tipo de exibição:", ['Gráficos de rosca/pizza', 'Gráficos de barra', "Tabelas"], horizontal=True)
        
        # Tabs para separar as áreas analisadas
        st.write('Obs: dados importados do Trello do Tribuna do Norte. Portanto, podem divergir dos dados do impresso mostrado junto dos dados do Portal.')
        
        # Informações de cada tab
        tab1, tab2, tab3, tab4, tab5= st.tabs(["Notícias por editoria", "Nóticias por repórter", "Editoria por repórter", "Créditos/origem das fotos", "Editoria por foto"])
        
        with tab1:
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                tnImpresso.noticiasPorEditoria()
            elif exib_type == 'Tabelas':
                # Exibindo df com o width maximo
                st.dataframe(tnImpresso.teble_ediImpresso, use_container_width = True, hide_index=True)
        with tab2:
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                tnImpresso.noticiasPorReporter()
            elif exib_type == 'Tabelas':
                # Exibindo df com o width maximo
                st.dataframe(tnImpresso.table_reporteres_impresso, use_container_width = True, hide_index=True)
        with tab3:
            st.write('')
        with tab4:
            st.write("Obs: os números são referentes a quantidade de notícias associadas ao fotógrafo. É importante observar que várias fotos podem ter sido tiradas.")
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                tnImpresso.credfotografos()
            elif exib_type == 'Tabelas':
                # Exibindo df com o width maximo
                st.dataframe(tnImpresso.table_fotografos, use_container_width = True, hide_index=True)
        
    elif selected_option2 == "Instagram":
        st.write("Gráficos do instagram")
    elif selected_option2 == "Facebook":
        st.write("Gráficos do facebook")
    elif selected_option2 == "Twitter":
        st.write("Gráficos do twitter")
    elif selected_option2 == "YouTube":
        st.write("Gráficos do youtube")

elif selected_option1 == "JP News - Natal":
    # Adiciona a respectiva imagem ao topo da página
    image_placeholder.image(JPN_image_path, use_column_width=True)
    
    # Gráficos referentes a cada categoria
    if selected_option2 == "Instagram":
        st.write("Gráficos do instagram")
    elif selected_option2 == "Twitter":
        st.write("Gráficos do twitter")
    elif selected_option2 == "YouTube":
        st.write("Gráficos do youtube")

# Adicione mais condições conforme necessário para outras opções
