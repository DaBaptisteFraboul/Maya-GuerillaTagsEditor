# Maya-GuerillaTagsEditor

## Introduction 
This is a script I created for Autodesk Maya, its purpose is to generate GuerillaTags for GuerillaRender workflow
my purpose is to make it the most comfortable possible. Feedbacks for improvements are welcomes.
I will upgrade it on  my spare time.


## How to install ?
- Step 1 : Clone or download the repository to a desired location (e.g. <DOWNLOAD_LOCATION>) 
- Step 2 : Inside Maya, Create a new python Script in the Script Editor
- Step 3 : Use the folowing code to call the Guerilla Tag editor
```python 
import sys
import importlib
# Add the Maya Guerilla Tag editor folder (<DOWNLOAD_LOCATION>) to the Maya Python Interpreter
sys.path.append(<DOWNLOAD_LOCATION>)
# Import main module from GuerillaTagEditor.main
import main
#Launch Editor
main.execute()
```
- Last step : You may want to save the script as a shortcut on the shelf.
## How to use 

![002](https://github.com/DaBaptisteFraboul/Maya-GuerillaTagsEditor/assets/100163862/c3fab047-81a2-402e-82f1-0159e89a49db)
THe tool window that should Pop-up
![001](https://github.com/DaBaptisteFraboul/Maya-GuerillaTagsEditor/assets/100163862/2dcc2ac8-45cc-4cb1-841f-7181bc9dcf58)
You can drag and drop with middle mouse button to get the Tags directly from the outliner.

## Todo list 
    - No future features planned

