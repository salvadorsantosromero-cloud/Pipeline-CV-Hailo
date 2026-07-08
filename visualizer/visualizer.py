import cv2
from settings import CLASES, COLORES, INPUT_SIZE

class Visualizer:
    def __init__(self, window_name="Deteccion de Enfermedades en Hojas"):
        self.window_name = window_name

    def draw_detections(self, frame_bgr, boxes, scores, class_ids, indices):
        # Si no hay nada detectado, devolver la imagen original
        if len(indices) == 0:
            return frame_bgr

        # Calcular la escala -> la inferencia se hizo en 416x416, 
        # pero la cámara puede ser de 640x480 o 1920x1080
        h_orig, w_orig = frame_bgr.shape[:2]
        scale_x = w_orig / INPUT_SIZE
        scale_y = h_orig / INPUT_SIZE

        for i in indices:
            # OpenCV NMS puede devolver los índices anidados, asegurarse que sea entero
            idx = int(i) 
            
            box = boxes[idx]
            score = scores[idx]
            cid = class_ids[idx]

            # Escalar coordenadas a la resolución original de la pantalla
            x1 = int(box[0] * scale_x)
            y1 = int(box[1] * scale_y)
            x2 = int(box[2] * scale_x)
            y2 = int(box[3] * scale_y)

            color_caja = COLORES[cid]
            nombre_clase = CLASES[cid]
            
            # Dibujar Bounding Box
            cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color_caja, 2)
            
            # Preparar el texto
            label = f"{nombre_clase}: {int(score * 100)}%"
            
            # Calcular el tamaño del fondo negro para que el texto sea legible
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame_bgr, (x1, y1 - text_height - 10), (x1 + text_width, y1), color_caja, -1)
            
            # Dibujar el texto en blanco sobre el fondo de color
            cv2.putText(frame_bgr, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame_bgr

    def show(self, frame_bgr):
        cv2.imshow(self.window_name, frame_bgr)
        
        # Espera 1 milisegundo por un evento de teclado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False 
        return True

    def cleanup(self):
        cv2.destroyAllWindows()