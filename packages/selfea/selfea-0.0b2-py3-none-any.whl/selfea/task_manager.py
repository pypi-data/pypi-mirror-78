
class TaskManager():
    
    def __init__(self, 
                 data,
                 root_dirpath, 
                 features, 
                 target, 
                 orderby,
                 model_algo,
                 max_num_features,
                 stopping_rounds,
                 evaluation_method=None):
        
        self.data = data
        self.root_dirpath = root_dirpath
        self.features = features
        self.target = target 
        self.orderby = orderby
        self.model_algo = model_algo
        self.evaluation_method = evaluation_method

        self.max_num_features = max_num_features
        self.stopping_rounds = stopping_rounds
        