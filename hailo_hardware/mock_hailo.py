import numpy as np

# --- MOCKS DE LAS CLASES DE HAILO ---
class HEF:
    def __init__(self, path):
        self.path = path
    def get_input_vstream_infos(self):
        class Info: name = "mock_input"
        return [Info()]

class VDevice:
    def configure(self, hef, params):
        class NetworkGroup:
            def create_params(self): return None
            def activate(self, params):
                class ContextManager:
                    def __enter__(self): pass
                    def __exit__(self, *args): pass
                return ContextManager()
        return [NetworkGroup()]

class ConfigureParams:
    @staticmethod
    def create_from_hef(hef, interface=None): return None

class InputVStreamParams:
    @staticmethod
    def make(group, format_type): return None

class OutputVStreamParams:
    @staticmethod
    def make(group, format_type): return None

class InferVStreams:
    def __init__(self, group, in_params, out_params):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def infer(self, input_data):
        # Simulamos los tensores que YoloDecoder espera recibir (64 y 10)
        return {
            "mock_output_boxes": np.zeros((1, 100, 64), dtype=np.float32),
            "mock_output_scores": np.zeros((1, 100, 10), dtype=np.float32)
        }

class FormatType:
    UINT8 = 1
    FLOAT32 = 2

class HailoStreamInterface:
    PCIe = 1