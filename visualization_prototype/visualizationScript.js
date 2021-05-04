// var width = window.innerWidth;
// var height = window.innerHeight;
var map = d3.select("svg #map");
var width = 1500;
var height = 1000;

var currentIndex = 0;

// put in 'svg' element in body of html
// var svg = d3.select('body')
// .append('svg')
// .attr('width', width)
// .attr('height', height);

// var g = svg.append('g');

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
    


// update map
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
  .append("svg:title")
  .text(function(d) { return d.properties.ADMIN });
}

update();







// slider code
var slider = d3.sliderHorizontal()
.min(0)
.max( colors.length - 1)
.step(1)
.displayValue(true)
.width(600)
.on('onchange', (val) => {
  if (val != currentIndex) {
    currentIndex = val;
    map.selectAll("path").remove();
    update();
  }
  zoomed();
  d3.select('#value').text(val);
  console.log(val)
});

d3.select("#slider")
  .append("svg")
  .attr('width', 600)
  .attr('height', 100)
  .append('g')
  .attr('transform', 'translate(30,30)')
  .call(slider);

// d3.select("#slider") // (1)
//     .call(
//       chroniton()  // (2)
//         .domain([new Date(startYear, 1, 1), new Date(startYear + (colors.length - 1) * 10, 1, 1)])  // (3)
//         .labelFormat(function(date) {
//           return Math.ceil((date.getFullYear()) / 10) * 10;  // (4)
//         })
//         .width(600)  // (5)
//     );