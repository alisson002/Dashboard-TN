import streamlit as st
import pandas as pd
from datetime import datetime # Para pegar a data atual
from PIL import Image # Imagens da tn e jpn
from graficos.Tribuna_do_Norte import tnPortal
from graficos.Tribuna_do_Norte import tnImpresso
import importlib
from graficos.Tribuna_do_Norte import tnFB
from graficos.Tribuna_do_Norte import tnIG
from graficos.JP_News import jpnIG

# Cria um espaço reservado vazio onde vai receber as imagens
image_placeholder = st.empty()

# Caminho das imagens
TN_image_path = Image.open("imagens/tribunaLogo.png") 
JPN_image_path = Image.open("imagens/jpnnatalLogo3.png") 

# Criar seletor 1 na coluna à esquerda
options1 = ["Inicio - escolha uma opção:","Tribuna do norte", "JP News - Natal"]
selected_option1 = st.sidebar.selectbox("Selecione a opção 1:", options1)

# Criar seletor 2 na coluna à esquerda
if selected_option1 == "Tribuna do norte":
    options2 = ["Site/Portal", "Google Analytics (portal)","Impresso","Instagram", "Facebook", "Twitter", "YouTube"]
    selected_option2 = st.sidebar.selectbox("Selecione a opção 2:", options2)
# Criar seletor 2 na coluna à esquerda
elif selected_option1 == "JP News - Natal":
    options2 = ["Instagram", "Twitter", "YouTube"]
    selected_option2 = st.sidebar.selectbox("Selecione a opção 2:", options2)
else:
    
    html_text = """
        <p style='font-size:32px;'><b>•</b> Atualizações:</p>
        """
    st.write(html_text, unsafe_allow_html=True)
    st.write("╰┈➤ Mais gráficos do impresso alterados. Também foi adicionado novamente o gráfico dos fotografos. - (18/07/2024);")
    st.write("╰┈➤ **Impressões e cliques em anúncios (PORTAL TN):** novas tabelas adicionadas à dashboard do Google Looker. - (17/07/2024);")
    st.write("╰┈➤ Em breve farei atualizações visuais de alguns elementos da Dashboard. - (26/06/2024);")
    st.divider()
    st.write("**Tribuna do Norte:**")
    st.write("╰┈➤ Mais gráficos do impresso alterados. Também foi adicionado novamente o gráfico dos fotografos. - (18/07/2024);")
    st.write("╰┈➤ **Impressões e cliques em anúncios (PORTAL TN):** novas tabelas adicionadas à dashboard do Google Looker. - (17/07/2024);")
    st.write("╰┈➤ Adicionadas as médias das métricas do Instagram e Facebook - (26/06/2024);")
    st.divider()
    st.write("**Jovem Pan News - Natal:**")
    st.write("╰┈➤ Adicionadas as médias das métricas do Instagram - (26/06/2024);")
    st.write("╰┈➤ Adicionadas gráficos e métricas de alcance, visitas e seguidores do IG com comparativos em relação ao período anterior - (13/06/2024);")
    st.write("╰┈➤ Em breve;")
    st.divider()
    html_text = """
        <p style='font-size:32px;'><b>•</b> Sugestões/Informar erros:</p>
        """
    st.write(html_text, unsafe_allow_html=True)
    st.write("E-mail: kinto17@gmail.com")
    st.write("**Sugestões:**")
    st.write("╰┈➤ Título do e-mail: **SUGESTÃO - DASHBOARD STREAMLIT TN**;")
    st.write("╰┈➤ Título do e-mail: **SUGESTÃO - DASHBOARD STREAMLIT JPN**;")
    st.write("**Erro:**")
    st.write("╰┈➤ Título do e-mail: **ERRO - DASHBOARD STREAMLIT TN**;")
    st.write("╰┈➤ Título do e-mail: **ERRO - DASHBOARD STREAMLIT JPN**;")
    st.write("╰┈➤ Se possível envie prints complementando a informação do e-mail;")
    st.divider()
    options2 = []
    selected_option2 = st.sidebar.selectbox("Selecione a opção 2:", options2)

# Definindo a data mínima e máxima
data_minima = pd.to_datetime('2023-01-01')
if selected_option2 == "Site/Portal":
    data_maxima = pd.to_datetime('2023-10-16')
