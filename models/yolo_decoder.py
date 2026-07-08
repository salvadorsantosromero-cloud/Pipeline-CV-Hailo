import numpy as np
import cv2
from settings import INPUT_SIZE, CONF_THRESHOLD

class YoloDecoder:
    """ Decodifica los tensores del modelo YOLOv8 """
    def __init__(self):
        self.anchors, self.strides = self._make_anchors(INPUT_SIZE)
    
    def _make_anchors(self, imgsz):
        anchors, strides = [], []
        for stride in [8, 16, 32]:
            h, w = imgsz // stride, imgsz // stride
            xv, yv = np.meshgrid(np.arange(w), np.arange(h))
            grid = np.stack((xv, yv), 2).reshape(-1, 2)
            anchors.append(grid)
            strides.append(np.full((grid.shape[0], 1), stride))
        return np.concatenate(anchors), np.concatenate(strides)

    def decode(self, box_tensor, score_tensor):
        """ Extraer matemáticas crudas de los tensores """
        box_tensor = box_tensor.reshape(1, -1, 64)
        score_tensor = score_tensor.reshape(1, -1, 10) 

        max_scores = np.max(score_tensor[0], axis=-1)
        class_ids = np.argmax(score_tensor[0], axis=-1)

        mask = max_scores > CONF_THRESHOLD
        
        if not np.any(mask): 
            return [], [], []
        
        scores = max_scores[mask]
        ids = class_ids[mask]
        boxes_dfl = box_tensor[0, mask, :]
        anchors = self.anchors[mask]
        strides = self.strides[mask]

        boxes_dfl = boxes_dfl.reshape(-1, 4, 16)
        e_x = np.exp(boxes_dfl - np.max(boxes_dfl, axis=2, keepdims=True))
        weights = e_x / np.sum(e_x, axis=2, keepdims=True)
        pos_vec = np.arange(16, dtype=np.float32)
        dist = np.sum(weights * pos_vec, axis=2)

        lt, rb = dist[:, :2], dist[:, 2:]
        x1y1 = anchors - lt
        x2y2 = anchors + rb
        bboxes = np.concatenate((x1y1, x2y2), axis=1) * strides
        
        return bboxes, scores, ids

    def apply_nms(self, boxes, scores):
        """ Filtrar cajas superpuestas (Supresión de No Máximos) """
        if len(boxes) == 0:
            return []

        # OpenCV requiere el formato [x, y, ancho, alto] para NMSBoxes
        boxes_wh = boxes.copy()
        boxes_wh[:, 2] = boxes[:, 2] - boxes[:, 0]
        boxes_wh[:, 3] = boxes[:, 3] - boxes[:, 1]
        
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes_wh.tolist(), 
            scores=scores.tolist(),
            score_threshold=CONF_THRESHOLD, 
            nms_threshold=0.50
        )
        
        if len(indices) > 0:
            return indices.flatten()
        return []