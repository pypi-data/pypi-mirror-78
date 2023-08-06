# run pip install -r requirements.txt
import glob
import sys
from os import listdir
import yaml
from sqlpie.exceptions import MissingModelConfigFile
from pandas.core.common import flatten

class Project:

	@staticmethod
	def models(dynamic_env=None):
		all_paths = Project._all_model_paths()
		all_models = list(map(lambda x: x.split('/')[-1].split('.')[0] , all_paths))
		if dynamic_env:
			dynamic_env_models = []
			for model in all_models:
				dynamic_env_models.append( Project.dynamic_env_table_name(dynamic_env, model) )
			return dynamic_env_models
		else:
			return all_models

	@staticmethod
	def prep_models(dynamic_env=None):
		prep_models = []
		models = Project.models()
		dynamic_env_models = Project.models(dynamic_env)
		for i in range(len(models)):
			model_config = Project.get_model_config(models[i])
			if model_config and 'prep_schema' in model_config.keys():
				if dynamic_env:
					prep_model = model_config['prep_schema']
				else:
					prep_model = model_config['prep_schema']
				prep_models.append(prep_model)
			else:
				if dynamic_env:
					prep_model = f"{dynamic_env_models[i]}_prep"
				else:
					prep_model = f"{models[i]}_prep"
				prep_models.append(prep_model)
		return prep_models

	@staticmethod
	def sources():
		sources_config_file = open("./config/sources.yml", "r")
		sources_conf = yaml.load(sources_config_file, Loader=yaml.FullLoader)
		sources_config_file.close()
		return sources_conf

	@staticmethod
	def project_payload(**kwargs):
		payload_list = []
		payload = {}
		models = Project.models()
		prep_models = Project.prep_models()
		if 'dynamic_env' in kwargs.keys():
			for model in models:
				payload_list.append( Project.dynamic_env_table_name(kwargs['dynamic_env'], model))
			for prep_model in prep_models:
				payload_list.append(Project.dynamic_env_table_name(kwargs['dynamic_env'], prep_model))
		else:
			payload_list.append(models)
			payload_list.append(prep_models)
		payload_list.append(list(Project.sources().keys()))
		return list(flatten(payload_list))

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
	
	@staticmethod
	def dynamic_env_table_name(dynamic_env, table_name):
		return f"{dynamic_env}_{table_name}"