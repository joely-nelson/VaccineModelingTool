var currentCountryCode;

// Initializes popup window
// Creates input slider for each parameter in config file
// populates with current values (from default or custom global)
// display plots for simulation output
window.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById('countryname').innerHTML = window.opener.currentCountryName;
    var ctx = document.getElementById('myChart');
    var simResults = window.opener.simResults;
    currentCountryCode = window.opener.currentCountryCode;
    
    // load sliders from configuration file
    loadParams(currentCountryCode);

    // bind event listener to apply button
    d3.select('#apply').on("click", function() {
        console.log("Click on apply");
        applyEventListener();
    });

    // load graph
    if (simResults != undefined) {
        console.log(window.opener.simResults);
        console.log("pop up");
        var xaxis = [];
        var succeptible = [] // 0
        var exposed = []; // 1
        var infected = []; // 2
        var dead = []; // 3
        var recovered = []; // 4
        var vaccinated = []; // 5
        for (i = 0; i < simResults[currentCountryCode][1].length; i++) {
            xaxis.push(i);
            succeptible.push(simResults[currentCountryCode][1][i][0]);
            exposed.push(simResults[currentCountryCode][1][i][1]);
            infected.push(simResults[currentCountryCode][1][i][2]);
            dead.push(simResults[currentCountryCode][1][i][3]);
            recovered.push(simResults[currentCountryCode][1][i][4]);
            vaccinated.push(simResults[currentCountryCode][1][i][5]);
        }
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: xaxis,
                datasets: [{
                    label: "Succeptible",
                    data: succeptible,
                    borderColor: '#7fc97f',
                    tension: 0.1
                }, {
                    label: "Exposed",
                    data: exposed,
                    borderColor: '#beaed4',
                    tension: 0.1
                }, {
                    label: "Infected",
                    data: infected,
                    borderColor: '#fdc086',
                    tension: 0.1
                }, {
                    label: "Dead",
                    data: dead,
                    borderColor: '#ffff99',
                    tension: 0.1
                }, {
                    label: "Recovered",
                    data: recovered,
                    borderColor: '#386cb0',
                    tension: 0.1
                }, {
                    label: "Vaccinated",
                    data: vaccinated,
                    borderColor: '#f0027f',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y:  {
                        title: {
                        display: true,
                        text: '# of People'
                        }
                    },
                    x:  {
                        title: {
                        display: true,
                        text: 'Time'
                        }
                    }
                }
            }
        });
    }
});

// function for loading sliders in config file
function loadParams(countryCode) {
    console.log("Loading Params");
    var customParams = window.opener.customParams;
    var sliders = window.opener.sliders;

    // iterate over each slider and display current value
    var i = 1;
    for (param in sliders) {
        document.getElementById("countryParams").insertAdjacentHTML('beforeend',
        '<label for=country_input_' + i + '>' + param +': </label>' +
        '<input class="custom"' +
        ' type=' + sliders[param]["type"] + 
        ' min=' + sliders[param]["min"] + 
        ' max=' + sliders[param]["max"] + 
        ' step=' + sliders[param]["step"] + 
        ' value=' + customParams[countryCode][sliders[param]["mapping"]] + 
        ' id="country_input_' + i + '"><br>');
        i++;
    }
}



// event listener for "apply"
function applyEventListener() {
    var newParams = new Array();
    var numParams = window.opener.numParams;
    for (var i = 1; i < numParams; i++) {
        inputElementID = "country_input_" + i;
        newParams[i] = document.getElementById(inputElementID).value;
    }
    window.opener.countryUpdate(currentCountryCode, newParams);
}
