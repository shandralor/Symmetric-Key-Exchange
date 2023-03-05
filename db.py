from deta import Deta
from dotenv import load_dotenv
import os
from typing import Union
import logging
import secrets
import string

#---LOCAL IMPORTS---#
from models import UserKeyStore, KeyStore

#---LOAD ENV VARS---#
load_dotenv()

#---DB INIT---#
DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)
#---#
KEYS = deta.Base("keys_db")

def create_user_key(username:str, symmetric_key:str, password_hash:str)->None:
    """Function to create a new user. It takes three strings and inputs these into the new_user dictionary. The function then
    attempts to put this dictionary in the database"""

    new_user_key_object = {
        "key": username,
        "key_store": {
                "symmetric_key" : symmetric_key,
                "hashed_pw" : password_hash
                }
            }
    try:
        return KEYS.put(new_user_key_object)
    except Exception as error_message:
        logging.exception(error_message)
        return None
    
def generate_api_access_key():
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for i in range(32))
    return api_key
