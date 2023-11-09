
import uuid
from database import close_connection, establish_connection, init_db
import mysql.connector
from datetime import datetime,timedelta
from response import success_response,fail_response






def insert_presign(cursor, connection, presign_key, file_name, path, file_type):
    try:
        insert_query = """
        INSERT INTO presigns (presign_key, file_name, path, file_type, created_at) VALUES (%s, %s, %s, %s, %s)
        """
        created_at = datetime.now()
        presign_data_with_datetime = (presign_key, file_name, path, file_type, created_at)
        
        cursor.execute(insert_query, presign_data_with_datetime)

        data = {
            "presign_key": presign_key,
            "file_name": file_name,
            "created_at": created_at.isoformat()
        }

        return success_response("Success",data)
    except Exception as e:
        close_connection(cursor, connection)
        return fail_response(f"Presign failed: {str(e)}")






def is_valid_presign_key(cursor, presign_key):
    if len(presign_key) != 36:
        return False
    
    try:
        uuid.UUID(presign_key)
    except ValueError:
        return False
    
    select_query = '''
    SELECT * FROM presigns WHERE presign_key = %s AND created_at >= %s AND created_at <= %s
    '''

    cursor.execute(select_query, (presign_key, datetime.now() - timedelta(minutes=1), datetime.now()))
    row = cursor.fetchone()

    if row:
        return True
    else:
        return False


    
    
def get_file_name_by_presign_key(cursor, presign_key):
    select_query = 'SELECT file_name FROM presigns WHERE presign_key = %s'

    try:
        cursor.execute(select_query, (presign_key,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    









    

