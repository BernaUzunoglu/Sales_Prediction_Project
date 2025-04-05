from fastapi import APIRouter, HTTPException
from api.models.customer_segment_request_model import CustomerSegmentRequest
from api.utils.model_loader import load_model
from config import Config
import pandas as pd

# Router
router = APIRouter()

# Model dosyasını yükle
pipeline_path = Config.PROJECT_ROOT / "src" / "models" / "saved_models" / "customer_segmentation_pipeline.pkl"
pipeline = load_model(pipeline_path)

@router.post("/predict-segment", tags=["Segmentation"])
def predict_segment(request: CustomerSegmentRequest):
    try:
        # Gelen veriyi DataFrame'e çevir
        input_df = pd.DataFrame([request.dict()])

        # Normalize et
        scaled_input = pipeline["scaler"].transform(input_df)

        # Segment tahmini
        segment_id = pipeline["model"].predict(scaled_input)[0]
        segment_name = pipeline["segment_map"].get(segment_id, "Unknown")

        return {
            "segment_id": int(segment_id),
            "segment_name": segment_name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin yapılamadı: {str(e)}")
