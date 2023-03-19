import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import re
def createDB(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def addRecipe(conn, values):
    sql = """INSERT INTO Recipes(recipeName,ingredientCount,ingredients,stepCount,steps,servings,prepTime,cookTime,saves) VALUES(?,?,?,?,?,?,?,?,?)"""
    c = conn.cursor()
    c.execute(sql,values)
    conn.commit()

def createRecipeTable(conn):
    sql = """CREATE TABLE IF NOT EXISTS Recipes (
        id integer PRIMARY KEY,
        recipeName text NOT NULL,
        ingredientCount integer NOT NULL,
        ingredients varchar NOT NULL,
        stepCount integer NOT NULL,
        steps varchar NOT NULL,
        servings integer NOT NULL,
        prepTime integer NOT NULL,
        cookTime integer NOT NULL,
        saves integer NOT NULL
    )"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit

allLinks = []

conn = createDB("recipes.db")
createRecipeTable(conn)
i = 1
r = requests.get("https://www.taste.com.au/dinner/search?page="+str(i)+"&sort=rating#")
soup = BeautifulSoup(r.text,'html.parser')
while(len(soup.find('div', {'class':'tiled-list'})) > 1):
    recipeCount=0
    a = soup.find_all('a')
    for link in a:
        if('/recipes/' in link.get('href') and '/recipes/collections' not in link.get('href') and link.get('href').split('#')[0] not in allLinks and '.html' not in link.get('href')):
            allLinks.append(link.get('href').split('#')[0])
            try:
                r = requests.get("https://www.taste.com.au"+link.get('href').split("#")[0])
            except:
                print("Connection error on line 100, page: "+str(i))
                exit()
            soup = BeautifulSoup(r.text,'html.parser')
            saveCount = -1
            try:
                saveCount = soup.find_all('div', {'class':'saved-counter'})[0].find('span', {'class':'counter'}).get('data-count')
            except:
                continue
            recipeTitle = soup.find('div', {'class':'recipe-title-container'}).find('h1').text.strip("\n")
            servings = -1
            cookTime = -1
            prepTime = -1
            try:
                allRecipeInfo = soup.find('ul', {'class':'recipe-cooking-info'})
                allRecipeInfo = allRecipeInfo.find_all('li')
                for info in allRecipeInfo:
                    if('servings' in info.text):
                        servings = int(re.sub("\D+", "", info.find('em').text.strip()))
                    if('prep' in info.text):
                        prepTime = int(re.sub("\D+", "", info.find('em').text.strip()))
                    if('cook' in info.text):
                        cookTime = int(re.sub("\D+", "", info.find('em').text.strip()))
            except:
                #print("Error")
                continue

            allIngredients = soup.find('div', {'id':'tabIngredients'})
            allIngredients = allIngredients.find_all('div', {'class':'ingredient-description'})
            ingredientCount = 1
            ingredientArray = []
            for ingredient in allIngredients:
                ingredientArray.append(ingredient.get('data-raw-ingredient'))
                ingredientCount+=1


            allSteps = soup.find('div', {'id':'tabMethodSteps'})
            allSteps = allSteps.find_all('li')
            stepCount=1
            stepArray = []
            for step in allSteps:
                stepNumber = step.find('div', {'class':'recipe-method-step-number'}).find('a').text
                instruction = step.find('div', {'class':'recipe-method-step-content'}).text.strip()
                stepArray.append(instruction)
                stepCount+=1
            print("Page: " + str(i) + " Recipe: " + str(recipeCount)+(" "*50), end='\r')
            addRecipe(conn,(recipeTitle,ingredientCount,json.dumps(ingredientArray),stepCount,json.dumps(stepArray),servings,prepTime,cookTime,saveCount))
            recipeCount+=1
    i+=1
    try:
        r = requests.get("https://www.taste.com.au/dinner/search?page="+str(i)+"&sort=rating#")
    except:
        print("Connection error on line 100, page: "+str(i))
        exit()
    soup = BeautifulSoup(r.text,'html.parser')
