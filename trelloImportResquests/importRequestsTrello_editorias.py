import requests
import json
import csv
from datetime import datetime

'''CHAVES, TOKEN E REQUESTS INICIAIS'''
# Chave de API e Token de acesso fornecidos pelo Trello
API_KEY = '14d771355a6d5e6844830a88f5af930f'
TOKEN = 'ATTAab028c2c6b819b9460e748a857a73df70181117328e15bea185f109dcbfeecd317CFD298'

# ID do quadro/área de trabalho do Trello que você deseja extrair dados
# TRELLO_BOARD_ID = 'bLA2Uwel'
TRELLO_BOARD_ID = 'bLA2Uwel'
LIST_ID = TRELLO_BOARD_ID
# URL da API do Trello para obter listas e cartões
LISTS_URL = f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists'
CARDS_URL = f'https://api.trello.com/1/lists/{LIST_ID}/cards'
ACTIONS_URL = f'https://api.trello.com/1/cards/{{card_id}}/actions' # estou usando {{card_id}} dessa forma por conta da substituição feita dentro da função fetch_actions

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
    # elif lista['name'] == 'FLASHES  DO DIA':
    #     flashes_do_dia_list = lista

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

# # flashes_do_dia_list['id'] pega o id do quadro FLASHES DO DIA
# # Usa esse id pra conseguir os dados de cada um dos cartões dentro desse quadro
# response = requests.get(f'https://api.trello.com/1/lists/{flashes_do_dia_list['id']}/cards?key={API_KEY}&token={TOKEN}')
# # Dados dos cartões dentro do quadro FLASHES DO DIA
# flashes_do_dia_cards_data = response.json()

'''FUNÇÕES'''
# Pega todos os 'idMembers' de cada quadro e coloca em sua respectiva lista
# Recebe os dados de cada um dos cartões e a key para acessar determinada informação de um dict
def getIds(pautas_feitas_cards_data, publicados_cards_data, key):
# def getIds(pautas_feitas_cards_data, publicados_cards_data,flashes_do_dia_cards_data, key):
    # Listas para receber os ids dos jornalistas e fotógrafos no trello
    ID_members_pautas_feitas =[]
    ID_members_publicados = []
    # ID_members_flashes = []
    
    for item_pf in pautas_feitas_cards_data:
        ID_members_pautas_feitas.append(item_pf[key])
    
    for item_pub in publicados_cards_data:
        ID_members_publicados.append(item_pub[key])
    
    # for item_pub in flashes_do_dia_cards_data:
    #     ID_members_flashes.append(item_pub[key])
    
    return ID_members_pautas_feitas, ID_members_publicados
    # return ID_members_pautas_feitas, ID_members_publicados, ID_members_flashes


# Recebe uma lista de listas, remove as listas dentro da lista e unifica todas as informações na lista de "fora", juntando as listas em uma só     
def simplificar_listas(*args):
    lista_de_listas = args[0]+args[1]
    # lista_de_listas = args[0]+args[1]+args[2]
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

editoria = {} 
freq_edi = {}
def editoriasById(id_labels):
    
    # Dicionarios para guardar as editorias e as frequancias de uso de cada uma de acordo com id da label
    editoria = {} 
    freq_edi = {}
    
    for id in id_labels:
        
        # Usa o id do usuário para pegar as informações de cada um
        responseLabel = requests.get(f'https://api.trello.com/1/labels/{id}?key={API_KEY}&token={TOKEN}')
        
        if responseLabel.status_code == 200:
            try:
                # Recebendo as reditorias do impresso
                labelId_data = responseLabel.json()
                editorias = labelId_data.get('name', 'Nome não encontrado')
                editoria[id] = editorias
                # Recebendo a freqência que cada editoria aparece
                freqs = labelId_data.get('uses', 'frequencia de uso não encontrada')
                freq_edi[id] = freqs
                
            except requests.exceptions.JSONDecodeError:
                print(f"Erro ao decodificar JSON para a etiqueta com ID {id}")
        else:
            print(f"Erro na solicitação para a etiqueta com ID {id}. Status code: {responseLabel.status_code}")
    return editoria, freq_edi

