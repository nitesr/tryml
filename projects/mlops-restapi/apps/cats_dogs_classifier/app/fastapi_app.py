from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
import base64

from cats_dogs_classifier.predict import DogCatClassifier

create_classifier = lambda: DogCatClassifier('model_final.h5')

class PredictRequest(BaseModel):
    image: str
    
class PredictResult(BaseModel):
    label: str


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/predict")
def predict(req: PredictRequest):
    f = req.image
    img = base64.b64decode(f)
    result = create_classifier().predict_bytes(img)
    return PredictResult(label=result['label'])
