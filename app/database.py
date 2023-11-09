import mysql.connector
from datetime import datetime,timedelta
from mysql.connector import pooling
from response import success_response,fail_response

# Set your database details
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': "",
    'database': 'cdn_server'
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