# pega a data de criação do card de acordo com os primeiros elementos de seu card id, que representa uma dtaa em hexadecimal
def get_creation_date(card_id):
    timestamp = int(card_id[:8], 16)
    # return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.fromtimestamp(timestamp).isoformat()

# retorna as ações de movimentação de cada card entre os quadros
def fetch_actions(card_id):
    url = ACTIONS_URL.format(card_id=card_id)
    response = requests.get(url, params={'key': API_KEY, 'token': TOKEN})
    return response.json()

# recebe as ações e retorna a data em que elas ocorreram em um vetor []
def get_move_dates(actions):
    move_dates = []
    for action in actions:
        if action['type'] == 'updateCard' and 'listAfter' in action['data'] and 'listBefore' in action['data']:
            move_dates.append(action['date'])
    return move_dates

def dataCard_PautasFeitas(cardID):
    # retorna as ações de movimentação de cada card entre os quadros
    actions_pautasFeitas = fetch_actions(cardID)
    
    # recebe as ações e retorna a data em que elas ocorreram em um vetor []
    datas_pautas_feitas = get_move_dates(actions_pautasFeitas)
    # datas_pautas_feitas[-1]: recebe a ultima data do vetor que representa a data de quando foi movida para o quadro PAUTAS FEITAS
    # caso esteja vazio, recebe a data de criação do card
    data_pautasFeitas = datas_pautas_feitas[-1] if datas_pautas_feitas else get_creation_date(card['id'])
    
    return data_pautasFeitas

def dataCard_Publicados(cardID):
    # retorna as ações de movimentação de cada card entre os quadros
    actions_Publicados = fetch_actions(cardID)
    
    # recebe as ações e retorna a data em que elas ocorreram em um vetor []
    datas_publicados = get_move_dates(actions_Publicados)
    # datas_pautas_feitas[-2]: recebe a ultima data do vetor que representa a data de quando foi movida para o quadro PAUTAS FEITAS
    # caso esteja vazio, recebe a data de criação do card
    data_Publicados = datas_publicados[-2] if len(datas_publicados)>=2 else (datas_publicados[-1] if datas_publicados else get_creation_date(card['id']))
    
    return data_Publicados

