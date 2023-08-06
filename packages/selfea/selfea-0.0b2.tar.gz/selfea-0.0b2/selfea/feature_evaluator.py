from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
import numpy as np

import HMF

from .utils.data_structure_utils import return_indices


class FeatureEvaluator():
    
    def __init__(self, task_manager, cv):
        
        self.task_manager = task_manager
        self.cv = cv
        
    def evaluate_feature(self, current_features, new_feature, i):
        """
        Requirements:
        - read in data
        - create train/valid split ith iter
        - evaluate 
        - return feature name, score tuple
        """
        
        self.current_features = current_features
        self.new_feature = new_feature
        self.i = i
        
        X, y = self._load_data(current_features, new_feature)
        X_train, X_valid, y_train, y_valid, train_index, valid_index = self._train_valid_split(X, y, i)
        model_algo = self._fit_model(self.task_manager.model_algo, X_train, y_train)
        score = self._evaluate_model(model_algo, X_valid, y_valid, valid_index)
        
        return score
        
    def _load_data(self, current_features, new_feature):
        
        root_dirpath = self.task_manager.root_dirpath
        f = HMF.open_file(root_dirpath, mode='r+')
        
        data_array = f.get_array('/data_array')
        column_names = list(f.get_node_attr('/column_names', key='column_names'))
        
        new_features = current_features + [new_feature]
        feature_column_indices = return_indices(column_names, new_features)
        target_column_index = return_indices(column_names, [self.task_manager.target])
        
        X = data_array[:, feature_column_indices]
        y = data_array[:, target_column_index]
        
        return X, y
        
    def _train_valid_split(self, X, y, i):
        
        for idx, (train_index, valid_index) in enumerate(self.cv.split(X)):
            
            if idx == i:
                # continue

            
                X_train, y_train = X[train_index], y[train_index]
                X_valid, y_valid = X[valid_index], y[valid_index]

                break

        return X_train, X_valid, y_train, y_valid, train_index, valid_index
        
    
    def _fit_model(self, model_algo, X_train, y_train):
        """may require configurable preprocess steps..."""

        self.model_algo = model_algo
        self.model_algo.fit(X_train, y_train)
        return self.model_algo
        
    
    def _evaluate_model(self, model_algo, X_valid, y_valid, valid_index):

        
        
        if self.task_manager.evaluation_method:
            
            result = self.task_manager.evaluation_method(X_valid=X_valid,
                                                         y_valid=y_valid,
                                                         valid_index=valid_index,
                                                         model_algo=model_algo,
                                                         task_manager=self.task_manager,
                                                         i=self.i,
                                                         cv=self.cv,
                                                         self_state=self)
            
            return result
        
        preds = model_algo.predict(X_valid)
        
        rmse_score = np.sqrt(mse(preds, y_valid))
        mae_score = mae(preds, y_valid)
        composite_score = rmse_score/2.0 + mae_score/2.0
        return (np.mean(preds), np.mean(X_valid.ravel()))
        