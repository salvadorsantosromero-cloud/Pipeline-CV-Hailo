import cv2
import numpy as np
import queue
import time
from settings import MODE, MOCK_VIDEO_PATH

# Solo importar GStreamer si esta en la Pi 5
if MODE == "hailo":
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

class MockVideoCamera:
    """ Cámara simulada para probar en la PC usando un video MP4 """
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(str(video_path))
        if not self.cap.isOpened():
            raise FileNotFoundError(f"No se pudo abrir el video: {video_path}")
        
        # Simular una cola para mantener la misma interfaz que GStreamer
        self.frame_queue = queue.Queue(maxsize=2)

    def start(self):
        pass

    def get_frame(self, timeout=0.5):
        ret, frame = self.cap.read()
        if not ret:
            # Si el video termina, se reinicia para pruebas continuas
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            
        # OpenCV lee en BGR, pero el pipeline espera RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        time.sleep(0.03) # Simulamos latencia de 30fps
        return frame_rgb

    def stop(self):
        self.cap.release()


class GStreamerCamera:
    """ Tu manejador original de cámara de la Pi 5 """
    def __init__(self):
        Gst.init(None)
        self.frame_queue = queue.Queue(maxsize=2)
        
        pipeline_str = (
            "libcamerasrc ! video/x-raw, format=YUY2, width=640, height=480 ! "
            "videoconvert ! video/x-raw, format=RGB ! "
            "appsink name=mysink emit-signals=true max-buffers=1 drop=true sync=false"
        )
        self.pipeline = Gst.parse_launch(pipeline_str)
        self.sink = self.pipeline.get_by_name("mysink")
        self.sink.connect("new-sample", self.on_new_sample)

    def on_new_sample(self, sink):
        sample = sink.emit("pull-sample")
        buffer = sample.get_buffer()
        caps = sample.get_caps()
        
        h = caps.get_structure(0).get_value('height')
        w = caps.get_structure(0).get_value('width')
        
        success, map_info = buffer.map(Gst.MapFlags.READ)
        if success:
            img = np.ndarray((h, w, 3), buffer=map_info.data, dtype=np.uint8).copy()
            buffer.unmap(map_info)
            if not self.frame_queue.full():
                self.frame_queue.put(img)
        return Gst.FlowReturn.OK

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def get_frame(self, timeout=0.5):
        return self.frame_queue.get(timeout=timeout)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)


# --- Dependency Injection Setup ---
def get_camera():
    """ Devuelve la cámara física o el video dependiendo del entorno """
    if MODE == "hailo":
        print("Iniciando cámara real (GStreamer)...")
        return GStreamerCamera()
    else:
        print(f"Iniciando cámara Mock con video: {MOCK_VIDEO_PATH}")
        return MockVideoCamera(MOCK_VIDEO_PATH)