def andamento(count, total):
    progress = (count / total) * 100
    steps = 10
    current_step = int(progress // steps)

    print(f"\rProgress: [{'•' * current_step}{' ' * (steps - current_step)}] - {progress:.2f}%", end="")

'''CHAMADAS DE FUNÇÕES: recebendo as informações que serão utilizadas''' 
# Chamada de função que pega todas as IDs de membros
# Guarda os ids dos membros de cada card em sua repectiva lisa
ID_members_pautas_feitas, ID_members_publicados = getIds(pautas_feitas_cards_data, publicados_cards_data, 'idMembers')
# ID_members_pautas_feitas, ID_members_publicados, ID_members_flashes = getIds(pautas_feitas_cards_data, publicados_cards_data,flashes_do_dia_cards_data, 'idMembers')

# Recebe a lista "limpa", ou seja, sem listas dentro da lista e sem ID repetidos
id_members = removePalavrasRepetidas(simplificar_listas(ID_members_pautas_feitas, ID_members_publicados))
# id_members = removePalavrasRepetidas(simplificar_listas(ID_members_pautas_feitas, ID_members_publicados, ID_members_flashes))

# Recebe um dict com id : nome completo
membros_nomes = membersName(id_members)

# Junta todas as informações das duas listas em uma única lista para que tudo seja escrito em um único CSV
todas_as_pautas = pautas_feitas_cards_data + publicados_cards_data
# todas_as_pautas = pautas_feitas_cards_data + publicados_cards_data + flashes_do_dia_cards_data

# Chamada de função que pega todas as IDs de labels
# Guarda os ids das labels de cada card em sua repectiva lisa
ID_labels_pautas_feitas, ID_labels_publicados = getIds(pautas_feitas_cards_data, publicados_cards_data, 'idLabels')
# ID_labels_pautas_feitas, ID_labels_publicados, ID_labels_flashes = getIds(pautas_feitas_cards_data, publicados_cards_data, flashes_do_dia_cards_data, 'idLabels')

# Recebe a lista "limpa", ou seja, sem listas dentro da lista e sem IDs repetidos
id_labels = removePalavrasRepetidas(simplificar_listas(ID_labels_pautas_feitas, ID_labels_publicados))
# id_labels = removePalavrasRepetidas(simplificar_listas(ID_labels_pautas_feitas, ID_labels_publicados, ID_labels_flashes))

# Recebem dicionarios com as editorias e frequencias de cada editoria para cada id de label
editoria, freq_edi = editoriasById(id_labels)

# print(id_members)
# print(membros_nomes)
# print(todas_as_pautas[-4])

'''ESCREVENDO NO CSV'''
caminho = 'tabelas/impresso/EDI_impresso.csv'
# Escreve as informações selecionadas no arquivo CSV
with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
    
        csvwriter = csv.writer(csvfile)
        
        # Cria as colunas
        csvwriter.writerow(['pauta', 'link', 'data', 'editoria', 'freq_edi'])
        count = 0
        # escreve os dados de PAUTAS FEITAS
        print("Atualizando dados de Pautas Feitas [1/2]:")
        for card in pautas_feitas_cards_data:
            
            # Cada card possui uma key contendo uma lista(value) com os ids dos jornalistas que estão envolvidos com aquela pauta
            # Acessa cada elemento dessa lista
            # for membros in card['idMembers']: 
                
                if card['idLabels'] == []:
                    
                    # Escreve as linhas em cada uma das colunas
                    # 'membros' pega o id do membro
                    # membros_nomes.get(membros) utiliza 'membros' para a cesar um dict onde cada id corresponde ao nome de um reporter id(key):reporter(value)
                    # card['name']: titulo da notícia
                    # card['shortUrl']: Link da notícia
                    # card['dateLastActivity']: Data da ultima vez que o card foi modificado
                    # 'Pauta sem editoria' para o caso de não tem editoria adicionada no card
                    csvwriter.writerow([card['name'], card['shortUrl'], dataCard_PautasFeitas(card['id']), 'Pauta sem editoria', 0])
                
                else:
                    
                    # Cada card possui uma key contendo uma lista(value) com os ids das labels de cada editoria
                    # Acessa cada elemento dessa lista
                    for lbl in card['idLabels']:
                        
                        # editoria.get(lbl): editoria de acordo com o id da label
                        # freq_edi.get(lbl): frequencia de determinada editoria de acordo com o id da label
                        csvwriter.writerow([card['name'], card['shortUrl'], dataCard_PautasFeitas(card['id']), editoria.get(lbl), int(freq_edi.get(lbl))])
                count += 1
                andamento(count, len(pautas_feitas_cards_data))
        
        # escreve os dados de ✅PUBLICADOS
        print("\nAtualizando dados de Publicados [2/2]:")
        count = 0
        for card in publicados_cards_data:
            
            if card['idLabels'] == []:
                
                csvwriter.writerow([card['name'], card['shortUrl'], dataCard_Publicados(card['id']), 'Pauta sem editoria', 0])
            
            else:
                
                for lbl in card['idLabels']:
                    
                    csvwriter.writerow([card['name'], card['shortUrl'], dataCard_Publicados(card['id']), editoria.get(lbl), int(freq_edi.get(lbl))])
            count += 1
            andamento(count, len(publicados_cards_data))
        
        # # escreve os dados de FLASHES DO DIA
        # print("\nAtualizando dados de Flashes do Dia [3/3]:")
        # count = 0
        # for card in flashes_do_dia_cards_data:
            
        #     if card['idLabels'] == []:
                
        #         csvwriter.writerow([card['name'], card['shortUrl'], dataCard_PautasFeitas(card['id']), 'Pauta sem editoria', 0])
            
        #     else:
                
        #         for lbl in card['idLabels']:
                    
        #             csvwriter.writerow([card['name'], card['shortUrl'], dataCard_PautasFeitas(card['id']), editoria.get(lbl), int(freq_edi.get(lbl))])
        #     count += 1
        #     andamento(count, len(flashes_do_dia_cards_data))

print('\nArquivo EDI_impresso.csv criado.')
