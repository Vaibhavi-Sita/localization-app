# Localize.json
Deployed App : https://localization.anvil.app/

## Usage:

![image](https://github.com/Vaibhavi-Sita/localization-app/assets/52885102/e38d367a-048e-4e95-94ce-c08c0ce668c9)

### Old Data (existing file) 
This is the existing .json in the application that needs to be localized
It may contain the following types of key-value pairs:
1. **To be translated:** These are the key-value pairs that are currently in English, but require to be translated into another language. These keys are compared against the target's and the matching key's value (from received data) will be updated into the output. Example: Refer "title" and "para" keys from the screenshot.
2. **Existing values:** These are the key-value pairs that are already translated. Unless there is an updated translation received, these will remain unchanged. Example: Refer "existingLocalized" from the screenshot.
3. **Newly Added Keys:** These key-value pairs are added to the existing file after it was sent for localization. Such data will not exist in the received files and can easily be overlooked while updating manually. With this application, this data will be taken into consideration to persist.  


### Updated Data (received file):

This is the file received from the localization team
This is compared against the existing file to update the non-localized values
It may contain the following types of key-value pairs:
1. **Translated:** These are the key-value pairs that are translated into another language. These keys are compared against the existing file and the matching key's value (from received data) will be updated into the output. Example: Refer "title" and "para" keys from the screenshot.
2. **Old values to be discarded:** These are the key-value pairs that were removed from the existing data after it was sent for translation. They are no longer needed. Such unnecessary data exists in the received targets and needs to be removed. The app will make sure that such data gets discarded in the output. Example: Refer "oldKeyToBeDiscarded" from the screenshot.


