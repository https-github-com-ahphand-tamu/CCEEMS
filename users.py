import psycopg2
from db import get_database_connection

def get_all_users():
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users;")
    users_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return users_data