elif selected_option2 == "Impresso":
    data_maxima = pd.to_datetime(tnImpresso.df_noticias_impresso['data'].max()) + pd.DateOffset(days=1) # foi adicionado um dia pois na dashboard não aparece o ultimo dia, o dia o qual a tabela foi atualizada.
elif selected_option2 == "Facebook":
    data_maxima = pd.to_datetime(tnFB.dados_FB_alcance['Data'].max())
elif selected_option2 == "Instagram":
    data_maxima = pd.to_datetime(tnIG.alcanceIG['Data'].max()) 
else:
    data_maxima = pd.to_datetime('2024-06-06')

# Adicionar seletor de períodos na coluna à esquerda
start_date_ = st.sidebar.date_input("Data de início", data_minima, min_value = data_minima, max_value = data_maxima, format="YYYY-MM-DD") #"DD-MM-YYYY"

end_date_ = st.sidebar.date_input("Data de término", data_maxima, min_value = data_minima, max_value = data_maxima, format="YYYY-MM-DD") #+ pd.DateOffset(days=1) #"DD-MM-YYYY"

periodo = end_date_ - start_date_

# Periodo anteior para gráficos com comparações
start_date_b4 = start_date_ - pd.DateOffset(days = periodo.days+1)

end_date_b4 = end_date_ - pd.DateOffset(days = periodo.days+1) + pd.DateOffset(days=1)

#VERIFICAR ESSAS DATAS
#periodo selecionado difere um pouco do que realmente estáno gráfico
# # Adicionar seletor de períodos na coluna à esquerda
# start_date_ = st.sidebar.date_input("Data de início", data_minima, min_value = data_minima, max_value = data_maxima, format="YYYY-MM-DD") #"DD-MM-YYYY"

# end_date_ = st.sidebar.date_input("Data de término", data_maxima, min_value = data_minima, max_value = data_maxima, format="YYYY-MM-DD") + pd.DateOffset(days=1) #"DD-MM-YYYY"

# periodo = pd.to_datetime(end_date_) - pd.to_datetime(start_date_)

# # Periodo anteior para gráficos com comparações
# start_date_b4 = start_date_ - pd.DateOffset(days = periodo.days-2)

# end_date_b4 = end_date_ - pd.DateOffset(days = periodo.days-2)


# st.sidebar.write("AVISO (impresso): O dia 31/12/2023 não está sendo reconhecido corretamente. Não o selecionem, por favor.")
# html_text_data = """
#         <p style='font-size:12px;'><b>FORMATO DA DATA:</b> A data está sendo exibida no formato <b>AAAA-MM-DD</b> para que os dados sejam selecionados/comparados corretamente. A forma de selecionar continua a mesma.</p>
#         """
# st.sidebar.write(html_text_data, unsafe_allow_html=True)

# html_text_avisoPortal = """
#         <p style='font-size:12px;'><b>AVISO (TN - Site/Portal):</b> No momento, por conta da mudança para o novo site, os dados disponíveis vão somente até 16/10/2023. Em breve os dados serão atualizados. Quaisquer dados do portal que estiverem sendo exibidos em períodos após essa data não devem ser levados em consideração por enquanto.</p>
#         """
# st.sidebar.write(html_text_avisoPortal, unsafe_allow_html=True)

# html_text_orientacao = """
#         <p style='font-size:12px;'><b>ORIENTAÇÃO (tema/ cor de fundo):</b> caso no seu computador esteja iniciando com o tema escuro e você, usuário deste sistema, não goste de como está por conta do fundo do gráfico continuar branco, basta fazer o seguinte: 3 pontos verticais (canto superior direito) >> Settings >> Seletor (Choose app theme, colors and fonts) >> Light.</p>
#         """
# st.sidebar.write(html_text_orientacao, unsafe_allow_html=True)

# html_text_criador = """
#         <div style='text-align: right;'>
#         <p style='font-size:14px;'><b>Criado por:</b> Alisson Moreira.</p>
#         </div>
#         """
# st.sidebar.write(html_text_criador, unsafe_allow_html=True)

start_date = start_date_.strftime('%Y-%m-%d')
end_date = (end_date_+ pd.DateOffset(days=1)).strftime('%Y-%m-%d')

