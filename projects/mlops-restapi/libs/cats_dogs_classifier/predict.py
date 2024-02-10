#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
from io import BytesIO 

class DogCatClassifier:
    def __init__(self, model_path):
        self.model_path = model_path
        
        # Load model
        self.model = load_model(model_path)
    
    def predict(self, file_path):
        with open(file_path, mode="rb") as img_file:
            img_bytes = img_file.read()
            return self.predict_bytes(img_bytes)
        
        
    def predict_bytes(self, image_bytes):
        image = Image.open(BytesIO(image_bytes))
        image = image.resize([64, 64])
  
        # Load and preprocess the image
        test_image = img_to_array(image)
        test_image = np.expand_dims(test_image, axis=0)
        test_image = test_image / 255.0  # Rescale pixel values to the range [0, 1] as done during training

        # Predict the class (0 for cat, 1 for dog)
        result = self.model.predict(test_image)

        if result[0][0] > 0.5:
            prediction = 'dog'
        else:
            prediction = 'cat'

        return {"label": prediction}
