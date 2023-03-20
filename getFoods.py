import sqlite3
from sqlite3 import Error
import json

f = open("foods.json","r")
foodJson = json.load(f)

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


def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        sql = """ CREATE TABLE IF NOT EXISTS foods (
                                            id int PRIMARY KEY,
                                            Food varchar NOT NULL,
                                            Class varchar NOT NULL
                                        ); """
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)



def main():
    database = r"foods.db"

    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn)
        count = 0
        # create projects table

        sql = 'INSERT INTO foods (Food,Class) VALUES(?,?)'
        c = conn.cursor()
        for foodClass in foodJson:
            for food in foodJson[foodClass]:
                count+=1
                c.execute(sql, (food,foodClass))
        conn.commit()
        print(count)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
