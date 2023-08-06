from selfea.utils.data_structure_utils import return_indices, get_max_value_key, get_min_value_key
from selfea.dask_clients import ClientFuture
from selfea.feature_evaluator import FeatureEvaluator
from selfea.default_models.default_xgboost_regressor import DefaultXGBoostRegressor
from collections import defaultdict

import numpy as np
import copy
import HMF
from sklearn.model_selection import KFold


class Selfea():
	
	def __init__(self, debug_mode=False):
		
		self.score_tracking_dict = dict()
		self.debug_mode = debug_mode
		
		
	def setup_evaluation(self, task_manager):
		
		self.task_manager = task_manager
		
		
		f = HMF.open_file(self.task_manager.root_dirpath, mode='w+')


		numeric_data = self.task_manager.data.select_dtypes(include=[np.number])

		self.task_manager.data = None


		# numeric_data = self.task_manager.data[self.task_manager.features + [self.task_manager.target, self.task_manager.orderby]]


		f.from_pandas(numeric_data, orderby=self.task_manager.orderby)

		f.register_array('data_array', numeric_data.columns)
		f.set_node_attr('/column_names', key='column_names', value=numeric_data.columns)

		f.close()
		


		
	def run_evaluation(self):
		
		cv = KFold(n_splits=5)
		self.feature_evaluator = FeatureEvaluator(self.task_manager, cv)
		
		if not self.debug_mode:
			self.dask_client = ClientFuture(local_client_n_workers=2, 
											local_client_threads_per_worker=2)
			self.dask_client.get_dashboard_link()

		else:
			self.dask_client = None

		score_tracking_dict, current_features = self._run_feature_selection()
		
		return score_tracking_dict, current_features

		
		
	def _feature_evaluation_futures(self, feature_evaluator, dask_client, feature_stack, current_features):


		if self.debug_mode:

			feature_futures_dict = defaultdict(list)

			for new_feature in feature_stack:

				for i in range(1, 5):

					feature_futures_dict[new_feature].append(feature_evaluator.evaluate_feature(current_features, new_feature, i))

			return feature_futures_dict




		feature_futures_dict = defaultdict(list)

		for new_feature in feature_stack:

			for i in range(1, 5):

				feature_futures_dict[new_feature].append(dask_client.submit(feature_evaluator.evaluate_feature, 
															   current_features, 
															   new_feature,
															   i))

		return feature_futures_dict
	
	def _run_feature_selection(self):
		
		score_tracking_dict = dict()
		
		current_features = []
		feature_stack = copy.copy(self.task_manager.features)
		max_num_features = self.task_manager.max_num_features
		
		counter = 0
		best_score = np.inf

		while(len(feature_stack)>0 and 
			  max_num_features>len(current_features)):

			feature_score_dict = dict()

			feature_futures_dict = self._feature_evaluation_futures(self.feature_evaluator, 
																	self.dask_client, feature_stack, current_features)



			for k, v in feature_futures_dict.items():

				if self.debug_mode:
					score = score = [future.result() for future in v]
				else:
					score = np.mean([future.result() for future in v])
# 
					# score = [future.result() for future in v]


				feature_score_dict[k] = score

			best_feature = get_min_value_key(feature_score_dict)
			worst_feature = get_max_value_key(feature_score_dict)

			new_score = feature_score_dict[best_feature]

			feature_stack.remove(best_feature)
			current_features.append(best_feature)

			score_tracking_dict[counter] = feature_score_dict
			
			counter += 1

			if self.debug_mode:

				pass

			else:

				if best_score > new_score:
					best_score = new_score
				else:
					print('stopping criterion met!')
					break
			
		return score_tracking_dict, current_features






