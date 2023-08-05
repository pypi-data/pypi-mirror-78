# run pip install -r requirements.txt
from sqlpie.compiler import Compiler
from sqlpie.project import Project
import glob
import sys
import yaml
import dag
from os import listdir
from os.path import isfile, join
from sqlpie.exceptions import UnknownSourceError

class ModelEngine:

  def __init__(self, model, vars_payload={}):
    self.all_models = Project.models()
    self.all_staging_models =  Project.staging_models()
    self.model = model
    self._set_source_conf()
    self.model_config = Project.get_model_config(self.model)
    self._vars_payload = vars_payload
    self.model_path = self._get_model_path()
    self.staging_model = self._set_staging_table_name()
    self._model_queries_path = glob.glob(self.model_path)
    self._set_payload()
    self.model_sources = {}
    self._current_query = None
    self.rendered_model = {}
    self.edges = []
    self.dag = dag.DAG()
    self._render_model()
  
  def _get_model_path(self):
    return f"./models/{self.model}/*.sql"
  
  def _load_snippets(self):
    path = './snippets'
    sys.path.append(path)
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
  
  #triggered when the source block is rendered
  def source(self, source_name, table_name):
    source_table = f"{source_name}.{table_name}"
    if source_name == self.model:
      source_name = self.model
      source_schema = source_name
      source_type = 'model'
    elif source_name ==  self.staging_model:
      source_name = self.model
      source_schema = source_name
      source_type = 'staging_model'
    elif source_name in self.all_models:
      source_schema = source_name
      source_type = 'other_model'
    elif source_name in self.all_staging_models:
      source_schema = source_name
      source_type = 'other_stagings_model'
    else:
      try:
        source_schema = self.sources_conf[source_name]['schema_name']
        source_type = 'source'
      except KeyError:
        raise UnknownSourceError(UnknownSourceError.message(source_name))
      update_method = None
    destination_table =f"{self._execution_metadata['destination_schema']}.{self._execution_metadata['destination_table']}"
    self.model_sources[source_table] = { 
                                          'source_type': source_type,
                                          'source_name': source_name, 
                                          'schema': source_schema,
                                          'table_name': source_table,
                                          'table_short_name': table_name,
                                          'destination_table': destination_table
                                        }
    self.dag.add_node_if_not_exists(destination_table)
    self.dag.add_node_if_not_exists(source_table)
    edge = [source_table, destination_table]
    if edge not in self.edges:
      self.edges.append(edge)
      self.dag.add_edge( source_table, destination_table)
    if source_name in self.sources_conf.keys():
      return f"{self.sources_conf[source_name]['schema_name']}.{table_name}"
    else:
      return source_table

  #triggered when the config block is rendered
  def query_execution_config(self, **kargs):
    #input validation 
    self._execution_metadata = kargs
    if 'staging' in self._execution_metadata.keys():
      if self._execution_metadata['staging'] == True:
        self._execution_metadata['destination_schema'] = self.staging_model
    else:
      self._execution_metadata['destination_schema'] = self.model
    return ''

  def _update_current_query(self, query):
    self.current_query = query
  
  def _parse_template_query(self, template):
    config = '\n' + template.split('}}')[0] + "}}"
    query = str('}}').join( template.split('}}')[1:])
    return {'config': config, 'query': query}

  def _render_model(self):
    for path in self._model_queries_path:
      self._update_current_query(path)
      rendered_query =  self._render_query(path)
      file_suffix = path.split('/')[-1].split('.')[1]
      if file_suffix == 'sql':
        table_short_name = self._execution_metadata['destination_table']
        table_name = f"{self._execution_metadata['destination_schema']}.{table_short_name}"
        self.rendered_model[table_name] = {}
        self.rendered_model[table_name]['rendered_query'] = rendered_query
        query_template = open(path, 'r')
        self.rendered_model[table_name]['template'] = self._parse_template_query(query_template.read())
        query_template.close()
        self.rendered_model[table_name]['execution_metadata'] = self._execution_metadata
        self.rendered_model[table_name]['table_short_name'] = table_short_name
        self.rendered_model[table_name]['file_path'] = path
        if 'description' in self.model_config.keys():
          if table_short_name in self.model_config['description']['tables'].keys():
            self.rendered_model[table_name]['description'] = self.model_config['description']['tables'][table_short_name]


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
    
  def _set_payload(self):
    self.payload = self._load_snippets()
    self.payload['model'] = self.model
    self.payload['vars'] = self._vars_payload
    self.payload['staging_model'] = self.staging_model
    self.payload['config'] = self.query_execution_config
    self.payload['source'] = self.source

  def print_query(self, destination_table):
    print(self.rendered_model[destination_table])
    return self.rendered_model[destination_table]