# tnPortal.filtroDeDatas(start_date, end_date) é a função que recebe as datas de inicio e fim do período selecionado e atualiza os dfs
# retorna multiplos dfs que seraão utilizados nas funções dos gráficos do portal
df_NOTICIAS_filtrado, editoria_freq, reporter_freq, reporter_unique, merge_ids_rep_noticias_editoria, fotografos, fotografos_teste = tnPortal.filtroDeDatas(start_date, end_date)

noticias_edi_somado, df_NOTICIAS_impresso_filtrado, reporteres_impresso, noticias_edi_somado, editorias_impresso = tnImpresso.filtroDeDatasImpresso(start_date, end_date)

# b4 = Before. Usado para compara periodos.
dados_FB_alcance_ANTERIOR, dados_FB_alcance_FILTRADAS,visitasFB_ANTERIOR,visitasFB_FILTRADO,seguidoresFB_ANTERIOR,seguidoresFB_FILTRADO = tnFB.filtrosDatasFACEBOOK(start_date, end_date, start_date_b4.strftime('%Y-%m-%d'), end_date_b4.strftime('%Y-%m-%d'))

dados_IG_alcance_ANTERIOR,dados_IG_alcance_FILTRADAS,visitasIG_ANTERIOR,visitasIG_FILTRADO,seguidoresIG_ANTERIOR,seguidoresIG_FILTRADO = tnIG.filtrosDatasINSTAGRAM(start_date, end_date, start_date_b4.strftime('%Y-%m-%d'), end_date_b4.strftime('%Y-%m-%d'))

dados_IG_alcance_ANTERIORjpn,dados_IG_alcance_FILTRADASjpn,visitasIG_ANTERIORjpn,visitasIG_FILTRADOjpn,seguidoresIG_ANTERIORjpn,seguidoresIG_FILTRADOjpn = jpnIG.filtrosDatasINSTAGRAMjpn(start_date, end_date, start_date_b4.strftime('%Y-%m-%d'), end_date_b4.strftime('%Y-%m-%d'))

