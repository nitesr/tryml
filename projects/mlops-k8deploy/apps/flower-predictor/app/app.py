from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
import numpy as np

from flower_predictor.predict import FlowerClassifier

classifer = FlowerClassifier(model_path='./model_iris_final.h5')

class PredictRequest(BaseModel):
    sepalLength: float
    sepalWidth: float
    petalLength: float
    petalWidth: float
    
class PredictResult(BaseModel):
    label: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/api/health/liveness')
def liveness(request: Request):
    return {}

@app.get('/api/health/readiness')
def liveness(request: Request):
    return {}

@app.post("/api/predict")
def predict(req: PredictRequest):
    try :
        x = np.array([[req.sepalLength, req.sepalWidth, req.petalLength, req.petalWidth]])
        result = classifer.predict(x)
        return PredictResult(label=result[0])
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)