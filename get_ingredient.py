import sqlite3
import json
import re
import os

'''
What info do I need?
-Meat type
-Amount
-Preperation Instructions
'''
def createDB(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def addWord(conn, values):
    sql = """INSERT INTO Words(Word,Type,Subtype) VALUES(?,?,?)"""
    c = conn.cursor()
    c.execute(sql,values)
    conn.commit()

def createRecipeTable(conn):
    sql = """CREATE TABLE IF NOT EXISTS Words (
        id integer PRIMARY KEY,
        Word varchar NOT NULL,
        Type varchar NOT NULL,
        Subtype varchar NOT NULL
    )"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit


conn = createDB("words.db")
createRecipeTable(conn)

wordTypes = ['Measurement','Ingredient','Instruction', "N\A"]
wordSubtypes = ['Number', 'UOM', 'Meat', 'Vegetable', 'Spice', 'Other']
wordArray = []
recipeDB = createDB("recipes.db")
sql = 'SELECT ingredients FROM Recipes'
recipeCur = recipeDB.cursor()
res = recipeCur.execute(sql)
for ingredients in res:
    ingredientArr = json.loads(ingredients[0])
    for ingredient in ingredientArr:
        for word in ingredient.split(" "):
            word = re.split("[^a-zA-Z0-9]", word)
            for w in word:
                type = -1
                subtype = -1
                if(w not in wordArray and len(word) > 0):
                    print("--"*10)
                    print(ingredient)
                    print(w)
                    print("--"*10)
                    typeDone = 0
                    while(not typeDone):
                        type = input("Word Type:\n  1 - Measurement\n  2 - Ingredient\n  3 - Instruction\n  4 - N\A\nSelection: ")
                        try:
                            type = str(wordTypes[int(type)-1])
                            typeDone = 1
                        except:
                            print("Please choose 1-4!")
                    if(type != "N\A"):
                        subtypeDone = 0
                        while(not subtypeDone):
                            subtype = input("Word Subtype:\n  1 - Number\n  2 - UOM\n  3 - Meat\n  4 - Vegetable\n  5 - Spice\n  6 - Other\nSelection: ")
                            try:
                                subtype = str(wordSubtypes[int(subtype)-1])
                                subtypeDone = 1
                            except:
                                print("Please choose 1-6!")
                        addWord(conn,(str(w), type, subtype))
                        print(str(w) +" - Type: " + type + " Subtype: "+ subtype)
                        wordArray.append(w)
                    os.system("clear")
print(len(wordArray))
