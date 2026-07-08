import cv2
import numpy as np
from settings import INPUT_SIZE
from models.yolo_decoder import YoloDecoder

class Detector:
    """ 
    Clase que coordina el pre-procesamiento, 
    la inferencia en hardware y la decodificación matemática.
    """
    def __init__(self, hailo_runner):
        # Le pasamos el motor de hardware ya configurado
        self.hailo_runner = hailo_runner
        self.decoder = YoloDecoder()

    def preprocess(self, frame_rgb):
        """ Ajusta la imagen al formato requerido por la red neuronal """
        img_resized = cv2.resize(frame_rgb, (INPUT_SIZE, INPUT_SIZE))
        img_batch = np.expand_dims(img_resized, axis=0)
        return img_batch

    def detect(self, frame_rgb):
        """ 
        Ejecuta todo el flujo: Preprocesar -> Inferir -> Decodificar -> NMS 
        Retorna los datos listos para ser dibujados.
        """
        # Preprocesar
        input_tensor = self.preprocess(frame_rgb)

        # Inferencia en el hardware
        raw_results = self.hailo_runner.infer(input_tensor)

        box_tensor = None
        score_tensor = None
        
        # Encontrar qué tensor es cuál
        for name, tensor in raw_results.items():
            if tensor.shape[-1] == 64:
                box_tensor = tensor
            elif tensor.shape[-1] == 10:
                score_tensor = tensor

        # Decodificación y NMS
        if box_tensor is not None and score_tensor is not None:
            boxes, scores, class_ids = self.decoder.decode(box_tensor, score_tensor)
            indices = self.decoder.apply_nms(boxes, scores)
            return boxes, scores, class_ids, indices
        
        # Si no hay detecciones o falló algo
        return [], [], [], []