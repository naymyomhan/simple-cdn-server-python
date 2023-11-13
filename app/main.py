import base64
import os
import secrets
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from uploader.file_uploader import uploadFile
from helper import checkFileType, ramdomFilename
from constants import ALLOWED_EXTENSIONS, STORAGE_PATH
from uploader.image_uploader import uploadImage
from presign import getPresignInfo, is_valid_presign_key, insert_presign
from response import success_response, fail_response
from database import establish_connection, init_db, close_connection

app = Flask(__name__)
load_dotenv()



def verify_api_key(api_key):
    stored_api_key = os.environ.get('API_KEY')
    return api_key is not None and secrets.compare_digest(api_key, stored_api_key)

@app.before_request
def before_request():
    api_key = request.headers.get("X-API-KEY")

    if request.endpoint == 'get_image':
        return
    
    if not verify_api_key(api_key):
        return jsonify({"error": "unauthorized"}), 403




#REQUEST PRESIGN KEY
@app.route("/api/v1/presign/request", methods=["POST"])
def presign():
    try:
        request_data = request.get_json()
        file_extension = request_data["file_name"].strip().lower().split('.')[-1]

        print('Presign >>> '+file_extension)

        if file_extension not in ALLOWED_EXTENSIONS:
            return fail_response("Don't allowed file extensions", 400)

        connection = establish_connection()

        try:
            cursor = connection.cursor()

            presign_key = str(uuid.uuid4())
            filename = ramdomFilename(datetime.now(), file_extension)
            file_path = request_data["file_path"]
            file_type = checkFileType(file_extension)

            # Insert presign
            response = insert_presign(cursor, connection, presign_key, filename, file_path, file_type)

            connection.commit()
            return success_response("Presign key generate successful",response)
        finally:
            close_connection(cursor, connection)

    except Exception as e:
        close_connection(cursor, connection)
        return jsonify({"error": str(e)}), 500






#UPLOAD FILE
@app.route("/api/v1/file/upload/base64", methods=["POST"])
def upload_base64():
    connection = establish_connection()

    try:
        request_data = request.get_json()
        file_data = base64.b64decode(request_data["base64_data"])
        presign_key = request_data["presign_key"]

        cursor = connection.cursor()

        # Check presign key
        if not is_valid_presign_key(cursor, presign_key):
            return fail_response("Invalid presign key", 400)

        # Get file name using presign key
        file_info = getPresignInfo(cursor, presign_key)
        if not file_info:
            return fail_response("Invalid presign info", 400)

        file_name = file_info['file_name']
        file_path = file_info['file_path']
        file_type = file_info['file_type']

        if file_type == 'image':
            response_data = uploadImage(file_data, file_path, file_name)
        elif file_type == 'Video':
            response_data = {}
        elif file_type == 'Audio':
            response_data = {}
        else:
            return fail_response("Something went wrong")

        return success_response("Upload successful", response_data)

    except Exception as e:
        return jsonify({"error": f"Error {str(e)}"}), 400
    finally:
        close_connection(cursor, connection)






# Endpoint for binary file upload
@app.route("/api/v1/file/upload", methods=["POST"])
def upload_binary():
    connection = establish_connection()
    cursor = connection.cursor()
    try:
        presign_key = request.form.get("presign_key")
        file = request.files['file']

        file_extension = os.path.splitext(file.filename)[1]

        #check if file exists
        if not file:
            return fail_response("No file provided for upload", 400)
        
        #validate presign key
        if not is_valid_presign_key(cursor, presign_key):
            return fail_response("Invalid presign key", 400)

        #get presign info
        file_info = getPresignInfo(cursor, presign_key)
        if not file_info:
            return fail_response("Invalid presign info", 400)

        #check file extension
        file_name = file_info['file_name']
        if(file_extension != os.path.splitext(file_name)[1]):
            return fail_response("Unsupported file type",400)
        
        file_path = file_info['file_path']
        file_type = file_info['file_type']

        #TODO Upload File
        response=uploadFile(file,file_path,file_name,file_type)

        return success_response("Upload successful", response)

    except Exception as e:
        return jsonify({"error": f"Error {str(e)}"}), 400
    finally:
        close_connection(cursor, connection)







# GET FILE
@app.route("/coderverse/<path:path>/<file_name>", methods=["GET"])
def get_image(path, file_name):
    try:
        ql = request.args.get('ql')
        if ql is not None:
            quality_dir = ql
        else:
            quality_dir = "source"

        image_path = os.path.join(STORAGE_PATH, path, quality_dir ,file_name)
        print(image_path)

        if not os.path.exists(image_path):
            return fail_response("File not found", 404)

        return send_from_directory(STORAGE_PATH, path +'/'+quality_dir+'/'+file_name)
    except Exception as e:
        return fail_response("Not found",404)






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
