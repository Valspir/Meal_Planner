import requests
import json
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

api_key = '5ca5524812decbad07ce42bf3cde3deb'
api_token = 'ATTAa18d7513da3a17144160fceabdd1531bd6883c5d671c6a5f7376f56776223c4234AFEE80'

board_id = '63ea070bd63a50cd95819fb8'
toTry = '63ea0713a50e8a50c49ced94'
weeklyFood = '63ea071c183540b79ced3e91'
url = 'https://api.trello.com/1/search?card_fields=name,labels&query=label:Dinner&key={ak}&token={at}'
url = url.format(list_id=toTry,ak=api_key,at=api_token)

r = requests.get(url)
rd = -1
try:
    rd = json.loads(r.text)
except:
    print(r.text)

print("--")
cardID = rd['cards'][1]['id']
print(rd['cards'][1]['name'])
url = 'https://api.trello.com/1/cards/{id}/checklists?key={ak}&token={at}'
url = url.format(id=cardID,list_id=toTry,ak=api_key,at=api_token)
r = requests.get(url)
rd = -1
try:
    rd = json.loads(r.text)
except:
    print(r.text)

print("--")
for x in range(len(rd[0]['checkItems'])):
    print(rd[0]['checkItems'][x]['name'])


url = 'https://api.trello.com/1/cards/{id}/customFieldItems?key={ak}&token={at}'
url = url.format(id=cardID,list_id=toTry,ak=api_key,at=api_token)
r = requests.get(url)
rd = -1
try:
    rd = json.loads(r.text)
except:
    print(r.text)
meatValue = rd[0]


for x in range(len(rd)):
    #print(rd[x])
    fieldID = rd[x]['idCustomField']
    meatID = 0
    if('idValue' in rd[x].keys()):
        meatID = rd[x]['idValue']
    url = 'https://api.trello.com/1/customFields/{id}?key={ak}&token={at}'
    url = url.format(id=fieldID,ak=api_key,at=api_token)
    r = requests.get(url)
    res = -1
    try:
        res = json.loads(r.text)
    except:
        print(r.text)
    print('--')
    print(res['name'])
    if('options' in res.keys()):
        for j in range(len(res['options'])):
            if(res['options'][j]['id'] == meatID):
                print(res['options'][j]['value']['text'])
        #pprint.pprint(res['options'])
    else:
        print(rd[x]['value'])


chosenFoods = []
for i in range(4):
    url = 'https://api.trello.com/1/search?card_fields=name,labels&query=label:Dinner&key={ak}&token={at}'
    url = url.format(list_id=toTry,ak=api_key,at=api_token)

    r = requests.get(url)
    rd = -1
    try:
        rd = json.loads(r.text)
    except:
        print(r.text)

    cardNumber = round((random.random()*100)%len(rd['cards'])-1)
    while(rd['cards'][cardNumber]['id'] in chosenFoods):
        cardNumber = round((random.random()*100)%len(rd['cards'])-1)
    chosenFoods.append(rd['cards'][cardNumber]['id'])
    print(rd['cards'][cardNumber])
    '''url = 'https://api.trello.com/1/cards/{id}?idList={idList}key={ak}&token={at}'
    url = url.format(id=rd['cards'][cardNumber]['id'],idList=weeklyFood,ak=api_key,at=api_token)

    r = requests.get(url)
    rd = -1
    try:
        rd = json.loads(r.text)
    except:
        print(r.text)'''
    


url = 'https://api.trello.com/1/boards?key={ak}&token={at}'
url = url.format(ak=api_key,at=api_token)

r = requests.get(url)
rd = -1
try:
    rd = json.loads(r.text)
except:
    print(r.text)

'''
ok so the plan is:

-query trello api for cards on the board that have a label, depending if I want breakfast/lunch/dinner/snacks
-pick some of those cards based on the meat, affordability and healthiness
-move the cards to weekly plan list and copy the card/ingredients a shopping list
-give feedback weekly/adjust settings like preferred meat type/tastes
-profit?

:3


'''
