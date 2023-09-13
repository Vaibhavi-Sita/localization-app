from ._anvil_designer import Form2Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json
# import codecs

# import shutil

class Form2(Form2Template):
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
          print(old_file.content_type)
          if(old_file.content_type == "application/json"):
            old_json = json.loads(old_file.get_bytes())
            new_json = json.loads(new_file.get_bytes())
  
            updated_json = self.update_json(old_json, new_json)
            updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=json.loads(updated_json).encode(), name=new_file.name)
            anvil.media.download(updatedJsonFile)
          else:
            old_properties_data = {}
            new_properties_data = {}

            #OLD FILE TO JSON
            current_section = None
            old_file = old_file.get_bytes()
            print(str(old_file, 'UTF-8'))
            # for line in str(old_file, 'UTF-8'):
            #   line = line.strip()
            #   print(line)

            # # Ignore comments and empty lines
            # if not line or line.startswith('#'):
            #     continue

            # # Check if the line defines a new section
            # if line.startswith('[') and line.endswith(']'):
            #     current_section = line[1:-1]
            #     old_properties_data[current_section] = {}
            # else:
                # key, value = line.split('=', 1)
                # key = key.strip()
                # value = value.strip()
                # old_properties_data[current_section][key] = value
            key, value = str(old_file, 'UTF-8').split('=', 1)
            key = key.strip()
            value = value.strip()
            print(key,value)
            old_properties_data[current_section][key] = value
            # print(old_properties_data)


            #NEW FILE TO JSON
            current_section = None

            for line in new_file.get_bytes():
              line = line.strip()

            # Ignore comments and empty lines
              if not line or line.startswith('#'):
                continue

            # Check if the line defines a new section
              if line.startswith('[') and line.endswith(']'):
                  current_section = line[1:-1]
                  new_properties_data[current_section] = {}
              else:
                  key, value = line.split('=', 1)
                  key = key.strip()
                  value = value.strip()
                  new_properties_data[current_section][key] = value
  
              updated_json = self.update_json(old_properties_data, new_properties_data)
              # updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=json.loads(updated_json).encode(), name=new_file.name)
  
              data = json.load(json_input)
              properties_str = ''
  
              def format_section(section_name, section_data):
                  formatted_section = f'[{section_name}]\n'
                  for key, value in section_data.items():
                      formatted_section += f'{key} = {value}\n'
                  return formatted_section
  
              for section_name, section_data in json_data.items():
                  properties_str += format_section(section_name, section_data)
              
              updatedPropertiesFile = anvil.BlobMedia(content_type="text/plain", content=properties_str.encode(), name=new_file.name)
  
              anvil.media.download(updatedPropertiesFile)
              
            # config = configparser.ConfigParser()
            # config.read(old_file)
        
            # old_data = {}
            # for section in config.sections():
            #     old_data[section] = dict(config.items(section))
            
            # config.read(new_file)
        
            # new_data = {}
            # for section in config.sections():
            #     new_data[section] = dict(config.items(section))
            # updated_json = self.update_json(old_json, new_json)
            # updatedJsonFile = anvil.BlobMedia(content_type="text/plain", content=json.loads(updated_json).encode(), name=new_file.name)

            # updatedPropertiesFile = configparser.ConfigParser()
            # for section, section_data in data.items():
            #   config[section] = section_data
            # anvil.media.download(updatedPropertiesFile)
            
            


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
