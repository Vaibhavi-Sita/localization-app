from ._anvil_designer import Form1Template
from anvil import *
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
    return json.dumps(updated_data, indent=4)

  def update_json_values(self, old_data, new_data):
      
      if isinstance(old_data, dict) and isinstance(new_data, dict):
          updated_data = {}
          for key in old_data:
              if key in new_data:
                  updated_data[key] = self.update_json_values(old_data[key], new_data[key])
              else:
                  updated_data[key] = old_data[key]
          # Discarded keys       
          for key in new_data:
              if key not in old_data:
                self.logs.text += "DISCARDED: " + "\n" + key + ": " + new_data[key] + "\n"
          #         updated_data[key] = new_data[key]
          # Newly Added keys       
          for key in old_data:
              if key not in new_data:
                self.logs.text += "NEWLY ADDED: " + "\n" + key + ": " + old_data[key] + "\n"
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

  def downloadData(self, **event_args):
    """This method is called when the downlaod button is clicked"""
    # BlobMedia("text/plain", self.outputData, [name=output])
    if(self.outputFileName.text == ""):
      self.outputFileName.text = "output"
    updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=self.outputData.text.encode(), name=self.outputFileName.text+".json")
    anvil.media.download(updatedJsonFile) 
  