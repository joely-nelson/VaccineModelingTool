// variables to manage radio inputs and input mappings
var radioIsCustom = new Array();
var inputNumMapping = new Array();

// maps storing configuration values and metadata
var globalDefaults;
var sliders;
var numParams;

// variables to store model params and corresponding model output
var defaultParams;
var customParams;
var defaultSimOutput;

// used by the map to display output
// points to either defaultSimOutput of output generated with custom params
var simResults;  

// Param for number to conduct simulation over
var numDaysSim = 365;

// initialize default and custom data structures
d3.json("http://localhost:8000/json_io_files/master-json.json").then(function(data) {
    defaultParams = data;
    customParams = JSON.parse(JSON.stringify(defaultParams)); // deep copy
});

// Load default simulation output
d3.json("http://localhost:8000/json_io_files/default_output.json").then(function(data) {
    defaultSimOutput = data;
    simResults = JSON.parse(JSON.stringify(defaultSimOutput));
    createSlider(numDaysSim);
    update();

});

// Dynamically Load Global Parameter Pane
document.addEventListener("DOMContentLoaded", function(event) {     
    // dynamically load vaccine drop down
    d3.json("http://localhost:8000/json_io_files/vaccines.json").then(function(options) {
        for (i in options["vaccines"]) {
            document.getElementById("input_0").insertAdjacentHTML('beforeend', 
            '<option value="' + options["vaccines"][i] + '">' + options["vaccines"][i] + '</option>');
        }
    });

    // load global defaults
    d3.json("http://localhost:8000/configuration_files/global_defaults.json").then(function(defaults) {
        globalDefaults = defaults;
    });

    // dynamically add all user inputs specified in the config file
    d3.json("http://localhost:8000/configuration_files/global_sliders.json").then(function(options) {
        sliders = options;
        var i = 1;
        radioIsCustom[0] = 0;
        inputNumMapping[0] = "vaccine_type";
        for (param in options) {
            document.getElementById("globalParams").insertAdjacentHTML('beforeend',
            '<p>' + param + ':</p>' +
            '<form>' + 
            '<input class="radio" type="radio" id="default_radio_' + i + '" name="radio' + i + '" checked>' +
            '<label for=default_radio_' + i + '>Default</label><br>' +
            '<input class="radio " type="radio" id="custom_radio_' + i + '" name="radio' + i + '">' +
            '<label for=custom_radio_' + i + '>Custom Global: </label>' +
            '<input class="custom"' +
            ' type=' + sliders[param]["type"] + 
            ' min=' + sliders[param]["min"] + 
            ' max=' + sliders[param]["max"] + 
            ' step=' + sliders[param]["step"] + 
            ' placeholder=' + globalDefaults[sliders[param]["mapping"]] + // TODO: retrieve from global default not options
            ' id="input_' + i + '"><br>' +
            '</form>');
            
            // initialize mappings
            inputNumMapping[i] = sliders[param]["mapping"];
            radioIsCustom[i] = 0;
            i++;
        }

        numParams = i;

        // attatch event listeners to all radio elements
        d3.selectAll(".radio")
            .on("click", function(){
                var id = d3.select(this).attr("id");
                var idFields = id.split("_");
                var inputType = idFields[0];
                var num = Number(idFields[2]);
                if (inputType == "default") {
                    defaultRadioOnClick(num);
                } else {
                    customRadioOnClick(num);
                }
            });

        // attatch event listener to all custom inputs
        d3.selectAll(".custom")
            .on("input", function() {
                var id = d3.select(this).attr("id");
                var idFields = id.split("_");
                var num = Number(idFields[1]);
                customInputOnChange(num);
            });
    });
    
});

// updates the field corresponding to num in the custom master
// json to be the defualt value for that country
function defaultRadioOnClick(num) {
    radioIsCustom[num] = 0;
    fieldName = inputNumMapping[num];
    for (iso in defaultParams) {
        customParams[iso][fieldName] = defaultParams[iso][fieldName];
    }
}

// updates the field corresponding to num in the custom master
// json to be the custom input value for all countries
function customRadioOnClick(fieldNum) {
    radioIsCustom[fieldNum] = 1;
    globalUpdate(fieldNum);
}

function customInputOnChange(fieldNum) {
    if (radioIsCustom[fieldNum] == 1) {
        globalUpdate(fieldNum);
    }
}
  
function globalUpdate(fieldNum) {
    fieldName = inputNumMapping[fieldNum];
    inputElementID = "input_" + fieldNum;
    customVal = document.getElementById(inputElementID).value;
    if (customVal == "") {
        customVal = globalDefaults[fieldName];
    }
    for (iso in customParams) {
        customParams[iso][fieldName] = customVal;
    }
}

function countryUpdate(countryCode, params) {
    for (var i = 1; i < numParams; i++) {
        fieldName = inputNumMapping[i];
        customParams[countryCode][fieldName] = params[i];
    }
    console.log(customParams);
}


// bind event listener to sim days
d3.select('#sim_days_input').on("click", function(){
    simDaysUpdate(+this.value);
});

// bind event listener to simulate
d3.select('#simulate').on("click", function() {
    simulate();
});

// bind event listener to reset
d3.select('#reset').on("click", function() {
    reset();
});

function simDaysUpdate(input) {
    numDaysSim = (input == "") ? 365 : input;
}

// trigger model simulation
function simulate() {
    var url = "http://localhost:8000/?numDays=" + numDaysSim;
    d3.json(url, {
        method:"POST",
        body: JSON.stringify(customParams),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
        .then(function(data) {
            simResults = data;
            fullResetMap(numDaysSim);
        });
}

function reset() {
    simResults = defaultSimOutput;

    // reset numDays Input
    numDaysSim = 365;
    document.getElementById("sim_days_input").value = "";

    // change all radio buttons to default checked
    for (var i=0; i < numParams; i++) {
        // reset radio
        var id = "default_radio_" + i;
        document.getElementById(id).checked = "checked";

        // reset input
        id = "input_" + i;
        document.getElementById(id).value = "";

        // reset isRadioCustom
        radioIsCustom[i] = 0;
    }

    // reset customGlobalParams to default
    customParams = JSON.parse(JSON.stringify(defaultParams)); // deep copy

    // TODO: render map
    fullResetMap(numDaysSim);
    
}