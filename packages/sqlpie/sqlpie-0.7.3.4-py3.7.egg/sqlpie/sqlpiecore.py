# run pip install -r requirements.txt
from sqlpie.compiler import Compiler
from sqlpie.project import Project
import glob
import sys
import yaml
import dag
from os import listdir
from os.path import isfile, join

class Sqlpie:

  def __init__(self, model, vars_payload={}):
    self.all_models = Project.models()
    self.model = model
    self._set_source_conf()
    self._set_models_conf()
    self.model_path = self._get_model_path()
    self.model_sources = {}
    self.staging_model = self._set_staging_table_name()
    self._model_queries_path = glob.glob(self.model_path)
    self.payload = self._load_snippets()
    self.payload['model'] = self.model
    self.payload['vars'] = vars_payload
    self.payload['staging_model'] = self.staging_model
    self.payload['config'] = self._query_execution_config
    self.payload['source'] = self._source
    self._current_query = None
    self.rendered_model = {}
    self.edges = []
    self.dag = dag.DAG()
    self._render_model()
  
  def _get_model_path(self):
    return f"./models/{self.model}/*.sql"
  
  def _load_snippets(self):
    sys.path.append('./snippets')
    path = './snippets'
    snippets = [f for f in listdir(path) if isfile(join(path, f))]
    payload = {}
    for snippet in snippets:
      prefix = snippet.split('.')[0]
      suffix = snippet.split('.')[1]
      if suffix == 'py' and prefix != '__init__':
        modname = prefix
        mod = __import__(modname)
        payload[modname] = mod
    return payload

  def _source(self, source_name, table_name):
    source_table = f"{source_name}.{table_name}"
    if source_name in [self.model, self.staging_model]:
      source_schema = source_name
    elif source_name in self.all_models:
      source_schema = source_name
    else:
      source_schema = self.sources_conf[source_name]['schema']
    destination_table =f"{self._execution_metadata['destination_schema']}.{self._execution_metadata['destination_table']}"
    self.model_sources[source_table] = { 
                                          'source_name': source_name, 
                                          'schema': source_schema,
                                          'table_name': table_name,
                                          'update_method': None
                                        }
    self.dag.add_node_if_not_exists(destination_table)
    self.dag.add_node_if_not_exists(source_table)
    edge = [source_table, destination_table]
    if edge not in self.edges:
      self.edges.append(edge)
      self.dag.add_edge( source_table, destination_table)
    if source_name in self.sources_conf.keys():
      return f"{self.sources_conf[source_name]['schema']}.{table_name}"
    else:
      return source_table

  def _update_current_query(self, query):
    self.current_query = query

  def _query_execution_config(self, **kargs):
    self._execution_metadata = kargs
    if 'staging' in self._execution_metadata.keys():
      if self._execution_metadata['staging'] == True:
        self._execution_metadata['destination_schema'] = self.staging_model
    else:
      self._execution_metadata['destination_schema'] = self.model
    return None
  
  def _parse_template_query(self, template):
    config = '\n' + template.split('}}')[0] + "}}"
    query = str('}}').join( template.split('}}')[1:])
    return {'config': config, 'query': query}

  def _render_model(self):
    for path in self._model_queries_path:
      self._update_current_query(path)
      rendered_query =  self._render_query(path)
      table_name = f"{self._execution_metadata['destination_schema']}.{self._execution_metadata['destination_table']}"
      self.rendered_model[table_name] = {}
      self.rendered_model[table_name]['rendered_query'] = rendered_query
      query_template = open(path, 'r')
      self.rendered_model[table_name]['template'] = self._parse_template_query(query_template.read())
      query_template.close()
      self.rendered_model[table_name]['execution_metadata'] = self._execution_metadata

  def _render_query(self, path=None):
    rendered_query = Compiler(path, self.payload).query_string[1:]
    return rendered_query
  
  def _set_source_conf(self):
    sources_config_file = open("./config/sources.yml", "r")
    self.sources_conf = yaml.load(sources_config_file, Loader=yaml.FullLoader)
    sources_config_file.close()

  def _set_staging_table_name(self):
    if self.model_config and 'staging_schema' in self.model_config.keys():
      return self.model_config['staging_schema']
    else:
      return f"{self.model}_staging"
  
  def _set_models_conf(self):
    models_config_file = open(f"./models/{self.model}/model_config.yml", "r")
    self.model_config = yaml.load(models_config_file, Loader=yaml.FullLoader)
    models_config_file.close()
  
  def print_query(self, destination_table):
    print(self.rendered_model[destination_table])
    return self.rendered_model[destination_table]
  
  def get_table_metadata(self, table_name):
    if table_name in self.model_sources.keys():
      return self.model_sources[table_name]
    elif table_name in self.rendered_model.keys():
      return {
                'table_name': self.rendered_model[table_name]['execution_metadata']['destination_table'],
                'schema': self.model,
                'update_method': self.rendered_model[table_name]['execution_metadata']['update_method']
              }
    else:
      return {
              'table_name': table_name,
              'schema': table_name,
              'update_method': None
              } 

  def viz_data_prep(self):
    data_for_viz = []
    for table in self.dag.topological_sort():
      downstream = self.dag.downstream(table)
      for dep_table in downstream:
        table_metadata = self.get_table_metadata(table)
        dep_table_metadata = self.get_table_metadata(dep_table)
        data_for_viz.append({
                              'from': table, 
                              'to': dep_table,
                              'weight': 1,
                              'custom_field': {
                                                'source_schema': table_metadata['schema'], 
                                                'destination_schema': dep_table_metadata['schema']
                                              }
                            })
    return data_for_viz