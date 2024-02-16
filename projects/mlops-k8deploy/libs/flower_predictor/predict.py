import joblib
import numpy as np

class FlowerClassifier:
    def __init__(
        self,
        flower_kinds = ['setosa', 'versicolor', 'virginica'], 
        model_path='./model_iris_final.h5') -> None:
        self.model_path = model_path
        self.flower_kinds = flower_kinds
    
    def predict(self, x):
        if not x.shape[1] == 4:
            raise ValueError('expect the input shape to be (n, 4)')
        
        if x.shape[0] == 1:
            x = np.reshape(x, (1, 4))
        
        model = joblib.load(self.model_path)
        Y_pred = model.predict(x)
        predictions = [ self.flower_kinds[y] for y in Y_pred ]
        return predictions