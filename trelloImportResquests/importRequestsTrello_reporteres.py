import requests
import json
import csv

'''CHAVES, TOKEN E REQUESTS INICIAIS'''
# Chave de API e Token de acesso fornecidos pelo Trello
API_KEY = '14d771355a6d5e6844830a88f5af930f'
TOKEN = 'ATTA58f75daa52546fed11141ce22e6ac3d978755aa1dba5b112f1e606bf668da1dcE6A7BB6A'

# ID do quadro/área de trabalho do Trello que você deseja extrair dados
# TRELLO_BOARD_ID = 'bLA2Uwel'
TRELLO_BOARD_ID = 'bLA2Uwel'
LIST_ID = TRELLO_BOARD_ID
# URL da API do Trello para obter listas e cartões
LISTS_URL = f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists'
CARDS_URL = f'https://api.trello.com/1/lists/{LIST_ID}/cards'

# Lista para armazenar dados
data = []

# Pega as informações dos quadros
response = requests.get(f'{LISTS_URL}?key={API_KEY}&token={TOKEN}')
lists_data = response.json()

'''SEPARANDO LISTAS DOS DOIS QUADROS QUE SERÃO UTILIZADOS'''
pautas_feitas_list = None
publicados_list = None
# Guarda os dois quadros que eu vou precisar de acordo com o nome do quadro
for lista in lists_data:
    if lista['name'] == 'PAUTAS FEITAS':
        pautas_feitas_list = lista
    elif lista['name'] == '✅ PUBLICADOS':
        publicados_list = lista
    elif lista['name'] == 'FLASHES  DO DIA':
        flashes_do_dia_list = lista

'''PEGANDO CADA UM DOS CARTÕES DO RESPECTIVO QUADRO'''
# Pautas_feitas_list['id'] pega o id do quadro PAUTAS FEITAS
# Usa esse id pra conseguir os dados de cada um dos cartões dentro desse quadro
response = requests.get(f'https://api.trello.com/1/lists/{pautas_feitas_list['id']}/cards?key={API_KEY}&token={TOKEN}')
# Dados dos cartões dentro do quadro PAUTAS FEITAS
pautas_feitas_cards_data = response.json()

# Publicados_list['id'] pega o id do quadro ✅PUBLICADOS
# Usa esse id pra conseguir os dados de cada um dos cartões dentro desse quadro
response = requests.get(f'https://api.trello.com/1/lists/{publicados_list['id']}/cards?key={API_KEY}&token={TOKEN}')
# Dados dos cartões dentro do quadro ✅PUBLICADOS
publicados_cards_data = response.json()

# flashes_do_dia_list['id'] pega o id do quadro FLASHES DO DIA
# Usa esse id pra conseguir os dados de cada um dos cartões dentro desse quadro
response = requests.get(f'https://api.trello.com/1/lists/{flashes_do_dia_list['id']}/cards?key={API_KEY}&token={TOKEN}')
# Dados dos cartões dentro do quadro FLASHES DO DIA
flashes_do_dia_cards_data = response.json()

'''FUNÇÕES'''
# Pega todos os 'idMembers' de cada quadro e coloca em sua respectiva lista
# Recebe os dados de cada um dos cartões e a key para acessar determinada informação de um dict
def getIds(pautas_feitas_cards_data, publicados_cards_data,flashes_do_dia_cards_data, key):
    # Listas para receber os ids dos jornalistas e fotógrafos no trello
    ID_members_pautas_feitas =[]
    ID_members_publicados = []
    ID_members_flashes = []
    
    for item_pf in pautas_feitas_cards_data:
        ID_members_pautas_feitas.append(item_pf[key])
    
    for item_pub in publicados_cards_data:
        ID_members_publicados.append(item_pub[key])
        
    for item_pub in flashes_do_dia_cards_data:
        ID_members_flashes.append(item_pub[key])
    
    return ID_members_pautas_feitas, ID_members_publicados, ID_members_flashes


# Recebe uma lista de listas, remove as listas dentro da lista e unifica todas as informações na lista de "fora", juntando as listas em uma só     
def simplificar_listas(*args):
    lista_de_listas = args[0]+args[1]+args[2]
    lista_simplificada = []
    for lista in lista_de_listas:
        lista_simplificada.extend(lista)
    return lista_simplificada


# Remove as IDs repetidas - feito dessa forma para evitar uso de loops
def removePalavrasRepetidas(lista_palavras):
    
    # Convertendo a lista para um conjunto para eliminar palavras repetidas
    conjunto_palavras = set(lista_palavras)

    # Convertendo o conjunto de volta para uma lista
    lista_sem_repeticao = list(conjunto_palavras)
    
    return lista_sem_repeticao


