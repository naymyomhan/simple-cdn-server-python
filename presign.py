
import uuid
from database import establish_connection, init_db
import mysql.connector
from datetime import datetime,timedelta
from response import success_response,fail_response






def insert_presign(cursor, connection, presign_key, file_name):
    try:
        insert_query = """
        INSERT INTO presigns (presign_key, file_name, created_at) VALUES (%s, %s, %s)
        """
        created_at = datetime.now()
        presign_data_with_datetime = (presign_key, file_name, created_at)
        
        cursor.execute(insert_query, presign_data_with_datetime)
        connection.commit()

        data = {
            "presign_key": presign_key,
            "file_name": file_name,
            "created_at": created_at.isoformat()
        }

        return success_response("Success",data)
    except Exception as e:
        return fail_response("Something went wrong")











def is_valid_presign_key(cursor, presign_key):
    if len(presign_key) != 36:
        return False

    try:
        uuid.UUID(presign_key)
    except ValueError:
        return False









    

