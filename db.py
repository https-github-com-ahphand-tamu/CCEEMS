import psycopg2
from psycopg2 import Error
import os

global_conn = None
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_database_connection():
    global global_conn

    if global_conn is None:
        try:
            global_conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except Error as e:
            print(f"Error connecting to database: {e}")

    return global_conn

if __name__ == "__main__":
    # Get the database connection
    conn = get_database_connection()

    # Use the database connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM your_table")

    # Close the connection when done (optional)
    conn.close()
