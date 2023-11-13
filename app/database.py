import os
from dotenv import load_dotenv
from mysql.connector import pooling
from response import success_response,fail_response

load_dotenv()
# Set your database details
db_config = {
    'host': os.environ.get('HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('PASSWORD'),
    'database': os.environ.get('DATABASE'),
}

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)



def establish_connection():
    return connection_pool.get_connection()


def close_connection(cursor, connection):
    cursor.close()
    connection.close()



def init_db(cursor):
    create_presign_table_query = '''
    CREATE TABLE IF NOT EXISTS presigns (
        id INT AUTO_INCREMENT PRIMARY KEY,
        presign_key VARCHAR(255),
        file_path VARCHAR(255),
        file_name VARCHAR(255),
        file_type VARCHAR(255),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    '''
    cursor.execute(create_presign_table_query)


try:
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    init_db(cursor)
    print("Database initialized successfully.")
except Exception as e:
    print(f"Error initializing database: {e}")
finally:
    close_connection(cursor, connection)




