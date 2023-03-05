from fastapi import FastAPI, Path, Query, HTTPException, status, Depends, Request, Header
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
import requests
import os
from dotenv import load_dotenv

#---LOCAL IMPORTS---#
from db import create_user_key, generate_api_access_key
from models import UserKeyStore, KeyStore

#---LOAD ENV VARS---#
load_dotenv()

#---APP INIT---#
app = FastAPI()

#---APP SECURITY INIT---#
API_KEY = os.getenv("SYM_KEY_API_KEY")


async def api_key_checker( api_key: str = Header(None)):
    API_KEY = os.getenv("SYM_KEY_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No API key provided!",
        )
    elif api_key != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )


#---API KEY GEN ROUTE---#

#route the will allow a one-time api key create request and set it in the .env. Afterwards it will refuse to create any new keys
@app.get("/init_api")
async def init_api_key():
    if os.getenv("SYM_KEY_API_KEY") is None:
        new_api_key = generate_api_access_key()
        os.environ["SYM_KEY_API_KEY"] = new_api_key
        with open(".env", "a") as env_file:
            env_file.write(f"SYM_KEY_API_KEY = {new_api_key}\n")
        load_dotenv()
        return {"api-key" : f"{new_api_key}"}
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API key already exists!",
        )

#---PROTECTED APP ROUTES---#        
@app.get("/")
async def root_route(api_key: str = Depends(api_key_checker)):
    return {"message" : "Root API call successful!"}

@app.post("/api/v1/user_key")
async def create_user_key_store(user_key_set : UserKeyStore, api_key: str = Depends(api_key_checker)):
    
    username = user_key_set.username
    symmetric_key = user_key_set.key_store.symmetric_key
    user_password_hash = user_key_set.key_store.user_password_hash
    
    return {"message" : f"UserKeyStore object received successfully! {username} {symmetric_key} {user_password}"}

@app.get("/api/v1/user_key")
async def get_user_key_store(api_key: str = Depends(api_key_checker)):
    """Function will take a username, password and friend username. After verification it will return an encrypted
    symmetric key."""
    pass
    
    return {"message" : "Encrypted symmetric key will be returned here"}