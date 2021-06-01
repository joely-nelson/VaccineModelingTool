import models as md
import json

with open ('C:/Users/Tevin/Dropbox/All_Classes/CSE_Classes/Capstone/VaccineModelingTool/json_io_files/master-json.json') as file:
    defaults = json.load(file)
    output = md.simulate_world(defaults, 365)
    print(defaults)
    print()
    print(output)

    with open("C:/Users/Tevin/Dropbox/All_Classes/CSE_Classes/Capstone/VaccineModelingTool/json_io_files/default_output.json", "w") as write_file:
        json.dump(output, write_file)
        