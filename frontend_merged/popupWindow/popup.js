window.onload = function() {
    console.log("this from child window" + window.opener.currentCountryName);
    document.getElementById('countryname').innerHTML = window.opener.currentCountryName;
    var ctx = document.getElementById('myChart');
    var currentCountryCode = window.opener.currentCountryCode
    var simResults = window.opener.simResults;
    
    
    
    
    
    // graphing
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
}

