import sqlite3
import pprint
import json
import spacy
import re

# Load the Spacy English language model
nlp = spacy.load('en_core_web_sm')


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

recipeDBConn = create_connection('recipes.db')
foodDBConn = create_connection('foods.db')
recipeCur = recipeDBConn.cursor()
foodCur = foodDBConn.cursor()
allInfo = []
i = 0


def is_instruction(token):
    # Check if the token is a verb
    if token.pos_ == 'VERB':
        # Check if the token is followed by other verbs or verb phrases in the sentence
        if any([t.pos_ == 'VERB' or t.dep_ == 'aux' for t in token.rights]):
            return True
    return False

def getIngredient(ingredient):
    doc = nlp(ingredient)
    extracted_info = []
    ingredientBreakdown = ()
    for token in doc:
        if token.pos_ == 'NUM':
            extracted_info.append(('Measurement', 'Number', token.text))
        elif token.text in ['tsp', 'tbsp', 'cup', 'oz', 'lb', 'g', 'kg']:
            extracted_info.append(('Measurement', 'UOM', token.text))
        elif(is_instruction(token)):
            extracted_info.append(('Instruction', 'Other', token.text))
        else:
            text = str(token.text).lower()
            text = re.sub('[^a-zA-Z]','',text)
            if(len(text) > 0):
                sql = "SELECT Class FROM foods WHERE food='"+text+"'"
                res = foodCur.execute(sql).fetchall()
                if(len(res) != 0):
                    extracted_info.append(('Ingredient', res[0][0], token.text))
                else:
                    extracted_info.append(('Ingredient Attribute', 'Other', token.text))
    return extracted_info

'''
sql = 'SELECT * FROM Recipes ORDER BY saves DESC'
res = recipeCur.execute(sql)
for r in res:
    ingredientList = json.loads(r[3])
    for ingredient in ingredientList:
        print(i,end='\r')
        i+=1
        allInfo.append(getIngredient(ingredient))
pprint.pprint(allInfo)'''

ing = getIngredient("10 lamb cutlet")
sql = "SELECT * FROM Products WHERE Description LIKE '%"
j = 0
for i in ing:
    if(i[0] == 'Ingredient' or i[0] == 'Ingredient Attribute'):
        if(j != 0):
            sql += " AND Description LIKE '%"
        sql += i[2]+"%'"
        j+=1

print(sql)
productDBConn = create_connection('productInfo.db')
productCur = productDBConn.cursor()
pprint.pprint(productCur.execute(sql).fetchall())
