# Localize.json
Deployed App : https://localization.anvil.app/

## Usage:

![Untitled](Localize%20json%20ff8d1df5152c4308ad9e4281f1202e27/Untitled.png)

![Untitled](Localize%20json%20ff8d1df5152c4308ad9e4281f1202e27/Untitled%201.png)

### Modes:

1. File Mode
2. Live Translate

### File Mode:

- Compares old file (untranslated/partially translated) and received file (translated) from localization team
    - **Old Data (existing file)**:
      This is the existing .json in the application that needs to be localized.
      It may contain the following types of key-value pairs:
    
      1. **To be translated:** These are the key-value pairs that are currently in English, but require to be translated into another language. These keys are compared against the target's and the matching key's value (from received data) will be updated into the output. Example: Refer "title" and "para" keys from the screenshot.
      2.  **Existing values:** These are the key-value pairs that are already translated. Unless there is an updated translation received, these will remain unchanged. Example: Refer "existingLocalized" from the screenshot.
      3. **Newly Added Keys:** These key-value pairs are added to the existing file after it was sent for localization. Such data will not exist in the received files and can easily be overlooked while updating manually. With this application, this data will be taken into consideration to persist.
       
    - **Updated Data (received file):**
      This is the file received from the localization team This is compared against the existing file to update the non-localized values.
      It may contain the following types of key-value pairs:
    
      1. **Translated:** These are the key-value pairs that are translated into another language. These keys are compared against the existing file and the matching key's value (from received data) will be updated into the output. Example: Refer "title" and "para" keys from the screenshot.
      2. **Old values to be discarded:** These are the key-value pairs that were removed from the existing data after it was sent for translation. They are no longer needed. Such unnecessary data exists in the received targets and needs to be removed. The app will make sure that such data gets discarded in the output. Example: Refer "oldKeyToBeDiscarded" from the screenshot.

- Provides logs regarding the newly added and discarded keys from both files
- Results a clean and latest output that can be downloaded

### Live Translate:

- Enter an untranslated .json file
- Provide source and target language codes
- Results a completely translate .json file that can be downloaded

###

