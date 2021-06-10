# VaccineModelingTool
Tool made for CSE 482: CSE 482B, Capstone Software Design to Empower Underserved Populations, that enables researchers to better understand how COVID-19 vaccination efficacy and distribution impacts the spread of the virus.

### How to run
1. Visit the VaccineModelingTool folder, in your terminal run the command "python centralServer.py"
2. on your web browser of choice visit the site: http://localhost:8000/frontend_merged/main.html
3. Interact with the tool and have fun :)

### Configuring the Model and Frontend
If you want to add a new model or configure which parameters the user can tune, complete the following steps
1. In centralServery.py, call your (custom) simulation function on line 29
2. Edit /configuration_file/global_sliders.json to include all of the inputs you want to be able to tune on the frontend
3. Edit /configuration_file/global_defaults.json to assign default values for parameter tuning and modeling. NOTE: There must be one entry in global_defaults.json for each corresponding entry in global_sliders.json AND there must be one entry for any parameter your model needs that the data aggregator does not provide. 
