import requests
import json
import csv


# Substitua 'SUA_CHAVE' e 'SEU_TOKEN' pelos valores obtidos ao criar sua chave de API e token de acesso
API_KEY = '14d771355a6d5e6844830a88f5af930f'
TOKEN = 'ATTA58f75daa52546fed11141ce22e6ac3d978755aa1dba5b112f1e606bf668da1dcE6A7BB6A'

# ID do quadro do Trello que você deseja extrair dados
# TRELLO_BOARD_ID = 'bLA2Uwel'
TRELLO_BOARD_ID = 'bLA2Uwel'
LIST_ID = TRELLO_BOARD_ID
# URL da API do Trello para obter listas e cartões
LISTS_URL = f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists'
CARDS_URL = f'https://api.trello.com/1/lists/{LIST_ID}/cards'

# Lista para armazenar dados
data = []

# Obter listas do quadro
response = requests.get(f'{LISTS_URL}?key={API_KEY}&token={TOKEN}')
lists_data = response.json()

pautas_feitas_list = None
publicados_list = None

# Guarda os dois quadros que eu vou precisar
for lista in lists_data:
    if lista['name'] == 'PAUTAS FEITAS':
        pautas_feitas_list = lista
    elif lista['name'] == '✅ PUBLICADOS':
        publicados_list = lista


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


ID_members_pautas_feitas =[]
ID_members_publicados = []
# Pega todos os 'idMembers' de cada quadro e coloca em sua respectiva lista
def getIdMembers(pautas_feitas_cards_data, publicados_cards_data):
    for item_pf in pautas_feitas_cards_data:
        ID_members_pautas_feitas.append(item_pf['idMembers'])
    
    for item_pub in publicados_cards_data:
        ID_members_publicados.append(item_pub['idMembers'])


# Recebe uma lista de listas, remove as listas dentro da lista e unifica todas as informações na lista de "fora" e junta as duas listas em uma só     
def simplificar_listas(*args):
    lista_de_listas = args[0]+args[1]
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

# Variável para guardar os nomes com as IDs de cada reporter e fotógrafo
membros_nomes = {}
# Usa o 'idMembers' que cada um dos cartões possui e pega o nome dos usuários que criaram aquele cartão
def membersName(id_members):   
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
    
# Chamada de função que pega todas as IDs
getIdMembers(pautas_feitas_cards_data, publicados_cards_data)

# Recebe a lista "limpa", ou seja, sem listas dentro da lista e sem ID repetidos
id_members = removePalavrasRepetidas(simplificar_listas(ID_members_pautas_feitas, ID_members_publicados))
    
membersName(id_members)
#dicionario_ordenado = dict(sorted(membros_nomes.items(), key=lambda item: item[1].lower()))

print("'ID': 'name': \n",membros_nomes)
print(type(membros_nomes))
print(type(pautas_feitas_cards_data))


# Junta todas as informações das duas listas em uma única lista para que tudo seja escrito em um único CSV
todas_as_pautas = pautas_feitas_cards_data + publicados_cards_data


# Escreve as informações selecionadas no arquivo CSV
with open('dados_impresso.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['IDmembers', 'Reporter ou fotografo', 'Pauta', 'link', 'data'])
        for card in todas_as_pautas:
            # Alguns idMembers possuem mais de um ID, transformando o seu value em uma lista
            # Portanto, para esses casos, precisamos de um loop para escrevermos as noticias para todos os membros participantes da pauta
            if len(card['idMembers']) == 1:
                # idMembers com somente um ID são escritos no formato ['5f3d301a2c3e28123f5695f3']
                # Para esses casos utilizamos o strip para remover [''] e manter tudo igual
                membro = card['idMembers'][0].strip("[]'")
                # membros_nomes.get(membro) é utilizado para pegar o o value referente a chave 'membro'
                csvwriter.writerow([membro, membros_nomes.get(membro),card['name'], card['shortUrl'], card['dateLastActivity']])
            else:
                for membros in card['idMembers']: 
                    csvwriter.writerow([membros, membros_nomes.get(membros), card['name'], card['shortUrl'], card['dateLastActivity']])
