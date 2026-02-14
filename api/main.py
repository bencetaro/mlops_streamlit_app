from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
from api.db import init_db, log_single, log_batch

app = FastAPI()
model = joblib.load("output/model.pkl")

class Item(BaseModel):
    size: float
    n_rooms: int
    quality: int

QUALITY_MAP = {"Low": 3, "Medium": 2, "High": 1}

@app.get("/")
def read_root():
    return {"message": "Model API running"}

@app.get("/model_info")
def get_model_info():
    return {
        "model_name": model.__class__.__name__,
        "model_type": type(model).__name__,
        "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None
    }

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/predict")
async def predict(size: float, rooms: int, quality: str):
    q = QUALITY_MAP.get(quality)
    if q is None:
        return {"error": "Invalid quality"}

    X = [[size, rooms, q]]
    pred = model.predict(X)
    price = float(pred[0])
    log_single(size, rooms, q, price)
    return {"predicted_price": price}

@app.post("/batch_predict")
async def batch_predict(items: List[Item]):
    X = [[i.size, i.n_rooms, i.quality] for i in items]
    preds = model.predict(X)
    log_batch(len(items), float(preds.mean()))
    return {"predictions": preds.tolist()}

