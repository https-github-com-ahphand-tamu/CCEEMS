import psycopg2
from db import get_database_connection

conn = get_database_connection()

create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(255) PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255)
    ); 
        INSERT INTO users (username, first_name, last_name)
        VALUES
            ('dummyuser1@example.com', 'John', 'Doe'),
            ('dummyuser2@example.com', 'Jane', 'Smith')
            ;
"""
cursor = conn.cursor()
cursor.execute(create_users_table)
conn.commit()
cursor.close()