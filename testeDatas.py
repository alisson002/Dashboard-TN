import streamlit as st
import pandas as pd

df_noticias = pd.read_csv('tabelas/noticias online/noticiasOnline.csv', low_memory=False)

df_noticias['not_datapub'] = pd.to_datetime(df_noticias['not_datapub']).dt.strftime('%m-%d-%y')

data_minima = pd.to_datetime('2023-01-01')
data_maxima = pd.to_datetime(df_noticias.iloc[-1]['not_datapub'])
    
# Adicionar seletor de períodos na coluna à esquerda
start_date = st.sidebar.date_input("Data de início", data_minima, min_value = data_minima, max_value = data_maxima, format="DD-MM-YYYY")

end_date = st.sidebar.date_input("Data de término", data_maxima, min_value = data_minima, max_value = data_maxima, format="DD-MM-YYYY") + pd.DateOffset(days=1)
print(type(end_date))
#df_noticias_filtrado = df_noticias.loc[df_noticias.not_datapub > start_date and df_noticias.not_datapub < end_date]

start_date = start_date.strftime('%m-%d-%y') #'%d-%m-%Y'
end_date = end_date.strftime('%m-%d-%y')
print(type(end_date))
df_filtrado = df_noticias.loc[(df_noticias['not_datapub'] > start_date) & (df_noticias['not_datapub'] < end_date)]

# df_filtrado['not_datapub'] = pd.to_datetime(df_filtrado['not_datapub'], format='%d-%m-%Y')

#df_filtrado = df_noticias.loc[(df_noticias['not_datapub'].dt.date > start_date) & (df_noticias['not_datapub'].dt.date < end_date)]

df_filtrado['not_datapub'] = pd.to_datetime(df_filtrado['not_datapub']).dt.strftime('%d-%m-%y')

#st.dataframe(df_filtrado['not_datapub'], use_container_width = True, hide_index=True)


with open("datas.txt", "w") as arquivo:
    # Escrever os valores das variáveis no arquivo
    arquivo.write(f"Nome: {start_date}\n")
    arquivo.write(f"Idade: {end_date}\n")


