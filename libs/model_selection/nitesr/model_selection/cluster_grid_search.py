import numpy as np
import pandas as pd

from sklearn.model_selection import ParameterGrid
from sklearn.manifold import TSNE
from sklearn.base import clone
from sklearn.metrics import silhouette_score

class ClusterGridSearch:
    
    def __init__(self, estimator, param_grid, scorer=silhouette_score, positive=1):
        self.param_grid = param_grid
        self.base_estimator = estimator
        self.scorer = scorer
        self.positive = positive
        self.tsne_z = None
        
    def fit(self, X):
        best_estimator = self.base_estimator
        best_score = np.NaN
        best_params = {}
        
        params = ParameterGrid(self.param_grid)
        results = {'score': []}
        
        for param in params:
            estimator = clone(self.base_estimator)
            estimator = estimator.set_params(**clone(param, safe=False))
            estimator = estimator.fit(X)
            
            score = self.scorer(X, estimator.labels_)
            for key in param:
                if not key in results.keys():
                    results[key] = []
                results[key].append(param[key])
            results['score'].append(score)
            
            if best_score is np.NaN:
                best_score = score
                best_estimator = estimator
                best_params = param.copy()
            elif self.positive*score > self.positive*best_score:
                best_score = score
                best_estimator = estimator
                best_params = param.copy()
            
        self.best_estimator_ = best_estimator
        self.best_score_ = best_score
        self.best_params_ = best_params
        self.results_ = results
            
        return self

    def plot(self, axis):
        axis.plot(self.results_['n_clusters'], self.results_['score'], color='k')
        axis.grid(color='grey', linestyle='--', linewidth=0.2)
        axis.set_title(self.scorer.__name__)
        axis.set_xlabel('#Clusters', color='b')
        axis.axvline(x=self.best_params_['n_clusters'], ymin=0, linewidth=2, color='r', linestyle='--')
        return self
    
    def scatter(self, X, axis):
        axis.scatter(X[:,0], X[:,1],c=self.best_estimator_.labels_);
        axis.grid(True)
        return self
    
    def tsne_plot(self, X, axis):
        tsne = TSNE(n_components=2, verbose=0, random_state=123)
        if self.tsne_z is None:
            self.tsne_z = tsne.fit_transform(pd.DataFrame(X))
        axis.scatter(self.tsne_z[:,0], self.tsne_z[:,1],c=self.best_estimator_.labels_)
        axis.grid(True)
