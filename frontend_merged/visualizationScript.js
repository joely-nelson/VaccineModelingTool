// var width = window.innerWidth;
// var height = window.innerHeight;
var map = d3.select("svg #map");
var width = 1000;
var height = 700;

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
.scale((width - 3) / (2 * Math.PI))
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
      var name = d.properties.ADMIN;
      return colors[currentIndex][name];
    })
    .on("click", function(d, i) {
      console.log(d);
      console.log(d.target.__data__.properties.ADMIN);
    })
  .append("svg:title")
  .text(function(d) { 
    // console.log(d.properties.ADMIN)
    var name = d.properties.ADMIN 
    if (dummy_model_output[name] == undefined) {
      return name;
    }
    console.log(population);
    console.log(population[d.properties.ISO_A3]);
    var s =  name + "\n\n"
    + "Population: " + population[d.properties.ISO_A3] + "\n"
    + "Suceptible: " + dummy_model_output[name][1][currentIndex][0] * 100 / 100.0  + "%\n"
    + "Exposed: " +  dummy_model_output[name][1][currentIndex][1] * 100 / 100.0  + "%\n"
    + "Infected: " +  dummy_model_output[name][1][currentIndex][2] * 100 / 100.0  + "%\n"
    + "Dead: " +  dummy_model_output[name][1][currentIndex][3] * 100 / 100.0 + "%\n"
    + "Recovered: " +  dummy_model_output[name][1][currentIndex][4] * 100 / 100.0 + "%\n"
    + "Vaccinated: " +  dummy_model_output[name][1][currentIndex][5] * 100 / 100.0 + "%\n"
    return s;
   })
  ;
  
}

// initial call 
update();





//~~~~~~~slider code~~~~~~~~~~~~
var slider = d3.sliderHorizontal()
.min(0)
.max(20) // size of the slider, may need adiditional info to adjust
.step(1)
.displayValue(true)
.width(600)
.on('onchange', (val) => {
  if (val != currentIndex) {
    currentIndex = val;
    map.selectAll("path")
    .style("fill", function(d, i) {
      var name = d.properties.ADMIN;

      var colorSelection = d3.scaleSequential(["#acb3bf", "blue"])
      if (dummy_model_output[name] == undefined) {
        return "black";
      }
      // console.log(name);
      // console.log(dummy_model_output[name]);
      // console.log(dummy_model_output[name][1]);
      return colorSelection(dummy_model_output[name][1][currentIndex][3] / 100.0);
    });
    update();
  }
  // d3.select('#value').text(val);
  // console.log(val)
});

d3.select("#slider")
  .append("svg")
  .attr('width', 600)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)')
  .call(slider);
