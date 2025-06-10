# Importamos las librerías necesarias:
import cv2  # OpenCV para procesamiento de imágenes y manejo de la cámara
import mediapipe as mp  # MediaPipe para detectar las manos
import time 
import math
import numpy as np
import sounddevice as sd
import threading

frame_rate = 2
frame_actual = frame_rate - 1

fs = 44100
volumen = 0.05
frecuencia_actual = 440
frecuencia_lock = threading.Lock()

sonido_activo = False

def audio_callback(outdata, frames, time_info, status):
    t = (np.arange(frames) + audio_callback.pos) / fs
    with frecuencia_lock:
        f = frecuencia_actual
    outdata[:] = (volumen * np.sin(2 * np.pi * f * t)).reshape(-1,1)
    audio_callback.pos += frames
audio_callback.pos = 0

# Crear y arrancar el stream de audio (hazlo UNA vez, antes del loop principal)
stream = sd.OutputStream(channels=1, callback=audio_callback, samplerate=fs)
stream.start()

# Activamos la cámara (por defecto la número 0)
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Inicializamos el módulo de detección de manos de MediaPipe
mpHands = mp.solutions.hands  # Acceso al módulo 'hands'
# Creamos el objeto 'hands' para detectar las manos
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.3
)
# Utilidad para dibujar los puntos y las conexiones de las manos
mpDraw = mp.solutions.drawing_utils

# Parámetros de entrada (0 a 200)
input_frecuencia = 100  # ej. 0 a 200
input_volumen = 150     # ej. 0 a 200

# Mapear volumen (0 a 1)
volumen = np.interp(input_volumen, [0, 200], [0, 1])

# Bucle principal del programa
while True:

    # Leemos un frame de la cámara
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Convertimos la imagen de BGR (formato de OpenCV) a RGB (formato que usa MediaPipe)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Procesamos la imagen para detectar las manos
    results = hands.process(imgRGB)
    # Imprimimos por consola los resultados (coordenadas de los puntos de las manos)

    # Si se detectaron manos...
    if results.multi_hand_landmarks:
        frame_actual += 1
        # Recorremos cada mano detectada
        for handLms in results.multi_hand_landmarks:
            # Dibujamos los puntos (landmarks) y las líneas que los conectan sobre la imagen original
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS,mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),mpDraw.DrawingSpec(color=(0, 255, 0), thickness=3))

            x_pulgar, y_pulgar = 0,0
            x_indice, y_indice = 0,0

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape  # Obtener tamaño de la imagen
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convertir coords normalizadas a pixeles

                if id == 4:
                    x_pulgar, y_pulgar = cx, cy
                elif id == 8:
                    x_indice, y_indice = cx, cy

            distancia = math.hypot(x_indice - x_pulgar, y_indice - y_pulgar)
            distancia = round(distancia, 0)
            

            if  ((handLms in results.multi_hand_landmarks) != None) and frame_actual == frame_rate:
                frame_actual = 0
                
                if sonido_activo == False:
                    stream.start()
                
                nueva_freq = np.interp(distancia, [30, 200], [200, 1000])

                with frecuencia_lock:
                    frecuencia_actual = nueva_freq

            # Dibujar una línea entre los dedos y mostrar la distancia en pantalla
            cv2.line(img, (x_pulgar, y_pulgar), (x_indice, y_indice), (255, 0, 0), 2)
            cv2.line(img, (0, 0), (50,50), (0, 255, 0), 2)
    else:
        stream.stop()
        sonido_activo = False
    # Mostramos la imagen en una ventana llamada "Image"
    cv2.imshow("Image", img)

    # Esperamos 1 milisegundo y seguimos con el siguiente frame
    if cv2.waitKey(5) & 0xFF == 27:  # ESC para salir
        break

stream.stop()
stream.close()