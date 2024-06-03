import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from constants import labels
import asyncio


# Cargar el modelo guardado
with tf.keras.utils.custom_object_scope({'KerasLayer': hub.KerasLayer}):
    model = tf.keras.models.load_model('model/modelo_entrenado.h5')

# Inicializar la webcam
cap = cv2.VideoCapture(0)

async def generate_frames():
    contador = 0
    # valor = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        img = np.array(img).astype(float) / 255
        img = cv2.resize(img, (224, 224))

        prediccion = model.predict(img.reshape(-1, 224, 224, 3))
        print(prediccion[0])
        if np.max(prediccion[0]) < 0.991:
            
            # print(await asyncio.to_thread(getArduinoClose))
            # if valor != 1:
            #     print("Esta cerrando y haciendo la peticion")
            #     cerrar = await asyncio.to_thread(getArduinoClose)
            # # Obtenemos el valor que necesitas
            # message = cerrar["message"]
            # valor = message.split(", ")[1]
            categoria = 3
            contador = 0
        else:
            categoria = np.argmax(prediccion[0], axis=-1)
            contador = contador + 1
            if contador > 20:
                if categoria == 0:
                    await asyncio.to_thread(getArduinoOpen)
                elif categoria == 1:
                    await asyncio.to_thread(getArduinoOpen)
                elif categoria == 2:
                    await asyncio.to_thread(getArduinoOpen)
                # message = abierto["message"]
                # valor = message.split(", ")[1]
                # print(message)

        categorizacion = labels[categoria]
        label = f'Categoria: {categorizacion}'
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # print(contador)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def getArduinoOpen():
    url = "http://localhost:3001/open"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "No se pudo obtener los datos de la API."}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

# def getArduinoClose():
#     url = "http://localhost:3001/close"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": "No se pudo obtener los datos de la API."}
#     except Exception as e:
#         return {"error": f"Ocurrió un error: {str(e)}"}