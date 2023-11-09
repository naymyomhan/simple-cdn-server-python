from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

def success_response(message,data):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return JSONResponse(content=response, status_code=200)

def fail_response(message,code=500):
    response = {
        "success": False,
        "message": message,
    }
    return JSONResponse(content=response, status_code=code)

