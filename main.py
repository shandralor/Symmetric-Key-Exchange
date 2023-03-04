from fastapi import FastAPI
import requests

#---APP INIT---#
app = FastAPI()


@app.get("/")
async def root_route():
    return {"API" : "Succesful api call"}
