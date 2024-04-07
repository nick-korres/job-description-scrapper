import os
import sqlite3
from db_connect import db_file,init_db_script

def init_db():
    # Delete the db file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
    # (Re)create the file
    with open(db_file,"w"):
        print("Creating new db")
        pass
    conn = sqlite3.connect(db_file)  
    cursor = conn.cursor()
    with open(init_db_script) as sql_file:
        sql_queries = sql_file.read().split(";")
        print("Running db init script")
        
        for query in sql_queries:
            if query.strip():  # Skip empty statements
                cursor.execute(query)
        conn.commit()
        conn.close()

if __name__ == "__main__" :
    init_db()