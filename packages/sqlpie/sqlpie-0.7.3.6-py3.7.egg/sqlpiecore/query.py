from jinja2 import Environment

class Compiler:

  def __init__(self, query_path, payload = {}):
    self.raw_template = open(query_path, 'r').read()
    self.payload = payload
    self.jinja = Environment()
    self.query_template = self.jinja.from_string(self.raw_template)
    self.query_string = self.query_template.render(self.payload)

  def print_template(self):
    print(self.raw_template)

  def print_query(self):
    print(self.query_string)
