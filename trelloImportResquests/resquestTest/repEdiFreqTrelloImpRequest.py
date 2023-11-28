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

'''FUNÇÕES'''
# Pega todos os 'idMembers' de cada quadro e coloca em sua respectiva lista
# Recebe os dados de cada um dos cartões e a key para acessar determinada informação de um dict
def getIds(pautas_feitas_cards_data, publicados_cards_data, key):
    # Listas para receber os ids dos jornalistas e fotógrafos no trello
    ID_members_pautas_feitas =[]
    ID_members_publicados = []
    
    for item_pf in pautas_feitas_cards_data:
        ID_members_pautas_feitas.append(item_pf[key])
    
    for item_pub in publicados_cards_data:
        ID_members_publicados.append(item_pub[key])
    
    return ID_members_pautas_feitas, ID_members_publicados


# Recebe uma lista de listas, remove as listas dentro da lista e unifica todas as informações na lista de "fora", juntando as listas em uma só     
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


# Usa o 'idMembers' que cada um dos cartões possui e pega o nome dos usuários que criaram aquele cartão
def membersName(id_members):
    
    # Variável para guardar os nomes com as IDs de cada reporter e fotógrafo
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

editoria = {} 
freq_edi = {}
def editoriasById(id_labels):  
    for id in id_labels:
        # Usa o id do usuário para pegar as informações de cada um
        responseLabel = requests.get(f'https://api.trello.com/1/labels/{id}?key={API_KEY}&token={TOKEN}')
        
        # labelId_data = responseLabel.json()
        # # Através das informações recebidas pega o nome completo do usuário
        # editorias = labelId_data['name']
        # # Guarda tudo em um dicionário id:name
        # editoria[id] = editorias
        print(responseLabel.text)
        if responseLabel.status_code == 200:
            try:
                # Recebendo as reditorias do impresso
                labelId_data = responseLabel.json()
                editorias = labelId_data.get('name', 'Nome não encontrado')
                editoria[id] = editorias
                # Recebendo a freqência que cada editoria aparece
                freqs = labelId_data.get('uses', 'frequencia de uso nãom encontrada')
                freq_edi[id] = freqs
                
            except requests.exceptions.JSONDecodeError:
                print(f"Erro ao decodificar JSON para a etiqueta com ID {id}")
        else:
            print(f"Erro na solicitação para a etiqueta com ID {id}. Status code: {responseLabel.status_code}")

'''CHAMADAS DE FUNÇÕES: recebendo as informações que serão utilizadas''' 
# Chamada de função que pega todas as IDs
# Guarda os ids do membros de cada card em sua repectiva lisa
ID_members_pautas_feitas, ID_members_publicados = getIds(pautas_feitas_cards_data, publicados_cards_data, 'idMembers')

# Recebe a lista "limpa", ou seja, sem listas dentro da lista e sem ID repetidos
id_members = removePalavrasRepetidas(simplificar_listas(ID_members_pautas_feitas, ID_members_publicados))

# Recebe um dict com id : nome completo
membros_nomes = membersName(id_members)

# Junta todas as informações das duas listas em uma única lista para que tudo seja escrito em um único CSV
todas_as_pautas = pautas_feitas_cards_data + publicados_cards_data

ID_labels_pautas_feitas, ID_labels_publicados = getIds(pautas_feitas_cards_data, publicados_cards_data, 'idLabels')
id_labels = removePalavrasRepetidas(simplificar_listas(ID_labels_pautas_feitas, ID_labels_publicados))

editoriasById(id_labels)

'''ESCREVENDO NO CSV'''
# Escreve as informações selecionadas no arquivo CSV
with open('EDI_impresso.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['IDmembers', 'Reporter ou fotografo', 'Pauta', 'link', 'data', 'editoria'])
        for card in todas_as_pautas:
            
            for membros in card['idMembers']: 
                
                # if len(card['idMembers']) == 0:
                #     membro = '-'
                # else:
                #     membro = membros
                
                # for lbl in card['idLabels']:
                    
                #     if len(card['idMembers']) == 0:
                #         id_lbl = '-'
                #     else:
                #         id_lbl = lbl
                    
                #     csvwriter.writerow([membro,membros_nomes.get(membros, '-'),card['name'], card['shortUrl'],card['dateLastActivity'], editoria.get(id_lbl, '-')])
                
                if card['idLabels'] == []:
                    csvwriter.writerow([membros, membros_nomes.get(membros), card['name'], card['shortUrl'], card['dateLastActivity'], '-'])
                else:
                    for lbl in card['idLabels']:
                        csvwriter.writerow([membros, membros_nomes.get(membros), card['name'], card['shortUrl'], card['dateLastActivity'], editoria.get(lbl, None)])

print('Aquivo CSV criado.')
