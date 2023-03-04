from deta import Deta
from dotenv import load_dotenv
import os
from typing import Union
import logging

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
        username: 
            {
                "symmetric_key" : symmetric_key,
                "hashed_pw" : password_hash
                }
            }
    try:
        return KEYS.put(new_user_key_object)
    except Exception as error_message:
        logging.exception(error_message)
        return None