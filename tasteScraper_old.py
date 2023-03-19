import requests
from bs4 import BeautifulSoup
import pprint
import re

loadingArr = ['|', '/', '-', '\\']
currentIndex = 0
for i in range(20,100):

    url = "https://www.taste.com.au/dinner/search?page="+str(i)+"&sort=recent"
    r = requests.get(url)
    #print(r.text)
    allLinks = []
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        if("/recipes/" in link.get('href') and "/recipes/collections" not in link.get('href') and link.get('href').split("#")[0] not in allLinks):
            #print(link.get('href').split("#")[0])
            allLinks.append(link.get('href').split("#")[0])

    with open('ingredientList', 'a') as outputFile:
        for link in allLinks:
            if(currentIndex == len(loadingArr)-1) :
                currentIndex = -1
            currentIndex+=1
            print("Reading page: " + str(i) + " " + loadingArr[currentIndex], end='\r')
            url = "https://www.taste.com.au"+link
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            x = soup.find("div", {"id": "tabIngredients"})
            x = str(x)

            soup = BeautifulSoup(x,'html.parser')
            for el in soup.find_all('div', { 'class' : 'ingredient-description'}):
                outputFile.write(el.get('data-raw-ingredient')+"\n")

#lines = re.sub('^[a-zA-Z0-9_.-]*$','', x)
#print(lines)
#for line in lines.split('\n'):
#    pprint.pprint(line)
