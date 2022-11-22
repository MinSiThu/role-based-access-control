from datetime import datetime, timedelta
from typing import Union

from fastapi import FastAPI,Depends,Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel

from consts import *
from rbac_config import *
from jwt_master import create_access_token,decode_access_token

app = FastAPI()
auth_scheme = HTTPBearer()

class Document(BaseModel):
    title:str
    content:str

class User(BaseModel):
    username:str
    usertype:ROLES

documents = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/token')
def create_token_for_user(user: User):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data = create_access_token(data=user.dict(),expires_delta=access_token_expires)
    return {"encoded_data":encoded_data}

@app.post('/document')
def create_document(document:Document,authorization: HTTPAuthorizationCredentials= Depends(auth_scheme)):
    try:
        print(authorization.credentials)
        user_dict = decode_access_token(authorization.credentials)
        if FastApiRBACMaster().RBAC([ROLES.MODERATOR,ROLES.ADMIN],user_dict["usertype"]) == True:
            documents.append(document)
            return document
    except:
        return JSONResponse(
            status_code=401,
            content={"message": "UnAuthorized Access"},
        )

@app.get('/documents',)
def all_documents():
    return documents

@app.put("/documents/{id}")
def read_item(id: int,document:Document, q: Union[str, None] = None,authorization:HTTPAuthorizationCredentials= Depends(auth_scheme)):
    try:
        user_dict = decode_access_token(authorization.credentials)
        if FastApiRBACMaster().RBAC([ROLES.ADMIN],user_dict["usertype"]) == True:
            if id< len(documents):
                documents[id] = document
                return documents[id]
            return {}
    except:
        return JSONResponse(
            status_code=401,
            content={"message": "UnAuthorized Access"},
        )