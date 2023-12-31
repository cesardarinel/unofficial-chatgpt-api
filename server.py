"""Make some requests to OpenAI's chatbot"""
import threading
import os

import flask
from chatgptapi import chatgtp
from dotenv import load_dotenv

APP = flask.Flask(__name__)
CHAT=None
load_dotenv()
#semaphore = threading.Semaphore(1)
# Accede a las variables de entorno cargadas
database_url = os.getenv("DATABASE_URL")
ruta = os.getenv("RUTA")
visible = False #if os.getenv("INVISIBLE", "False").lower() == "true" else False 

@APP.route("/chat", methods=["GET"]) 
def chat():
 #   semaphore.acquire()
    #try:
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    response=CHAT.send_message(message)
    print("Response: ", response)
    return response
    #finally:
       # semaphore.release()

@APP.route("/reset", methods=["GET"])
def reset():
    print("Resetting chat")
    CHAT.get_reset_button()
    return "Chat thread reset"

@APP.route("/close", methods=["GET"])
def close():
    CHAT.close()
    return "Lista cerrados"

@APP.route("/restart", methods=["GET"])
def restart():
    CHAT.int_sync_playwright()
    return "API restart!"

def start_browser():
    global CHAT
    CHAT=chatgtp(ruta,visible)
    APP.run(port=5001, threaded=False)
    print("Logged in")

if __name__ == "__main__":
    start_browser()