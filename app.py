import time

class App:
    """ 
    Maneja el bucle infinito de procesamiento.
    Recibe sus dependencias (cámara, detector, visualizador) ya listas.
    """
    def __init__(self, camera, detector, visualizer):
        self.camera = camera
        self.detector = detector
        self.visualizer = visualizer

    def run(self):
        try:
            print("Iniciando la cámara...")
            self.camera.start()
            
            time.sleep(1)
            print("Presiona 'q' en la ventana para salir.")

            while True:
                # Obtener frame (GStreamer o Mock)
                frame = self.camera.get_frame(timeout=0.5)

                if frame is not None:
                    # Inferencia y Postprocesamiento (Hailo o Mock)
                    boxes, scores, class_ids, indices = self.detector.detect(frame)

                    # Dibujar resultados (OpenCV en BGR)
                    import cv2
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    frame_drawn = self.visualizer.draw_detections(
                        frame_bgr, boxes, scores, class_ids, indices
                    )

                    # Mostrar y verificar si se presionó la tecla de salida
                    if not self.visualizer.show(frame_drawn):
                        break

        except KeyboardInterrupt:
            # Captura un Ctrl+C en la consola para no crashear
            print("\nDeteniendo el programa ...")
            
        except Exception as e:
            # Captura cualquier otro error para que no se quede colgado
            print(f"\nOcurrió un error inesperado: {e}")

        finally:
            # Garantiza que el hardware se libere siempre, incluso si hay un error
            print("Limpiando recursos...")
            self.camera.stop()
            self.visualizer.cleanup()