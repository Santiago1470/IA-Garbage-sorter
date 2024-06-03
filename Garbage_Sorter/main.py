import cv2
import numpy as np
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
# import speech_recognition as sr
from fastapi.middleware.cors import CORSMiddleware
# import pyttsx3 as sk
from pydantic import BaseModel
from video_modelo import generate_frames
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Texto(BaseModel):
    texto: str

# @app.get("/video")
# async def video_feed():
#     cap = cv2.VideoCapture(0)

#     def generate():
#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break

#             ret, buffer = cv2.imencode('.jpg', frame)

#             if not ret:
#                 continue

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

#     return StreamingResponse(
#         generate(),
#         media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/")
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/templates/{path}", name="templates")
async def serve_template(path: str, request: Request):
    return templates.TemplateResponse(path, {"request": request})


@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


# @app.get("/")
# async def getArduinoRight():
#     # URL de la API a la que deseas hacer la solicitud GET
#     api_url = "https://127.0.0.1:3001/"
    
#     try:
#         # Hacer la solicitud GET a la API
#         response = requests.get(api_url)
#         # Verificar si la solicitud fue exitosa (código de estado 200)
#         if response.status_code == 200:
#             # Devolver los datos obtenidos de la API
#             return response.json()
#         else:
#             # Devolver un mensaje de error si la solicitud no fue exitosa
#             return {"error": "No se pudo obtener datos de la API"}
#     except Exception as e:
#         # Manejar cualquier excepción que pueda ocurrir durante la solicitud
#         return {"error": str(e)}

# @app.get("/")
# async def getArduinoLeft():
#     # URL de la API a la que deseas hacer la solicitud GET
#     api_url = "https://127.0.0.1:3001/left"
    
#     try:
#         # Hacer la solicitud GET a la API
#         response = requests.get(api_url)
#         # Verificar si la solicitud fue exitosa (código de estado 200)
#         if response.status_code == 200:
#             # Devolver los datos obtenidos de la API
#             return response.json()
#         else:
#             # Devolver un mensaje de error si la solicitud no fue exitosa
#             return {"error": "No se pudo obtener datos de la API"}
#     except Exception as e:
#         # Manejar cualquier excepción que pueda ocurrir durante la solicitud
#         return {"error": str(e)}

# @app.get("/habla")
# async def obtener_habla():
#     r = sr.Recognizer() 
#     with sr.Microphone() as recurso:
#         audio = r.listen(recurso)
#         try:
#             texto = r.recognize_google(audio, language='es-ES')
#             print(texto)
#             return texto
#         except:
#             return 'No se escucho, repite de nuevo'
        

# @app.post("/responde")
# async def hablando(texto_obj: Texto):
#     texto = texto_obj.texto
#     engine = sk.init()
#     engine.say(texto)
#     engine.runAndWait()