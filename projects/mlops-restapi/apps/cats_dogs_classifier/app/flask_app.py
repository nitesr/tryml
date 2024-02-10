from flask import Flask, jsonify, request, render_template
from cats_dogs_classifier.predict import DogCatClassifier
from flask_cors import CORS, cross_origin

import base64
import os
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
create_classifier = lambda: DogCatClassifier('model_final.h5')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/api/predict", methods = ['POST'])
def predict():
    f = request.json['image']
    img = base64.b64decode(f)
    result = create_classifier().predict_bytes(img)
    return jsonify(result)

if __name__ == "__main__":
    app.run(static_folder='static',
            template_folder='templates')