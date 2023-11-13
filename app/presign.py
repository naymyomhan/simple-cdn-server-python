
import uuid
from database import close_connection
from datetime import datetime,timedelta
from response import fail_response






def insert_presign(cursor, connection, presign_key, file_name, file_path, file_type):
    try:
        insert_query = """
        INSERT INTO presigns (presign_key, file_name, file_path, file_type, created_at) VALUES (%s, %s, %s, %s, %s)
        """
        created_at = datetime.now()
        presign_data_with_datetime = (presign_key, file_name, file_path, file_type, created_at)
        
        cursor.execute(insert_query, presign_data_with_datetime)

        data = {
            "key": presign_key,
            "name": file_name,
        }

        return data
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

    cursor.execute(select_query, (presign_key, datetime.now() - timedelta(minutes=50), datetime.now()))
    row = cursor.fetchone()

    if row:
        return True
    else:
        return False


    
    
def getPresignInfo(cursor, presign_key):
    # select_query = 'SELECT file_name, file_path, file_type FROM presigns WHERE presign_key = %s'

    select_query = '''
    SELECT file_name, file_path, file_type FROM presigns WHERE presign_key = %s
    '''

    try:
        cursor.execute(select_query, (presign_key,))
        result = cursor.fetchone()

        if result:
            file_name, file_path, file_type = result
            return {'file_name': file_name, 'file_path': file_path, 'file_type': file_type}
        else:
            return None

    except Exception as e:
        print(f"Error executing query: {e}")
        return None

    









    

