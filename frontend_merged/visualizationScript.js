// var width = window.innerWidth;
// var height = window.innerHeight;
var map = d3.select("svg #map");
var width = 1000; // width of map
var height = 700; // height of map
var currentCountryName = "not initialized yet"; // holds value of clicked country name
var currentCountryCode = ""; // holds value of clicked country code
var viewingOptions = {"Suceptible":0, "Exposed":1, "Infected":2, "Dead":3, "Recovered":4, "Vaccinated":5};
var viewingOptionsArray = ["Suceptible", "Exposed", "Infected", "Dead", "Recovered", "Vaccinated"]
var currentViewingOption = "Suceptible" // relates to index of above array
var currentViewingOptionIndex = 0;
var currentTimeIndex = 0; // represent current time step slider is on

// reads in population data from file.
var population = (function () {
  var json = null;
  $.ajax({
      'async': false,
      'global': false,
      'url': "./data/population-figures-by-country-json.json",
      'dataType': "json",
      'success': function (data) {
          json = data;
      }
  });
  return json;
})();




// creating the projection type
var albersProjection = d3.geoMercator()
.scale(400)
.center([-60, 45.659])
// .scale((width - 3) / (2 * Math.PI))
.translate([width / 2, height / 2]);

var svg = d3.select('body').select('svg')

var geoPath = d3.geoPath()
.projection(albersProjection);


// zoom in functionality
const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on('zoom', zoomed);




function zoomed(event, d) {
    map.selectAll('path') // To prevent stroke width from scaling
    .attr('transform', event.transform);
}

    

  

// ~~~~~~~~update map~~~~~~~~~~~~~
function update() {
  //linking projection to the data
  map.selectAll('path')
  .data(countries_json.features)
  .enter()
  .append('path')
  .attr('d', geoPath)
  .style("fill", function(d, i) {
      var countryCode = d.properties.ISO_A3;
      var colorScale = ["#fff7fb", "#08306b"]
      var colorSelection = d3.scaleSequential(colorScale) // used for normal output values
      var logColorSelector = d3.scalePow().exponent(0.1).range(colorScale); // use for smaller output values
      if (simResults == undefined) {
        if (dummy_model_output[countryCode] == undefined) {
          return "black";
        }
        return colorSelection(dummy_model_output[countryCode][1][currentTimeIndex][3] / 100.0);
      } else if (simResults[countryCode] == undefined) {
        return "black";
      } else if (currentViewingOption == "Exposed" || currentViewingOption == "Dead" || currentViewingOption == "Infected" || currentViewingOption == "Recovered") {
        return logColorSelector(simResults[countryCode][1][currentTimeIndex][viewingOptions[currentViewingOption]] / population[countryCode]);
      } else {
        return colorSelection(simResults[countryCode][1][currentTimeIndex][viewingOptions[currentViewingOption]] / population[countryCode]);
      }
    })
    .on("click", function(d, i) { // handles on click functionality
      currentCountryName = d.target.__data__.properties.ADMIN;
      currentCountryCode = d.target.__data__.properties.ISO_A3;
      // open window??
      popupWindow = window.open(
        'popupWindow/popup.html','popUpWindow','height=700,width=500,left=0,top=200,resizable=no,scrollbars=yes,toolbar=no,menubar=no,location=no,directories=no,status=yes')
    })
  .append("svg:title")
  .text(function(d) { // handles the hover functionality

    var countryCode = d.properties.ISO_A3;
    var countryName = d.properties.ADMIN;
    if (simResults == undefined) {
      if (dummy_model_output[countryCode] == undefined) {
        return countryCode;
      }
      var s =  countryName + "\n\n"
      + "Population: " + population[d.properties.ISO_A3] + "\n"
      + "Suceptible: " + dummy_model_output[countryCode][1][currentTimeIndex][0] * 100 / population[d.properties.ISO_A3]  + "%\n"
      + "Exposed: " +  dummy_model_output[countryCode][1][currentTimeIndex][1] * 100 / population[d.properties.ISO_A3]  + "%\n"
      + "Infected: " +  dummy_model_output[countryCode][1][currentTimeIndex][2] * 100 / population[d.properties.ISO_A3]  + "%\n"
      + "Dead: " +  dummy_model_output[countryCode][1][currentTimeIndex][3] * 100 / population[d.properties.ISO_A3] + "%\n"
      + "Recovered: " +  dummy_model_output[countryCode][1][currentTimeIndex][4] * 100 / population[d.properties.ISO_A3] + "%\n"
      + "Vaccinated: " +  dummy_model_output[countryCode][1][currentTimeIndex][5] * 100 / population[d.properties.ISO_A3] + "%\n";

      return s; 
    } else {
      if (simResults[countryCode] == undefined) {
        return countryName;
      }
      var s =  countryName + "\n\n"
      + "Population: " + population[d.properties.ISO_A3] + "\n"
      + "Suceptible: " + (simResults[countryCode][1][currentTimeIndex][0] * 100 / population[d.properties.ISO_A3]).toFixed(2)  + "%\n"
      + "Exposed: " +  Math.round(simResults[countryCode][1][currentTimeIndex][1])  + "\n"
      + "Infected: " + Math.round(simResults[countryCode][1][currentTimeIndex][2]) + "\n"
      + "Dead: " +  Math.round(simResults[countryCode][1][currentTimeIndex][3]) + "\n"
      + "Recovered: " + Math.round(simResults[countryCode][1][currentTimeIndex][4]) + "\n"
      + "Vaccinated: " +  (simResults[countryCode][1][currentTimeIndex][5] * 100 / population[d.properties.ISO_A3]).toFixed(2)  + "%\n";

      return s;
    }
   });
  
}



// Slider code
function createSlider(n) {
  var slider = d3.sliderHorizontal()
  .min(0)
  .max(n - 1) // size of the slider, may need adiditional info to adjust
  .step(1)
  .displayValue(true)
  .width(600)
  .on('onchange', (val) => {
    if (val != currentTimeIndex) {
      currentTimeIndex = val;
        
      map.selectAll("path").remove();
      update();
      svg.call(zoom);
    }
  })
  .value(0);
  
  currentTimeIndex = 0;
  d3.select("#slider").select("svg").remove();



  d3.select("#slider")
  .append("svg")
  .attr('width', 600)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)')
  .call(slider);

  map.selectAll("path").remove();
  update();
}

function changeDataView() {
  var dropdownMenu = document.getElementById("dataView");
  currentViewingOption = dropdownMenu.options[dropdownMenu.selectedIndex].text;

  map.selectAll("path").remove();
  update();
}

function fullResetMap(timeLength) {
  update();
  createSlider(timeLength);
}

svg.call(zoom);

// initial call 
update();

// createSlider(20);


