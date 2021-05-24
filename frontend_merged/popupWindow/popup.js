window.onload = function() {
    console.log("this from child window" + window.opener.currentCountryName);
    document.getElementById('countryname').innerHTML = window.opener.currentCountryName;
    var ctx = document.getElementById('myChart');
    var currentCountryCode = window.opener.currentCountryCode
    var simResults = window.opener.simResults;'
    if (simResults != undefined) {
        console.log(window.opener.simResults);
        console.log("pop up");
        var xaxis = [];
        var datasets = [];
        for (i = 0; i < simResults[currentCountryCode][1].length; i++) {
            xaxis.push(i);
            datasets.push(simResults[currentCountryCode][1][i][window.opener.viewingOptions[window.opener.currentViewingOption]]);
        }
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: xaxis,
                datasets: [{
                    label: window.opener.currentViewingOption,
                    data: datasets,
                    // backgroundColor: [
                    //     'rgba(255, 99, 132, 0.2)',
                    //     'rgba(54, 162, 235, 0.2)',
                    //     'rgba(255, 206, 86, 0.2)',
                    //     'rgba(75, 192, 192, 0.2)',
                    //     'rgba(153, 102, 255, 0.2)',
                    //     'rgba(255, 159, 64, 0.2)'
                    // ],
                    borderColor: '#74a9cf',
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

