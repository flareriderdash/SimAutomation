# SimAutomation
A modular python tool that interacts with www.simcompanies.com and automates 
annoying repetitive tasks on a timer.

### Important
- Place user defined functions in the file **actions.py** and do not change the 
name of this file.

- For code reference just view the **core.py** file and familiarize yourself
with the function calls. Don't worry almost all the http and cookie handling
is done withing core.py itself and has been abstracted away from user defined
functions

- I recommend making this a linux service as this code is meant to be run as
a daemon in the back ground and periodically activating functions at 
determined times that are set in the generated **function.config** file.
Dont worry if you dont see this on the first run.

- In **function.config** you will see a automatically collected user
function list (if there are defined functions)
