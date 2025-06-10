# 🎵 Control de sonido con gestos usando OpenCV y MediaPipe

Este proyecto en Python utiliza **OpenCV**, **MediaPipe** y **sounddevice** para controlar el tono (frecuencia) de un sonido mediante gestos con la mano. Al mover el pulgar y el índice delante de la cámara, se genera un sonido cuya frecuencia varía según la distancia entre los dedos.

## 🧠 Tecnologías utilizadas

- `OpenCV`: Captura y procesamiento de imagen en tiempo real.
- `MediaPipe`: Detección y seguimiento de manos.
- `sounddevice`: Generación de audio en tiempo real.
- `NumPy`, `math`, `threading`: Utilidades para cálculos y manejo de audio.

## ⚙️ Funcionamiento

- El sistema detecta una mano en la imagen.
- Se calcula la distancia entre el pulgar (landmark 4) y el índice (landmark 8).
- Esa distancia se mapea a una frecuencia de sonido (entre 200 Hz y 1000 Hz).
- Se genera un tono en tiempo real, cuyo tono varía con el movimiento de los dedos.

## 🛠 Requisitos

Instala las dependencias necesarias con:

```bash
pip install opencv-python mediapipe numpy sounddevice
```
README ECHO CON CHATGPT (me siento moralmente obligado a poner esto)
