import streamlit as st
import pandas as pd
from datetime import datetime # Para pegar a data atual
from PIL import Image # Imagnes da tn e jpn
from graficos.Tribuna_do_Norte import tnPortal

# Cria um espaço reservado vazio onde vai receber as imagens
image_placeholder = st.empty()

# Caminho das imagens
TN_image_path = Image.open("imagens/tribunaLogo.jpg") 
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
data_maxima = pd.to_datetime(datetime.now())
    
# Adicionar seletor de períodos na coluna à esquerda
start_date = st.sidebar.date_input("Data de início", data_minima, format="DD-MM-YYYY")
end_date = st.sidebar.date_input("Data de término", data_maxima, format="DD-MM-YYYY")

# Indica o período selecionado
#st.write(f"Período selecionado: de {start_date.strftime('%d-%m-%y')} a {end_date.strftime('%d-%m-%y')}")

# Adicione seus gráficos de acordo com as opções selecionadas
if selected_option1 == "Tribuna do norte":
    # Adiciona a respectiva imagem ao topo da página
    image_placeholder.image(TN_image_path, use_column_width=True)
    
    # Gráficos referentes a cada categoria
    if selected_option2 == "Site/Portal":
        tab1, tab2, tab3, tab4, tab5= st.tabs(["Total", "Notícias por ditoria", "Nóticias por reporter", "Editoria por reporter", "Notícias por fotógrafos"])
        with tab1:
            tnPortal.noticiasToTal()
        with tab2:
            tnPortal.noticiasPorEditoria()
        with tab3:
            tnPortal.noticiasPorReporter()
        with tab4:
            tnPortal.reporterPorEditoria()
        with tab5:
            tnPortal.fotografos()

    elif selected_option2 == "Impresso":
        st.write("Gráficos do impresso")
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
