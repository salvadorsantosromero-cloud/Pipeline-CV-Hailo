import os
from pathlib import Path

# --- MODO DE EJECUCIÓN ---
MODE = os.getenv("APP_MODE", "mock") # mock | hailo

# --- RUTAS DE DIRECTORIOS ---
BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"

HEF_PATH = RESOURCES_DIR / "yolov8n_leaf_416_v2.hef"
MOCK_VIDEO_PATH = RESOURCES_DIR / "video_prueba_mold2_1536x864.mp4" # Video de prueba

# --- PARÁMETROS DEL MODELO ---
INPUT_SIZE = 416  
CONF_THRESHOLD = 0.60

# --- CLASES Y COLORES ---
CLASES = [
    "Bacterial spot", "Early blight", "Healthy", "Late blight", 
    "Leaf Mold", "Septoria leaf spot", "Spider mites", 
    "Target Spot", "Tomato mosaic virus", "Yellow Leaf Curl Virus"
]

COLORES = [
    (0, 0, 255),   # Rojo
    (0, 165, 255), # Naranja
    (0, 255, 0),   # Verde (Ideal para Healthy)
    (255, 0, 0),   # Azul
    (255, 255, 0), # Cian
    (255, 0, 255), # Magenta
    (128, 0, 128), # Morado
    (0, 255, 255), # Amarillo
    (128, 128, 0), # Verde Oliva
    (0, 128, 255)  # Ámbar
]