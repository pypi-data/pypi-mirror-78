# run pip install -r requirements.txt
import glob
import sys
from os import listdir
import yaml
from sqlpie.exceptions import MissingModelConfigFile

class Project:
	
	@staticmethod
	def models():
		all_paths = Project._all_model_paths()
		return list(map(lambda x: x.split('/')[-1].split('.')[0] , all_paths))

	@staticmethod
	def staging_models():
		staging_models = []
		models = Project.models()
		for model in models:
			model_config = Project.get_model_config(model)
			if model_config and 'staging_schema' in model_config.keys():
				staging_models.append(model_config['staging_schema'])
			else:
				staging_models.append(f"{model}_staging")
		return staging_models

	@staticmethod
	def model_paths():
		all_paths = Project._all_model_paths()
		models_and_paths = list(map(lambda x: {x.split('/')[-1].split('.')[0]: x} , all_paths))
		models_and_paths_list = {}
		for item in models_and_paths:
			model_name = list(item)[0]
			models_and_paths_list[model_name] = item[model_name]
		return models_and_paths_list

	@staticmethod
	def _all_model_paths():
		return glob.glob('./models/*')
	
	@staticmethod
	def model_config_path(model):
		return f"./models/{model}/model_config.yml"
	
	@staticmethod
	def get_model_config(model):
		try:
			config_file = open(Project.model_config_path(model), "r")
			model_conf = yaml.load(config_file, Loader=yaml.FullLoader)
			config_file.close()
			if model_conf is None:
				return {}
			else:
				return model_conf
		except FileNotFoundError:
			raise MissingModelConfigFile(MissingModelConfigFile.message(model))