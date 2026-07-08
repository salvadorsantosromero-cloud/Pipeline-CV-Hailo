import numpy as np
from settings import MODE

# Determinar qué librería cargar basado en el MODO (Pi 5 vs PC)
if MODE == "hailo":
    try:
        from hailo_platform import (
            VDevice, HEF, InferVStreams, ConfigureParams, 
            InputVStreamParams, OutputVStreamParams, 
            FormatType, HailoStreamInterface
        )
    except ImportError:
        print("ERROR: Librería hailo_platform no encontrada. Activando MOCK.")
        from hailo_hardware.mock_hailo import *
else:
    from hailo_hardware.mock_hailo import *


class HailoRunner:
    def __init__(self, hef_path):
        self.hef_path = str(hef_path)
        self.target = VDevice()
        self.hef = HEF(self.hef_path)
        
        self._configure_device()

    def _configure_device(self):
        """ Configura los parámetros de red y streams """
        try:
            configure_params = ConfigureParams.create_from_hef(
                self.hef, interface=HailoStreamInterface.PCIe
            )
        except AttributeError:
            configure_params = ConfigureParams.create_from_hef(self.hef)
            
        network_groups = self.target.configure(self.hef, configure_params)
        self.network_group = network_groups[0]
        self.network_group_params = self.network_group.create_params()

        self.input_vstreams_params = InputVStreamParams.make(
            self.network_group, format_type=FormatType.UINT8
        )
        self.output_vstreams_params = OutputVStreamParams.make(
            self.network_group, format_type=FormatType.FLOAT32
        )

        self.input_name = self.hef.get_input_vstream_infos()[0].name

    def infer(self, input_tensor: np.ndarray) -> dict:
        """ 
        Activa la red, envía la imagen y retorna los tensores crudos.
        """
        # La activación ocurre por inferencia para garantizar memoria limpia
        with self.network_group.activate(self.network_group_params):
            with InferVStreams(self.network_group, self.input_vstreams_params, self.output_vstreams_params) as infer_pipeline:
                
                input_data = {self.input_name: input_tensor}
                results = infer_pipeline.infer(input_data)
                
                return results