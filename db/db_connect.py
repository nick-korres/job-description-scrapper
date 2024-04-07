import sqlite3

init_db_script="./db/init_db.sql"
db_file="./db/cache.sqlite"

def get_db_cursor():
    con = sqlite3.connect(db_file)
    return con.cursor()


def run_query(query: str,parameters:list[str] = None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # foreign_keys are enabled per connection or on compilation https://www.sqlite.org/foreignkeys.html
    cursor.execute("PRAGMA foreign_keys = ON;")
    try:
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        result = cursor.fetchall()  # or other fetch methods
        conn.commit()
        return result
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()
