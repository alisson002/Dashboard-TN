import requests
import json
import csv
from datetime import datetime

def get_creation_date(card_id):
    timestamp = int(card_id[:8], 16)
    return datetime.fromtimestamp(timestamp).isoformat()

print(get_creation_date('663e42236f04336e5546e4b0'))

# Chave de API e Token de acesso fornecidos pelo Trello
API_KEY = '14d771355a6d5e6844830a88f5af930f'
TOKEN = 'ATTA58f75daa52546fed11141ce22e6ac3d978755aa1dba5b112f1e606bf668da1dcE6A7BB6A'

# ID do quadro/área de trabalho do Trello que você deseja extrair dados
TRELLO_BOARD_ID = 'bLA2Uwel'

# URL da API do Trello para obter listas e cartões
# LISTS_URL = f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists'
# CARDS_URL = f'https://api.trello.com/1/lists/{{list_id}}/cards'
ACTIONS_URL = f'https://api.trello.com/1/cards/{{card_id}}/actions'

def fetch_actions(card_id):
    url = ACTIONS_URL.format(card_id=card_id)
    response = requests.get(url, params={'key': API_KEY, 'token': TOKEN})
    return response.json()

actions = fetch_actions('6300102290dc2520fe9e2e65')

print(actions)

def get_move_dates(actions):#se o card está em publicados devo pegar a penultima data e se estiver em pautas feitas pego a ultima data. flashes do dia éa data de criação
    #como será pelo id do card faremos com um if else,para caso tenha mais de uma data pega a penultima e se só tiver uma pegar a ultima
    #ou será com 3 for, sendo um pra cada quadro usado ao invez de juntar todos os quadros em um só. TALVEZ SEJA O IDEAL, POIS DESSA FORMA PODEMOS PEGAR SEPARADAMENTE OS DADOS E EM PUBLICADOS PEGAR A PENULTIMA DATA E EM PAUTAS FEITAS PEGAR A ULTIMA.
    move_dates = []
    for action in actions:
        if action['type'] == 'updateCard' and 'listAfter' in action['data'] and 'listBefore' in action['data']:
            move_dates.append(action['date'])
    return move_dates

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

datas = get_move_dates(actions)
print(datas)
print(datas[-1])

print(get_creation_date('6300102290dc2520fe9e2e65'))

# DeprecationWarning: datetime.datetime.utcfromtimestamp() is 
# deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.fromtimestamp(timestamp, datetime.UTC).  
#   return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print("•",end=" ")
print("•",end=" ")
print("•",end=" ")