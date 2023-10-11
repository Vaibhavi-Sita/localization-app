from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def getData(self, **event_args):
    """This method is called when the submit button is clicked"""
    self.logs.text = ""
    self.outputData.text = self.update_json(self.oldData, self.newData)    
    pass

  def update_json(self, old_data, new_data):
    old_data = json.loads(old_data.text)
    new_data = json.loads(new_data.text)
    
    updated_data = self.update_json_values(old_data, new_data)
    self.checkLogs(old_data,new_data)
    return json.dumps(updated_data, indent=4)

  def update_json_values(self, old_data, new_data):
      if isinstance(old_data, dict) and isinstance(new_data, dict):
          updated_data = {}
          for key in old_data:
              if(isinstance(old_data[key], dict) or isinstance(old_data[key], list)):
                updated_data[key] = self.update_json_values(old_data[key], new_data)
              else:
                if old_data[key] in new_data:
                  updated_data[key] = new_data[old_data[key]]
                else:
                  updated_data[key] = old_data[key]
          return updated_data
      elif isinstance(old_data, list) and isinstance(new_data, list):
          updated_data = []
          for i in range(min(len(old_data), len(new_data))):
              updated_data.append(update_json_values(old_data[i], new_data[i]))
          if len(new_data) > len(old_data):
              updated_data.extend(new_data[len(old_data):])
          return updated_data
      elif isinstance(old_data, list) and isinstance(new_data, dict):
          updated_data = []
          for i in range(len(old_data)):
            if(isinstance(old_data[i], dict) or isinstance(old_data[i], list)):
              updated_data.append(self.update_json_values(old_data[i], new_data))
            else:
              updated_data.append(old_data[i])
          return updated_data
      else:
          return new_data

  def checkLogs(self, old_data, new_data):
      discarded = {}
      newlyAdded = {}
      # Discarded keys       
      for key in new_data:
          if key not in old_data:
            # self.logs.text += "DISCARDED: " + "\n" + key + ": " + new_data[key] + "\n" + "\n"
            discarded[key] = new_data[key]
      #         updated_data[key] = new_data[key]
      # Newly Added keys       
      for key in old_data:
          if key not in new_data:
            # self.logs.text += "NEWLY ADDED: " + "\n" + key + ": " + old_data[key] + "\n" + "\n"
            newlyAdded[key] = old_data[key]

      self.logs.text += "\n NEWLY ADDED VALUES: " + "\n"
      self.logs.text += json.dumps(newlyAdded, indent=4)
      self.logs.text += "\n DISCARDED VALUES: " + "\n"
      self.logs.text += json.dumps(discarded, indent=4)

  def downloadData(self, **event_args):
    """This method is called when the downlaod button is clicked"""
    # BlobMedia("text/plain", self.outputData, [name=output])
    if(self.outputFileName.text == ""):
      self.outputFileName.text = "output"
    updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=self.outputData.text.encode(), name=self.outputFileName.text+".json")
    anvil.media.download(updatedJsonFile) 

  def goToForm4(self, **event_args):
    open_form('Form4')

  def goToForm2(self, **event_args):
    open_form('Form2')

  