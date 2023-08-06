from sqlpie.model_engine import ModelEngine
from sqlpie.project import Project
from sqlpie.exceptions import BadInputError, UnknownSourceError
import yaml
import dag

class Sqlpie:
	#render single model
	#Sqlpie(model = 'model_1')
	#render single model with payload
	#Sqlpie(model = 'model_1', vars_payload={'key': 'value'}) 
	#render multiple selected models
	#Sqlpie(models = ['model_1', 'model_2']) 
	#render multiple selected models with payload
	#Sqlpie(models = ['model_1', 'model_2'], {'model_1': {'key': 'value'}})
	#render all but model that are passed in the excludes params
	#Sqlpie(excludes = ['model_3', model_4])
	#render all but model that are passed in the excludes params with payloads
	#Sqlpie(excludes = ['model_3', model_4], vars_payload={'model_1': {'key': value}}) 
	#render all models
	#Sqlpie()
	#render all models with payload
	#Sqlpie(vars_payload={'model_1': {'key':'value'}, 'model_2': { 'key': 'value' }})
  #render all models
  #include in client only selected models
	def __init__(self, **kwargs):
		if 'vars_payload' in kwargs.keys() and 'dynamic_env' in kwargs['vars_payload']:
			self.dynamic_env = kwargs['vars_payload']['dynamic_env']
		else:
			self.dynamic_env = None
		self.models = {}
		self.table_index = {}
		self.file_path_index = {}
		self.sources_conf = Project.sources()
		self.api_data = {'models': {}, 'selected_models': [], 'dag': {} }
		self.args = kwargs
		conf_keys = list(kwargs.keys())
		conf_keys.sort()
		self.dag = dag.DAG()
		self.dag_edges = []
		if not kwargs:
			self.render_all()
		elif conf_keys == ['vars_payload']:
			self.render_all(vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['models']:
			self.render_multiple(models=kwargs['models'])
		elif conf_keys == ['models', 'vars_payload']:
			self.render_multiple(models=kwargs['models'], vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['excludes']:
			self.exclude_and_render(excludes=kwargs['excludes'])
		elif conf_keys.sort() == ['excludes', 'vars_payload']:
			self.exclude_and_render(excludes=kwargs['excludes'], vars_payload=kwargs['vars_payload'])
		else:
			raise BadInputError
		self.api_data['dag'] = self.build_dag_api_data(self.dag)
		self.build_table_index()
		self.api_data['table_index'] = self.table_index
		self.api_data['file_path_index'] = self.file_path_index
		self.build_viz_api_data()

	def render_all(self, vars_payload={}):
		all_models = Project.models()
		self.render_multiple(all_models, vars_payload)

	def exclude_and_render(self, excludes, vars_payload={}):
		all_models = Project.models()
		models_after_exclusion = [i for i in all_models if not i in excludes]
		self.render_multiple(models=models_after_exclusion, vars_payload=vars_payload)

	def render_multiple(self, models, vars_payload={}):
		for model in Project.models():
			model_payload = {}
			if vars_payload.keys():
				if self.dynamic_env:
					model_payload['dynamic_env'] = self.dynamic_env
				if model in vars_payload.keys():
					model_payload.update(vars_payload[model])					
				rendered_model = self.render_single(model, model_payload)
			else:
				rendered_model = self.render_single(model)
			if model in models:
				self.api_data['selected_models'].append(model)
				self.append_to_dag(rendered_model)

	def render_single(self, model, vars_payload={}):
		model = ModelEngine(model, vars_payload)
		self.models[model.model] = model
		self.api_data['models'][model.model] = self.build_model_api_data(model)
		return model

	def build_model_api_data(self, model):
		api_data = self.build_dag_api_data(model.dag)
		api_data['prep_model'] = model.prep_model
		api_data['sources'] =  model.model_sources
		api_data['rendered_model'] = model.rendered_model
		if self.dynamic_env:
			api_data['dynamic_env'] = model.dynamic_env_model
		return api_data

	def build_dag_api_data(self, dag):
		return 	{
							'ind_nodes': dag.ind_nodes(),
							'all_leaves': dag.all_leaves(),
							'graph_object': self.parse_graph_object(dag.graph),
							'dag_topological_sort': dag.topological_sort(),
							'dag_index': self.build_dag_index(dag)
						}

	def append_to_dag(self, model):
		for edge in model.edges:
			source_table = edge[0]
			destination_table = edge[1]
			self.dag.add_node_if_not_exists(source_table)
			self.dag.add_node_if_not_exists(destination_table)
			if edge not in self.dag_edges:
				self.dag_edges.append(edge)
				self.dag.add_edge(source_table, destination_table)

	def build_dag_index(self, dag):
		obj = {}
		for node in dag.topological_sort():
			obj[node] = {'predecessors': sorted(dag.predecessors(node)), 'downstreams': sorted(dag.downstream(node)) }
		return obj

	def parse_graph_object(self, graph):
		dict_graph = dict(graph)
		for key in dict_graph.keys():
			dict_graph[key] = list(dict_graph[key])
		return dict_graph

	def build_viz_api_data(self):
		for model_name, model in self.models.items():
			self.api_data['models'][model_name]['viz_data'] = self.generate_viz_data_from_dag(model.dag)
		self.api_data['dag']['viz_data'] = self.generate_viz_data_from_dag(self.dag)

	def generate_viz_data_from_dag(self, dag):
		data_for_viz = []
		for table in dag.topological_sort():
			downstream = dag.downstream(table)
			table_metadata = self.table_index[table]
			for dep_table in downstream:
				dep_table_metadata = self.table_index[dep_table]
				data_for_viz.append({
														'from': table,
														'to': dep_table,
														'weight': 1,
														'custom_field':{
																						'source_schema': table_metadata['schema'], 
																						'destination_schema': dep_table_metadata['schema']
																						}
													})
		return data_for_viz

	def build_table_index(self):
		for model_name, model in self.models.items():
			for table, table_metadata in model.rendered_model.items():
				self.table_index[table] = self.convert_model_metadata(model, table, table_metadata)
				self.file_path_index[table_metadata['file_path']] = table
		for model_name, model in self.models.items():
			for table, table_metadata in model.model_sources.items():
				if table_metadata['source_type'] in ['model', 'prep_model']:
					if not table in self.table_index.keys():
						raise UnknownSourceError(UnknownSourceError.message(table))
				if table_metadata['source_type'] in ['other_model', 'other_prep_model', 'prep_model']:
					if not table in self.table_index.keys():
						raise UnknownSourceError(UnknownSourceError.message(table))
					if not 'included_in' in self.table_index[table].keys():
						self.table_index[table]['included_in'] = []
					self.table_index[table]['included_in'].append(model_name)
				elif table_metadata['source_type'] == 'source':
					if not table in self.table_index.keys():
						self.table_index[table] = table_metadata
						self.table_index[table]['included_in'] = []
					self.table_index[table]['included_in'].append(model_name)
					source_conf = self.sources_conf[self.table_index[table]['source_name']]
					table_short_name = self.table_index[table]['table_short_name']
					if 'tables' in source_conf.keys() and table_short_name in source_conf['tables'].keys():
						self.table_index[table]['description'] = source_conf['tables'][table_short_name]['description']
								
					
		
	def convert_model_metadata(self, model, table_name, table_metadata):
		metadata =  {
									'file_path': table_metadata['file_path'],
									'source_name': model.model,
									'schema': table_metadata['execution_metadata']['destination_schema'],
									'table_name': table_name,
									'table_short_name': table_metadata['table_short_name'],
									'update_method': table_metadata['execution_metadata']['update_method']
								}
		if 'description' in table_metadata.keys():
			metadata['description'] = table_metadata['description']

		if metadata['schema'] == model.prep_model:
			metadata['source_type'] = 'prep'
		else:
			metadata['source_type'] = 'model'
		return metadata
	
	def render_from_tables(self, tables):
		self.from_tables_dag_edges = []
		self.from_tables_dag = dag.DAG()
		self.build_specific_tables_dag(tables)
		self.api_data['from_tables_dag'] = self.build_dag_api_data(self.from_tables_dag)
		self.api_data['from_tables_dag']['viz_data'] = self.generate_viz_data_from_dag(self.from_tables_dag)
	
	def build_specific_tables_dag(self, tables):
		i = 0
		while i < len(tables):
			downstreams = self.api_data['dag']['dag_index'][tables[i]]['downstreams']
			for downstream_table in downstreams:
				self.append_to_specific_tables_dag(tables[i], downstream_table)
			self.build_specific_tables_dag(downstreams)
			i+=1
	
	def build_diff_downstream_path(self, diff):
		self.diff_downstream_path = diff
		self.get_table_downstreams(diff)

	def get_table_downstreams(self, tables):
		i = 0
		while i < len(tables):
			downstreams = self.api_data['dag']['dag_index'][tables[i]]['downstreams']
			for downstream_table in downstreams:
				self.diff_downstream_path.append(downstream_table)
			self.build_specific_tables_dag(downstreams)
			i+=1

	def append_to_specific_tables_dag(self, source_table, destination_table):
		edge = [source_table, destination_table]
		self.from_tables_dag.add_node_if_not_exists(source_table)
		self.from_tables_dag.add_node_if_not_exists(destination_table)
		if edge not in self.from_tables_dag_edges:
			self.from_tables_dag_edges.append(edge)
			self.from_tables_dag.add_edge(source_table, destination_table)


