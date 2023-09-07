
import numpy as np

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class HiddenLayerEstimator:
    def __init__(self, num_of_labels=2, verbose=0):
        self.num_of_labels = num_of_labels
        self.verbose = verbose
        return

    def compute_targets(self, X):
        pca_obj = PCA().fit(X)
        cum_var = 0
        
        target_n_components = 0
        target_cum_var = 40
        if self.num_of_labels > 2:
            target_cum_var = 60
            
        for comp in range(0, pca_obj.n_components_):
            target_n_components = target_n_components + 1
            cum_var = cum_var + pca_obj.explained_variance_ratio_[comp]
            
            if self.verbose > 9:
                print(
                    f"PCA_{comp}", 
                    round(pca_obj.explained_variance_ratio_[comp]*100), 
                    round(cum_var*100))
            
            if cum_var > target_cum_var:
                break;
        
        self.target_n_components = target_n_components
        self.target_cum_var = cum_var
        
        return pca_obj, target_n_components
    
    def compute_clusters(self, X):
        params_grid = {'n_clusters': range(2, 20), 'n_init': ['auto']}
        grid_search = ClusterGridSearch(KMeans(), params_grid, scorer=silhouette_score)
        grid_search.fit(X)
        
        return (grid_search, grid_search.best_params_['n_clusters'])
        
    
    def fit(self, X):
        (pca_obj, target_n_components) = self.compute_targets(X)
        
        layers = []
        
        
        X_new = pca_obj.transform(X)
        for nlayer in range(0, target_n_components):
            PC_X = X_new[:, [nlayer]]
            (grid_search, n_clusters) = self.compute_clusters(PC_X)
            
            layers.append({
                'n_neurons': n_clusters, 
                'variance': pca_obj.explained_variance_ratio_[nlayer]
            })
            
            if self.verbose > 0:
                print({
                    'layer': nlayer,
                    'n_neurons': n_clusters, 
                    'variance': pca_obj.explained_variance_ratio_[nlayer]
                })
        
        layers.reverse()
        
        cum_var_curr = 0
        for l in layers:
            cum_var_curr = cum_var_curr + l["variance"]
            l["cum_variance"] = cum_var_curr
        
        
        self.layers_ = layers
        return self

rng = np.random.RandomState(0)
n_samples = 10
cov = [[3, 3], [3, 4]]
X = rng.multivariate_normal(mean=[0, 0], cov=cov, size=n_samples)
print(X)