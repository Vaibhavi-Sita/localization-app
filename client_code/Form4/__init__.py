from ._anvil_designer import Form4Template
from anvil import *
import anvil.server
import anvil.media
import json
import anvil.http

class Form4(Form4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def getData(self, **event_args):
    """This method is called when the submit button is clicked"""
    self.outputData.text = self.update_json(self.oldData)
    pass

  def update_json(self, old_data):
    old_data = json.loads(old_data.text)
    sourceLanguage  = self.sourceLanguage.text
    targetLanguage = self.targetLanguage.text
    if isinstance(old_data, dict):
      updated_data = {}
      for key in old_data:
        # updated_data[key] = self.getTranslatedData(old_data[key], sourceLanguage, targetLanguage)
        updated_data[key] = self.requestsData(old_data[key], sourceLanguage, targetLanguage)
        
    return json.dumps(updated_data, indent=4)

  def downloadData(self, **event_args):
    """This method is called when the downlaod button is clicked"""
    # BlobMedia("text/plain", self.outputData, [name=output])
    if(self.outputFileName.text == ""):
      self.outputFileName.text = "output"
    updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=self.outputData.text.encode(), name=self.outputFileName.text+".json")
    anvil.media.download(updatedJsonFile)

  def requestsData(self, oldDataValue, sourceLanguage, targetLanguage):
    url = "https://text-translator2.p.rapidapi.com/translate"

    payload = {
    	"source_language": sourceLanguage,
    	"target_language": targetLanguage,
    	"text": oldDataValue
    }

    headers = {
    	"content-type": "application/x-www-form-urlencoded",
    	"X-RapidAPI-Key": "d4faedeecamsha6e48bd17aecf54p1ad727jsn89f4ce00e486",
    	"X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
  
    response = anvil.http.request(url=url,
                    method="POST",
                    data=payload,
                    headers= headers)

    res = response.get_bytes().decode("utf-8")
    res = json.loads(res)
    return res['data']['translatedText']

  def goToForm1(self, **event_args):
    open_form('Form1')
    




