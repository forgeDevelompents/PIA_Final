from PIL import Image
from io import BytesIO
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import base64
import torch

from langchain.tools import tool  

# Carga del modelo YOLOv8 desde Hugging Face (solo se hace una vez)
yolo_model_path = hf_hub_download(repo_id="eidrieenbe/yolov8-novex-pallets", filename="best.pt")
yolo_model = YOLO(yolo_model_path)

def detect_pallets_from_bytes(image_bytes: bytes) -> dict:
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        results = yolo_model(image)

        boxes = results[0].boxes
        count = len(boxes)
        confidence = boxes.conf.mean().item() if count > 0 else 0.0

        return {
            "num_pallets": count,
            "mean_confidence": round(confidence, 4)
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def vision_tool(image_path: str) -> dict:
    """
    Detecta pallets en una imagen dada por su ruta local.
    Devuelve el número de pallets detectados y la confianza media.
    """
    import os
    from agents.vision_agent import detect_pallets_from_bytes

    if not os.path.exists(image_path):
        return {"error": "La imagen no existe."}
    
    with open(image_path, "rb") as f:
        return detect_pallets_from_bytes(f.read())

def detect_pallets_from_base64(image_b64: str) -> dict:
    try:
        image_bytes = base64.b64decode(image_b64)
        return detect_pallets_from_bytes(image_bytes)
    except Exception as e:
        return {"error": str(e)}
