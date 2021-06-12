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

### Making your own Model
If you want to create your own model to use with the visulization, then modify the ``simulate_world`` function  in ``models/models.py``, to suit your needs.
* ``simulate_world`` must take in two parameters: a python dictionary that will look identical to the master json (located at ``json_io_files/master-json.json``, and an integer representing the total number of days to simulate.
* ``simulate_world`` must return a dictionary where keys are the country codes, and the values are a pair of vectors. The first item in the pair is the time vector called ``t``, and the second item in the pair is a vector called ``v``.  ``v[i][j]`` corresponds to the number of individuals in category ``j`` on the date ``t[i]``. ``j = 0`` for susceptible, ``j = 1`` for exposed, ``j = 2`` for infected, ``j = 3`` for dead, ``j = 4`` for recovered, ``j = 5`` for vaccinated.