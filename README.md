# Detección de Enfermedades en Hojas con Hailo 8L (Edge AI)

Este repositorio contiene un pipeline de visión artificial optimizado para ejecutarse en tiempo real en una **Raspberry Pi 5** equipada con el acelerador de inteligencia artificial **Hailo 8L**. 

El proyecto implementa una **Arquitectura de Software** basada en Programación Orientada a Objetos (POO) e Inyección de Dependencias. 

---

## Arquitectura del Proyecto

Principio de Responsabilidad Única (SRP):

* **`sensors/`**: Abstrae la entrada de video. Instancia una cámara GStreamer de latencia ultrabaja en hardware real, o un lector de video `.mp4` para entornos de simulación.
* **`models/`**: Contiene la lógica matemática. Aquí vive el decodificador personalizado para los tensores DFL de YOLOv8 y el algoritmo de Supresión de No Máximos (NMS).
* **`hailo_hardware/`**: Maneja la conexión PCIe con el chip Hailo 8L. Incluye un módulo `Mock` automatizado que simula el hardware cuando se ejecuta en una PC de desarrollo.
* **`visualizer/`**: Encapsula exclusivamente la representación gráfica y funciones de OpenCV (`cv2.rectangle`, `cv2.putText`) para mantener el bucle principal desacoplado.

---

## Requisitos y Entornos

Debido a que los aceleradores de hardware requieren interacción directa con el Kernel de Linux y puertos PCIe, el proyecto maneja **dos entornos distintos**:

### 1. Entorno de Desarrollo (PC / Laptop)
Diseñado para trabajar en la lógica del código o interfaz gráfica sin necesidad de la Raspberry Pi física.
* Python 3.9+
* `numpy>=1.20.0`
* `opencv-python>=4.5.0`

### 2. Entorno de Producción (Raspberry Pi 5 + Hailo 8L)
**IMPORTANTE:** No es recomendable crear un entorno virtual desde cero mediante `pip`. La librería `hailo_platform` y los bindings de `GStreamer` requieren compilación nativa ligada al firmware de la placa. Se puede  ejecutar este proyecto utilizando el entorno virtual oficial proveído por el SDK de Hailo: `venv_hailo_rpi5_examples`.

---

## Instalación y Uso

Clona este repositorio en tu espacio de trabajo:
```bash
git clone https://github.com/salvadorsantosromero-cloud/Pipeline-CV-Hailo.git
cd Pipeline-CV-Hailo
```
El flujo de ejecución está controlado globalmente por la variable de entorno APP_MODE.

### Modo 1: Simulación en PC (Mock Mode)
Este modo utiliza hardware simulado y procesa un video pregrabado. Es ideal para depurar interfaces, verificar transformaciones de color o ajustar umbrales.

1. Crea una carpeta llamada `resources` en la raíz del proyecto.

2. Coloca un video corto de prueba en formato `.mp4` dentro de `resources/` y nómbralo `hojas_test.mp4`.

3. Ejecuta el programa desde la terminal:

**En Windows (PowerShell):**

```PowerShell
$env:APP_MODE="mock"
python main.py
```
**En Linux / macOS:**

```Bash
export APP_MODE=mock
python main.py
```

### Modo 2: Despliegue en Hardware Real (Raspberry Pi 5)
Este modo despierta los controladores físicos de la cámara mediante GStreamer y enlaza el flujo de datos por PCIe directamente al chip Hailo 8L.

1. Conecta la cámara física de la Raspberry Pi y asegúrate de que el módulo Hailo 8L esté correctamente montado en el HAT correspondiente.

2. Activa el entorno virtual oficial de Hailo (ajusta la ruta según el directorio donde lo hayas clonado):

```Bash
source ~/hailo-rpi5-examples/venv_hailo_rpi5_examples/bin/activate
```
1. Asegúrate de colocar tu modelo compilado `yolov8n_leaf_416_v2.hef` dentro de la carpeta `resources/`.

2. Ejecuta la aplicación indicando el modo de hardware nativo:

```Bash
export APP_MODE=hailo
python main.py
```

### Autor
Ing. Salvador Santos Romero 

Trabajo desarrollado como parte de la investigación de Tesis en la Maestría en Ciencias en Computación Avanzada y Electrónica.