# Exibe os gráficos de acordo com as opções selecionadas
if selected_option1 == "Tribuna do norte":
    
    # Adiciona a respectiva imagem ao topo da página
    image_placeholder.image(TN_image_path, use_column_width=True)
    
    # Gráficos referentes a cada categoria
    if selected_option2 == "Site/Portal":
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
                
            elif exib_type == 'Gráficos de barra':
                tnPortal.noticiasToTal_bc(df_NOTICIAS_filtrado)
                
        with tab2:
            
            if exib_type == 'Gráficos de rosca/pizza':
                
                # recebe o df editoria_freq com o período atualizado e exibe o gráfico na dashboard
                tnPortal.noticiasPorEditoria(editoria_freq)
                
            elif exib_type == 'Tabelas':
                
                # retorna o df das noticias por editoria
                table_noticias_edi = tnPortal.tabelaNoticiasEditoria(editoria_freq)
                
                # Exibindo os df com o width maximo
                st.dataframe(table_noticias_edi, use_container_width = True, hide_index=True)
            
            elif exib_type == 'Gráficos de barra':
                tnPortal.noticiasPorEditoria_bc(editoria_freq)
                
            
        with tab3:
            
            if exib_type == 'Gráficos de rosca/pizza':

                # recebe o df reporter_freq com o período atualizado e exibe o gráfico na dashboard
                tnPortal.noticiasPorReporter(reporter_freq)
                
            elif exib_type == 'Tabelas':
                
                # retorna o df das noticias por reporter
                table_noticias_rep = tnPortal.tabelaNoticiasReporter(reporter_freq)
                
                # Exibindo df com o width maximo
                st.dataframe(table_noticias_rep, use_container_width = True, hide_index=True)
                
            elif exib_type == 'Gráficos de barra':
                tnPortal.noticiasPorReporter_bc(reporter_freq)
                
        with tab4:
            
            if exib_type == 'Gráficos de rosca/pizza':

                # recebe o df reporter_unique e merge_ids_rep_noticias_editoria com o período atualizado e exibe o gráfico na dashboard
                tnPortal.editoriaPorReporter(reporter_unique, merge_ids_rep_noticias_editoria)
                
            elif exib_type == 'Tabelas':
                
                # retorna o df das editorias por reporter
                table_edi_rep = tnPortal.tableEditoriaPorReporter(reporter_unique, merge_ids_rep_noticias_editoria)
                
                # Exibindo df com o width maximo
                st.dataframe(table_edi_rep.drop_duplicates(), use_container_width = True, hide_index=True)
                
            elif exib_type == 'Gráficos de barra':
                tnPortal.editoriaPorReporter_bc(reporter_unique, merge_ids_rep_noticias_editoria)
                
            
        with tab5:
            st.write("Obs: os números são referentes a quantidade de notícias associadas ao fotógrafo. É importante observar que várias fotos podem ter sido tiradas.")
            if exib_type == 'Gráficos de rosca/pizza':
                
                # recebe o df fotografos com o período atualizado e exibe o gráfico na dashboard
                tnPortal.credfotografos(fotografos)
                
            elif exib_type == 'Tabelas':
                
                # Exibindo df com o width maximo
                # retorna o df dos fotografos
                st.dataframe(fotografos,use_container_width = True, hide_index=True)
            
            elif exib_type == 'Gráficos de barra':
                tnPortal.credfotografos_bc(fotografos)
                
        with tab6:
            # INCOMPLETO
            tnPortal.fotPorEditoria(fotografos)
        
            

    elif selected_option2 == "Impresso":
        # Radio para selecionar a forma de visualização
        exib_type = st.radio("Selecione o tipo de exibição:", ['Gráficos de rosca/pizza', 'Gráficos de barra', "Tabelas"], horizontal=True)
        
        # Tabs para separar as áreas analisadas
        
        # Informações de cada tab
        tab1, tab2, tab3, tab4, tab5= st.tabs(["Notícias por editoria", "Nóticias por repórter", "Editoria por repórter", "Créditos/origem das fotos", "Editoria por foto"])
        
        with tab1:
            html_text = """
            <p style='font-size:12px;'><b>•</b> A maioria das notícias possuem duas editorias cadastradas, portanto, a soma total é referente as notícias sem levar em consideração as editorias. Editorias com nomes de reporteres foram removidas da contagem.</p>
            """
            html_text2 = """
            <p style='font-size:12px;'><b>•</b> Passe o cursor por cima do gráfico para obter mais informações.</p>
            """
            html_text3 = """
            <p style='font-size:12px;'><b>•</b> Dê <b>clique duplo</b> em uma das informações da legenda para que somente ela seja exibida. Dessa forma, outras podem ser adicionadas uma a uma para uma melhor comparação entre determinadas editorias. Para remover ou adicionar apenas uma, basta <b>1 clique</b>.</p>
            """
            st.write(html_text, unsafe_allow_html=True) 
            if exib_type == 'Gráficos de rosca/pizza':
                
                # st.write(html_text2, unsafe_allow_html=True) 
                # st.write(html_text3, unsafe_allow_html=True) 
                
                tnImpresso.noticiasPorEditoria(editorias_impresso,df_NOTICIAS_impresso_filtrado)
                
            elif exib_type == 'Tabelas':
                
                # Exibindo df com o width maximo
                st.dataframe(tnImpresso.tableEdiImpresso(editorias_impresso), use_container_width = True, hide_index=True)
                
            elif exib_type == 'Gráficos de barra':
                
                st.write(html_text2, unsafe_allow_html=True)  
                tnImpresso.noticiasPorEditoria_bc(editorias_impresso,df_NOTICIAS_impresso_filtrado)
                
        with tab2:
            
            # st.write('Obs: Passe o cursor por cima do gráfico para obter mais informações.')
            if exib_type == 'Gráficos de rosca/pizza':
                
                tnImpresso.noticiasPorReporter(reporteres_impresso)
                
            elif exib_type == 'Tabelas':
                # Exibindo df com o width maximo
                st.dataframe(tnImpresso.tableRepImpresso(reporteres_impresso), use_container_width = True, hide_index=True)
            elif exib_type == 'Gráficos de barra':
                tnImpresso.noticiasPorReporter_bc(reporteres_impresso)
                
        with tab3:
            st.write('')
        with tab4:
            html_text = """
            <p style='font-size:12px;'><b>•</b> Os números são referentes a quantidade de notícias associadas ao fotógrafo.</p>
            """
            html_text2 = """
            <p style='font-size:12px;'><b>•</b> Após o <b>Trello</b> se tornar pago e o número de pessoas com acessor ser limitado alguns dados não se manteram, já que o algoritmo utiliza sua API para trazer os dados para esta dashboard de acordo com quem atualmente tem acesso aos quadros.</p>
            """
            html_text3 = """
            <p style='font-size:14px;'><b>• Dados a partir de 08/05/2024.</b> Dados a partir dessa data pois estão sendo adquiridos de outra forma, por conta do motivo citado acima.</p>
            """
            st.write(html_text, unsafe_allow_html=True) 
            st.write(html_text2, unsafe_allow_html=True) 
            st.write(html_text3, unsafe_allow_html=True) 
            if exib_type == 'Gráficos de rosca/pizza':
                # Gráfico de rosca
                tnImpresso.credfotografos(reporteres_impresso,editorias_impresso)
            elif exib_type == 'Tabelas':
                # Exibindo df com o width maximo
                st.dataframe(tnImpresso.tableFotografosImpresso(reporteres_impresso,editorias_impresso), use_container_width = True, hide_index=True)
            elif exib_type == 'Gráficos de barra':
                tnImpresso.credfotografos_bc(reporteres_impresso,editorias_impresso)
    
    elif selected_option2 == "Google Analytics (portal)":
        html_text = """
        <p style='font-size:32px;'><b>•</b> Os dados do Google Analytics relacionados ao portal estão no link abaixo em uma dashboard construida no <b>Looker Studio</b>, que também é uma plataforma da Google.</p>
        """
        st.write(" ")
        st.write(html_text, unsafe_allow_html=True) 
        st.write("**Link: https://lookerstudio.google.com/reporting/c15e734d-d123-4070-acd9-a7c5e23df494**")   
        st.write(" ")
        st.write("Para ter acesso aos dados, siga os seguintes passos:")
        st.write("1. Entre no link;")
        st.write("2. Faça login com uma conta Gmail;")
        st.write("3. Solicite acesso para visualizar (**Ver**) os dados.") 

    elif selected_option2 == "Instagram":
        
        tnIG.igMetrics(dados_IG_alcance_ANTERIOR,dados_IG_alcance_FILTRADAS,visitasIG_ANTERIOR,visitasIG_FILTRADO,seguidoresIG_ANTERIOR,seguidoresIG_FILTRADO)
        
        exib_type = st.radio("Selecione o tipo de exibição:", ['Normal', 'Acumulativo'], horizontal=True)
        
        # Tabs para separar as áreas analisadas
        tab1, tab2, tab3 = st.tabs(["Alcance", "Visitas", "Seguidores"])
        
        # Informações de cada tab
        with tab1:
            
            tnIG.igMedias_alcance(dados_IG_alcance_FILTRADAS)

            if exib_type == "Normal":

                tnIG.IG_alcance(dados_IG_alcance_ANTERIOR, dados_IG_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                tnIG.IG_alcance_cumsum(dados_IG_alcance_ANTERIOR, dados_IG_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4)
        
        with tab2:
            
            tnIG.igMedias_visitas(visitasIG_FILTRADO)
            if exib_type == "Normal":

                tnIG.IG_visitas(visitasIG_ANTERIOR, visitasIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                tnIG.IG_visitas_cumsum(visitasIG_ANTERIOR, visitasIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)
        
        with tab3:
            
            st.write("Obs.: os números de seguidores são apenas em relação aos ganhos. Os valores de perda não são disponibilizados para download.")
            tnIG.igMedias_seguidores(seguidoresIG_FILTRADO)
            if exib_type == "Normal":

                tnIG.IG_seguidores(seguidoresIG_ANTERIOR, seguidoresIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                tnIG.IG_seguidores_cumsum(seguidoresIG_ANTERIOR, seguidoresIG_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)
        
    elif selected_option2 == "Facebook":

        tnFB.fbMetrics(dados_FB_alcance_ANTERIOR,dados_FB_alcance_FILTRADAS,visitasFB_ANTERIOR,visitasFB_FILTRADO,seguidoresFB_ANTERIOR,seguidoresFB_FILTRADO)
        
        exib_type = st.radio("Selecione o tipo de exibição:", ['Normal', 'Acumulativo'], horizontal=True)
        
        # Tabs para separar as áreas analisadas
        tab1, tab2, tab3 = st.tabs(["Alcance", "Visitas", "Seguidores"])
        
        # Informações de cada tab
        with tab1:
            tnFB.FBMedias_alcance(dados_FB_alcance_FILTRADAS)
            if exib_type == "Normal":

                tnFB.FB_alcance(dados_FB_alcance_ANTERIOR, dados_FB_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                tnFB.FB_alcance_cumsum(dados_FB_alcance_ANTERIOR, dados_FB_alcance_FILTRADAS, start_date, end_date, start_date_b4, end_date_b4)
        
        with tab2:
            tnFB.FBMedias_visitas(visitasFB_FILTRADO)
            if exib_type == "Normal":

                tnFB.FB_visitas(visitasFB_ANTERIOR, visitasFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                tnFB.FB_visitas_cumsum(visitasFB_ANTERIOR, visitasFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)
        
        with tab3:
            tnFB.FBMedias_seguidores(seguidoresFB_FILTRADO)
            if exib_type == "Normal":

                tnFB.FB_seguidores(seguidoresFB_ANTERIOR, seguidoresFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                tnFB.FB_seguidores_cumsum(seguidoresFB_ANTERIOR, seguidoresFB_FILTRADO, start_date, end_date, start_date_b4, end_date_b4)
        
    elif selected_option2 == "Twitter":
        st.write("Gráficos do twitter")
    elif selected_option2 == "YouTube":
        st.write("Gráficos do youtube")

elif selected_option1 == "JP News - Natal":
    # Adiciona a respectiva imagem ao topo da página
    image_placeholder.image(JPN_image_path, use_column_width=True)
    
    # Gráficos referentes a cada categoria
    if selected_option2 == "Instagram":
        
        jpnIG.igMetrics(dados_IG_alcance_ANTERIORjpn,dados_IG_alcance_FILTRADASjpn,visitasIG_ANTERIORjpn,visitasIG_FILTRADOjpn,seguidoresIG_ANTERIORjpn,seguidoresIG_FILTRADOjpn)
        
        exib_type = st.radio("Selecione o tipo de exibição:", ['Normal', 'Acumulativo'], horizontal=True)
        
        # Tabs para separar as áreas analisadas
        tab1, tab2, tab3 = st.tabs(["Alcance", "Visitas", "Seguidores"])
        
        # Informações de cada tab
        with tab1:
            jpnIG.igMedias_alcance(dados_IG_alcance_FILTRADASjpn)
            if exib_type == "Normal":
                
                jpnIG.IG_alcance(dados_IG_alcance_ANTERIORjpn, dados_IG_alcance_FILTRADASjpn, start_date, end_date, start_date_b4, end_date_b4)
        
            elif exib_type == "Acumulativo":
                jpnIG.IG_alcance_cumsum(dados_IG_alcance_ANTERIORjpn, dados_IG_alcance_FILTRADASjpn, start_date, end_date, start_date_b4, end_date_b4)
        
        with tab2:
            jpnIG.igMedias_visitas(visitasIG_FILTRADOjpn)
            if exib_type == "Normal":

                jpnIG.IG_visitas(visitasIG_ANTERIORjpn, visitasIG_FILTRADOjpn, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                jpnIG.IG_visitas_cumsum(visitasIG_ANTERIORjpn, visitasIG_FILTRADOjpn, start_date, end_date, start_date_b4, end_date_b4)
        
        with tab3:
            st.write("Obs.: os números de seguidores são apenas em relação aos ganhos. Os valores de perda não são disponibilizados para download.")
            jpnIG.igMedias_seguidores(seguidoresIG_FILTRADOjpn)
            if exib_type == "Normal":

                jpnIG.IG_seguidores(seguidoresIG_ANTERIORjpn, seguidoresIG_FILTRADOjpn, start_date, end_date, start_date_b4, end_date_b4)

            elif exib_type == "Acumulativo":
                jpnIG.IG_seguidores_cumsum(seguidoresIG_ANTERIORjpn, seguidoresIG_FILTRADOjpn, start_date, end_date, start_date_b4, end_date_b4)
        
    elif selected_option2 == "Twitter":
        st.write("Gráficos do twitter")
    elif selected_option2 == "YouTube":
        st.write("Gráficos do youtube")

# Adicione mais condições conforme necessário para outras opções
