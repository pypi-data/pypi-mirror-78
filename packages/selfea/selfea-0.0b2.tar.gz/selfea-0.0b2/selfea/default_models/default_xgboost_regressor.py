import xgboost as xgb
from sklearn.model_selection import train_test_split

class DefaultXGBoostRegressor():
    
    def __init__(self):
        pass
    
    def fit(self, X, y):
        
        algo = xgb.XGBRegressor(n_estimators=300, tree_method='hist')  
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
        eval_set = [(X_train, y_train), (X_test, y_test)]
        
        self.model_object = algo.fit(X_train, y_train, early_stopping_rounds=10, eval_set=eval_set, verbose=False)
        
    def predict(self, X):
        
        return self.model_object.predict(X)

# import numpy as np
# class DefaultXGBoostRegressor():
    
#     def __init__(self):
#         pass
    
#     def fit(self, X, y):
        
#         algo = xgb.XGBRegressor(n_estimators=300, tree_method='hist')  
        
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
#         eval_set = [(X_train, y_train), (X_test, y_test)]
        
#         self.model_object = None
        
#     def predict(self, X):
        
#         return np.arange(len(X))