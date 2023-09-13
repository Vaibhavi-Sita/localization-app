from ._anvil_designer import PropertiesUploadTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json
# import shutil

class PropertiesUpload(PropertiesUploadTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def getFiles(self, **event_args):
    # self.process_directory(self.oldFiles, self.newFiles, self.outputFiles)
    self.process_directory(self.oldFilesUpload, self.newFilesUpload)
    pass

  def process_directory(self, oldFilesUpload, newFilesUpload):
    # os.makedirs(output_dir, exist_ok=True)

    # List all files in the old and new directory

    # for old_file, new_file in oldFilesUpload.files, newFilesUpload.files:
    for old_file in oldFilesUpload.files:
      for new_file in newFilesUpload.files:
        # Check if the file exists in the new directory
        if old_file.name == new_file.name:
          # old_json = json.load(old_file)
          # new_json = json.load(new_file)
          old_json = json.loads(old_file.get_bytes())
          new_json = json.loads(new_file.get_bytes())


          updated_json = self.update_json(old_json, new_json)
          # self.outputArea.text += json.dumps(updated_json)
          # self.outputArea.text = json.loads(updated_json)

          updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=json.loads(updated_json).encode(), name=new_file.name)
          anvil.media.download(updatedJsonFile)


  def update_json(self, old_data, new_data):

    old_data = json.dumps(old_data)
    new_data = json.dumps(new_data)
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
    elif isinstance(old_data, list) and isinstance(new_data, list):
      updated_data = []
      for i in range(min(len(old_data), len(new_data))):
        updated_data.append(update_json_values(old_data[i], new_data[i]))
      if len(new_data) > len(old_data):
        updated_data.extend(new_data[len(old_data):])
      return updated_data
    else:
      return new_data

  def goToForm1(self, **event_args):
    open_form('Form1')
