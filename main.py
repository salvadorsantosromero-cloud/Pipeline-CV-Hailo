import os
from settings import MODE, HEF_PATH

from sensors.camera import get_camera
from visualizer.visualizer import Visualizer
from models.detector import Detector
from hailo_hardware.hailo_runner import HailoRunner
from app import App

def main():
    print(f"--- INICIANDO PROYECTO HAILO (MODO: {MODE.upper()}) ---")
    
    # Verificación rápida de entorno
    if MODE == "mock" and not os.path.exists("resources"):
        print("ADVERTENCIA: Estás en modo MOCK pero falta la carpeta 'resources' con tu video de prueba.")
    
    if MODE == "hailo" and not os.path.exists(HEF_PATH):
        print(f"ERROR: Falta el archivo HEF en la ruta: {HEF_PATH}")
        return

    # Crear las Dependencias (Instanciar los objetos)
    # Hardware/Modelo
    hailo_runner = HailoRunner(HEF_PATH)
    detector = Detector(hailo_runner)
    # Sensores y Salida
    camera = get_camera()
    visualizer = Visualizer(window_name="Deteccion Hojas enfermas de Tomate")

    # Inyectar las dependencias en la Aplicación
    app = App(
        camera=camera,
        detector=detector,
        visualizer=visualizer
    )

    app.run()

if __name__ == "__main__":
    main()