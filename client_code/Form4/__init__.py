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
    currentLanguage  = self.currentLanguage.text
    translationLanguage = self.translationLanguage.text
    if isinstance(old_data, dict):
      updated_data = {}
      for key in old_data:
        # updated_data[key] = self.getTranslatedData(old_data[key], currentLanguage, translationLanguage)
        updated_data[key] = self.requestsData(old_data[key], currentLanguage, translationLanguage)
        
    return json.dumps(updated_data, indent=4)

  def getTranslatedData(self, oldDataValue, currentLanguage, translationLanguage):
    conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
    #payload = "q=Hello%2C%20world!&target=es&source=en"
    payload = "q=" + oldDataValue.encode("utf-8") + "&target=" + translationLanguage + "&source=" +currentLanguage
    
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'Accept-Encoding': "application/gzip",
        'X-RapidAPI-Key': "d4faedeecamsha6e48bd17aecf54p1ad727jsn89f4ce00e486",
        'X-RapidAPI-Host': "google-translate1.p.rapidapi.com"
    }
    
    conn.request("POST", "/language/translate/v2", payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")

  def downloadData(self, **event_args):
    """This method is called when the downlaod button is clicked"""
    # BlobMedia("text/plain", self.outputData, [name=output])
    if(self.outputFileName.text == ""):
      self.outputFileName.text = "output"
    updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=self.outputData.text.encode(), name=self.outputFileName.text+".json")
    anvil.media.download(updatedJsonFile)

  def requestsData(self, oldDataValue, currentLanguage, translationLanguage):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
    	"q": oldDataValue,
    	"target": translationLanguage,
    	"source": currentLanguage
    }
    headers = {
    	"content-type": "application/x-www-form-urlencoded",
    	"Accept-Encoding": "application/gzip",
    	"X-RapidAPI-Key": "d4faedeecamsha6e48bd17aecf54p1ad727jsn89f4ce00e486",
    	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    
    # response = requests.post(url, data=payload, headers=headers)

    response = anvil.http.request(url=url,
                    method="POST",
                    data=payload,
                    headers= headers, json=True)
    return response.json()


