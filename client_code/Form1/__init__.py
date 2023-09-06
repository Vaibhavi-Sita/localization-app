from ._anvil_designer import Form1Template
from anvil import *

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def getData(self, **event_args):
    """This method is called when the button is clicked"""
    # output = anvil.server.call('getData', 
    #                             self.question.text)
    # if getData:
    #   self.outputData = output;
    self.outputData = self.update_json(self.oldData, self.newDta)
    pass

  def update_json(self, old_data, new_data):
    # with open(old_file_path, 'r') as old_file, open(new_file_path, 'r') as new_file:
    #     old_data = json.load(old_file)
    #     new_data = json.load(new_file)

    updated_data = update_json_values(old_data, new_data)
    return updated_data

  def update_json_values(self, old_data, new_data):
      if isinstance(old_data, dict) and isinstance(new_data, dict):
          updated_data = {}
          for key in old_data:
              if key in new_data:
                  updated_data[key] = update_json_values(old_data[key], new_data[key])
              else:
                  updated_data[key] = old_data[key]
          for key in new_data:
              if key not in old_data:
                  updated_data[key] = new_data[key]
          return updated_data
      elif isinstance(old_data, list) and isinstance(new_data, list):
          updated_data = []
          for i in range(min(len(old_data), len(new_data))):
              updated_data.append(update_json_values(old_data[i], new_data[i]))
          if len(new_data) > len(old_data):
              updated_data.extend(new_data[len(old_data):])
          return updated_data
      else:
          return new_data