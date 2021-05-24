// var width = window.innerWidth;
// var height = window.innerHeight;
var map = d3.select("svg #map");
var width = 1000;
var height = 700;
var currentCountryName = "not initialized yet";
var currentCountryCode = "";
var viewingOptions = {"Suceptible":0, "Exposed":1, "Infected":2, "Dead":3, "Recovered":4, "Vaccinated":5};
var currentViewingOption = "Suceptible" // relates to index of above array

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


var currentIndex = 0;

// creating the projection type
var albersProjection = d3.geoMercator()
.scale(250)
.center([21.03, 45.659])
// .scale((width - 3) / (2 * Math.PI))
.translate([width / 2, height / 2]);

var svg = d3.select('body').select('svg')

var geoPath = d3.geoPath()
.projection(albersProjection);


// zoom in functionality
const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on('zoom', zoomed);


svg.call(zoom);

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
      var name = d.properties.ISO_A3;
      var colorScale = ["#fff7fb", "#08306b"]
      var colorSelection = d3.scaleSequential(colorScale) // used for normal output values
      var logColorSelector = d3.scalePow().exponent(0.1).range(colorScale); // use for smaller output values
      if (simResults == undefined) {
          if (dummy_model_output[name] == undefined) {
            return "black";
          }
          return colorSelection(dummy_model_output[name][1][currentIndex][3] / 100.0);
      } else {
          if (simResults[name] == undefined) {
            return "black";
          }
          // "Exposed":1, "Infected":2, "Dead":3, "Recovered":4
          if (currentViewingOption == "Exposed" || currentViewingOption == "Dead" || currentViewingOption == "Infected" || currentViewingOption == "Recovered") {
            return logColorSelector(simResults[name][1][currentIndex][viewingOptions[currentViewingOption]] / population[d.properties.ISO_A3]);
          } 
          // console.log("name: " + d.properties.ADMIN);
          // console.log("country code:" + name);
          // console.log("result: " + simResults[name][1][currentIndex][viewingOptions[currentViewingOption]]);
          // console.log("population: " + population[d.properties.ISO_A3]);
          // console.log("");
          return colorSelection(simResults[name][1][currentIndex][viewingOptions[currentViewingOption]] / population[d.properties.ISO_A3]);
      }
    
    })
    .on("click", function(d, i) {
      currentCountryName = d.target.__data__.properties.ADMIN;
      currentCountryCode = d.target.__data__.properties.ISO_A3;
      console.log(currentCountryName);
      console.log(currentCountryCode);
      // open window??
      popupWindow = window.open(
        'popupWindow/popup.html','popUpWindow','height=454,width=300,left=0,top=200,resizable=no,scrollbars=yes,toolbar=no,menubar=no,location=no,directories=no,status=yes')
      // console.log(d.target.__data__.properties.ADMIN);
    })
  .append("svg:title")
  .text(function(d) { 

    var name = d.properties.ISO_A3;
    if (simResults == undefined) {
      if (dummy_model_output[name] == undefined) {
        return name;
      }
      

      var s =  d.properties.ADMIN + "\n\n"
      + "Population: " + population[d.properties.ISO_A3] + "\n"
      + "Suceptible: " + dummy_model_output[name][1][currentIndex][0] * 100 / population[d.properties.ISO_A3]  + "%\n"
      + "Exposed: " +  dummy_model_output[name][1][currentIndex][1] * 100 / population[d.properties.ISO_A3]  + "%\n"
      + "Infected: " +  dummy_model_output[name][1][currentIndex][2] * 100 / population[d.properties.ISO_A3]  + "%\n"
      + "Dead: " +  dummy_model_output[name][1][currentIndex][3] * 100 / population[d.properties.ISO_A3] + "%\n"
      + "Recovered: " +  dummy_model_output[name][1][currentIndex][4] * 100 / population[d.properties.ISO_A3] + "%\n"
      + "Vaccinated: " +  dummy_model_output[name][1][currentIndex][5] * 100 / population[d.properties.ISO_A3] + "%\n"
  
      return s; 
    } else {
      if (simResults[name] == undefined) {
        return d.properties.ADMIN;
      }
        var s =  d.properties.ADMIN + "\n\n"
      + "Population: " + population[d.properties.ISO_A3] + "\n"
      + "Suceptible: " + (simResults[name][1][currentIndex][0] * 100 / population[d.properties.ISO_A3]).toFixed(2)  + "%\n"
      + "Exposed: " +  Math.round(simResults[name][1][currentIndex][1])  + "\n"
      + "Infected: " + Math.round(simResults[name][1][currentIndex][2]) + "\n"
      + "Dead: " +  Math.round(simResults[name][1][currentIndex][3]) + "\n"
      + "Recovered: " + Math.round(simResults[name][1][currentIndex][4]) + "\n"
      + "Vaccinated: " +  (simResults[name][1][currentIndex][5] * 100 / population[d.properties.ISO_A3]).toFixed(2)  + "%\n"
      // console.log(s);
      return s;
    }
   });
  
}

// initial call 
update();

// Slider code
function createSlider(n) {
  console.log("creating slider with size" + n);
  var slider = d3.sliderHorizontal()
  .min(0)
  .max(n - 1) // size of the slider, may need adiditional info to adjust
  .step(1)
  .displayValue(true)
  .width(600)
  .on('onchange', (val) => {
    if (val != currentIndex) {
      currentIndex = val;
        
      map.selectAll("path").remove();
      update();
      svg.call(zoom);
    }
  });
  

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

  console.log(currentViewingOption);
  map.selectAll("path").remove();
  update();
}

createSlider(20);