# Usa o 'idMembers' que cada um dos cartões possui e pega o nome dos usuários que criaram aquele cartão
def membersName(id_members):
    
    # Dicionario para guardar os nomes com as IDs de cada reporter e fotógrafo
    membros_nomes = {}
    
    # Com a lista de ids dos reporteres vai usar cada um deles para solicitar as informações de cada repórter, guardar em mamber_data, pegar o nome completo do repórter no dict recebido e depois criar um novo dict com id:nome completo
    for member_id in id_members:
        # Usa o id do usuário para pegar as informações de cada um
        response = requests.get(f'https://api.trello.com/1/members/{member_id}?key={API_KEY}&token={TOKEN}')
        member_data = response.json()
        # Através das informações recebidas pega o nome completo do usuário
        membro_nome = member_data['fullName']
        # Guarda tudo em um dicionário id:name
        membros_nomes[member_id] = membro_nome  
    
    # Colcoa o emoji de camera no nome dos fotografos
    for key, value in membros_nomes.items():
        if value == 'Magnus Nascimento':
            membros_nomes[key] = membros_nomes[key]+"📷"
        elif value == 'Alex Regis':
            membros_nomes[key] = membros_nomes[key]+"📷"
        elif value == 'adriano abreu':
            membros_nomes[key] = membros_nomes[key]+"📷"
            
    return membros_nomes

'''CHAMADAS DE FUNÇÕES: recebendo as informações que serão utilizadas''' 
# Chamada de função que pega todas as IDs
# Guarda os ids do membros de cada card em sua repectiva lisa
ID_members_pautas_feitas, ID_members_publicados, ID_members_flashes = getIds(pautas_feitas_cards_data, publicados_cards_data, flashes_do_dia_cards_data, 'idMembers')

# Recebe a lista "limpa", ou seja, sem listas dentro da lista e sem ID repetidos
id_members = removePalavrasRepetidas(simplificar_listas(ID_members_pautas_feitas, ID_members_publicados, ID_members_flashes))

# Recebe um dict com id : nome completo
membros_nomes = membersName(id_members)

# Junta todas as informações das duas listas em uma única lista para que tudo seja escrito em um único CSV
todas_as_pautas = pautas_feitas_cards_data + publicados_cards_data + flashes_do_dia_cards_data

'''ESCREVENDO NO CSV'''
# caminho = 'tabelas/impresso/dados_impresso.csv'
# # Escreve as informações selecionadas no arquivo dados_impresso.csv
# with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
    
#         csvwriter = csv.writer(csvfile)
        
#         # Cria as colunas
#         csvwriter.writerow(['IDmembers', 'reporter_fotografo', 'pauta', 'link', 'data'])
        
#         # Acessa cada um dos cards todas_as_pautas que possui todos os cards dos dois quadros
#         for card in todas_as_pautas:
            
#             '''
#             -> Esse trecho com o if só vale a pena quando a maioria card['idMembers'] tem mananho 1 e a escrita do arquivo fica ligeiramente mais rápida sem ele.
#             '''
            
#             # # Alguns idMembers possuem mais de um ID, transformando o seu value em uma lista
#             # # Portanto, para esses casos, precisamos de um loop para escrevermos as noticias para todos os membros participantes da pauta
#             # if len(card['idMembers']) == 1:
#             #     # idMembers com somente um ID são escritos no formato ['5f3d301a2c3e28123f5695f3']
#             #     # Para esses casos utilizamos o strip para remover [''] e manter tudo igual
#             #     membro = card['idMembers'][0].strip("[]'")
#             #     # membros_nomes.get(membro) é utilizado para pegar o o value referente a chave 'membro'
#             #     csvwriter.writerow([membro, membros_nomes.get(membro),card['name'], card['shortUrl'], card['dateLastActivity']])
#             # else:
            
#             # Cada card possui uma key contendo uma lista(value) com os ids dos jornalistas que estão envolvidos com aquela pauta
#             # Acessa cada elemento dessa lista
#             for membros in card['idMembers']:
                
#                 # Escreve as linhas em cada uma das colunas
#                 # 'membros' pega o id do membro
#                 # membros_nomes.get(membros) utiliza 'membros' para a cesar um dict onde cada id corresponde ao nome de um reporter id(key):reporter(value)
#                 # card['name']: titulo da notícia
#                 # card['shortUrl']: Link da notícia
#                 # card['dateLastActivity']: Data da ultima vez que o card foi modificado
#                 csvwriter.writerow([membros, membros_nomes.get(membros), card['name'], card['shortUrl'], card['dateLastActivity']])

# print('Arquivo dados_impresso.csv criado.')
