from ._anvil_designer import Form3Template
from anvil import *
import anvil.media
import json
import http.client

class Form3(Form3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def getData(self, **event_args):
    """This method is called when the submit button is clicked"""
    self.logs.text = ""
    self.outputData.text = self.update_json(self.oldData)
    pass

  def update_json(self, old_data):

    old_data = json.loads(old_data.text)
    updated_data = self.update_json_values(old_data)
    return json.dumps(updated_data, indent=4)

  def update_json_values(self, old_data):
    if isinstance(old_data, dict):
      updated_data = {}
      for key in old_data:
        updated_data[key] = self.update_json_values(old_data[key])
      return updated_data

  conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
  
  payload = "q=English%20is%20hard%2C%20but%20detectably%20so"
  
  headers = {
      'content-type': "application/x-www-form-urlencoded",
      'Accept-Encoding': "application/gzip",
      'X-RapidAPI-Key': "d4faedeecamsha6e48bd17aecf54p1ad727jsn89f4ce00e486",
      'X-RapidAPI-Host': "google-translate1.p.rapidapi.com"
  }
  
  conn.request("POST", "/language/translate/v2/detect", payload, headers)
  
  res = conn.getresponse()
  data = res.read()
  
  print(data.decode("utf-8"))

  def downloadData(self, **event_args):
    """This method is called when the downlaod button is clicked"""
    # BlobMedia("text/plain", self.outputData, [name=output])
    if(self.outputFileName.text == ""):
      self.outputFileName.text = "output"
    updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=self.outputData.text.encode(), name=self.outputFileName.text+".json")
    anvil.media.download(updatedJsonFile)


