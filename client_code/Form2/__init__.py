from ._anvil_designer import Form2Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json
import shutil

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
   
  def getFiles(self):
    # self.process_directory(self.oldFiles, self.newFiles, self.outputFiles)
    self.process_directory(self.oldFilesUpload, self.newFilesUpload, self.output_dir)
    pass

  def process_directory(self, oldFilesUpload, newFilesUpload, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # List all files in the old and new directory

    for old_file, new_file in oldFilesUpload.files, newFileUpload.files:
        # Check if the file exists in the new directory
        if old_file.name == new_file.name:
          old_json = json.load(old_file)
          new_json = json.load(new_file)
          
          updated_json = update_json(old_json, new_json)

    return json.dump(updated_json, output_file, indent=4)

          # Write the updated JSON to the output directory
          # output_file_path = os.path.join(output_dir, old_file_name)
          # with open(output_file_path, 'w') as output_file:
          #     json.dump(updated_json, output_file, indent=4)

  def create_zip(self, output_dir, zip_filename):
    shutil.make_archive(zip_filename, 'zip', output_dir)
    self.downloadZip()
    
  def downloadZip(self, **event_args):
    """This method is called when the downlaod button is clicked"""
    # BlobMedia("text/plain", self.outputData, [name=output])
    # if(self.outputFileName.text == ""):
    #   self.outputFileName.text = "output"
    outputFiles = anvil.BlobMedia(content_type="application/zip", content=self.output_dir, name="Output Files")
    anvil.media.download(outputFiles)  
  
  def getData(self, **event_args):
    """This method is called when the submit button is clicked"""
    self.logs.text = ""
    self.outputData.text = self.update_json(self.oldData, self.newData)
    # self.outputData.text = (self.old_dir, self.new_dir)
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
          self.logs.text += "DISCARDED: " + "\n" + key + ": " + new_data[key] + "\n" + "\n"
      #         updated_data[key] = new_data[key]
      # Newly Added keys
      for key in old_data:
        if key not in new_data:
          self.logs.text += "NEWLY ADDED: " + "\n" + key + ": " + old_data[key] + "\n" + "\n"
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

 
    
  # def process_directory(self, old_files, new_files, output_files):
  #   # os.makedirs(output_dir, exist_ok=True)
    
  #   # List all files in the old directory
  #   # old_files = os.listdir(old_dir)
    
  #   for old_file_name in old_files:
  #       if old_file_name in new_files:
  #         for new_file_name in new_files:
  #           if old_file_name == new_file_name:
  #             old_json = json.load(old_file_name)
  #             new_json = json.load(new_file_name)
                
  #             updated_json = update_json_values(old_json, new_json)
              
  #             # Write the updated JSON to the output directory
  #             output_file_path = os.path.join(output_dir, old_file_name)
  #             with open(output_file_path, 'w') as output_file:
  #                 json.dump(updated_json, output_file, indent=4)
