// variables to manage radio inputs and input mappings
var radioIsCustom = new Array();
var inputNumMapping = new Array();

// variables to store params and corresponding model output
var defaultParams;
var defaultSimOutput;

var customParams;
var customSimOutput;

var numDaysSim;

// Dynamically Load Global Parameter Pane
document.addEventListener("DOMContentLoaded", function(event) {     
   
    // initialize default and custom data structures
    d3.json("http://localhost:8000/default_params.json").then(function(data){
        defaultParams = data;
        customParams = JSON.parse(JSON.stringify(defaultParams)); // deep copy
    });

    /*
    d3.json("http://localhost:8000/json_io_files/default_output.json").then(function(data)) {
        defaultSimOutput = data;
    });
    */

    // dynamically load vaccine drop down
    d3.json("http://localhost:8000/vaccines.json").then(function(options) {
        for (i in options["vaccines"]) {
            document.getElementById("input_0").insertAdjacentHTML('beforeend', 
            '<option value="' + options["vaccines"][i] + '">' + options["vaccines"][i] + '</option>');
        }
    });

    d3.json("http://localhost:8000/global_sliders.json").then(function(options) {
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
            ' type=' + options[param]["type"] + 
            ' min=' + options[param]["min"] + 
            ' max=' + options[param]["max"] + 
            ' step=' + options[param]["step"] + 
            ' value=' + options[param]["default"] + 
            ' id="input_' + i + '"val><br>' +
            '</form>');
            
            // initialize mappings
            inputNumMapping[i] = options[param]["mapping"];
            radioIsCustom[i] = 0;
            i++;
        }

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
    console.log(inputElementID);
    customVal = document.getElementById(inputElementID).value;
    for (iso in customParams) {
        customParams[iso][fieldName] = customVal;
    }
}

// country update function
    // map input number to param name
    // update param name to custom for given country

// simulate onClick logic
d3.select('#simulate').on("click", function() {
    simulate();
});

// trigger model simulation
function simulate() {
    console.log("Click");
    d3.json("http://localhost:8000/?simulate=true", function(data) {
    console.log(data);
    simResults = data;
    // NOTE: hard coded for now
    createSlider(100);
    update();
    }); 
}

// Reset onClick Logic
// TODO




// // trigger model simulation
// function simulate() {
//     console.log("Click");
//     var url = "http://localhost:8000/?alpha="+in1+
// 				     "&beta="+in2+
//                                      "&eps="+in3+
// 				     "&gamma="+in4+
//                                      "&vac_start_day="+in5+
// 				     "&uptake_per="+in6+
//                                      "&num_vac_days="+in7+
//                                      "&vac_rate="+in8;

//     d3.json(url)
//      .then(function(data) {
//     console.log(data);
//     simResults = data;
    
//     }); 
    
// }