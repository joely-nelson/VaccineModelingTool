var width = window.innerWidth;
var height = window.innerHeight;

var svg = d3.select('body')
.append('svg')
.attr('width', width)
.attr('height', height);

var g = svg.append('g');

// creating the projection type
var albersProjection = d3.geoMercator()
.scale((width - 3) / (2 * Math.PI))
.translate([width / 2, height / 2]);



var geoPath = d3.geoPath()
.projection(albersProjection);

const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on('zoom', zoomed);


svg.call(zoom);

    

//linking porojection to the data
g.selectAll('path')
.data(countries_json.features)
.enter()
.append('path')
.attr('d', geoPath)
.style("fill", function(d, i) {
    var name = d.properties.ADMIN;
    return colors[name];
  })
.append("svg:title")
.text(function(d) { return d.properties.ADMIN });


function zoomed() {
    g.selectAll('path') // To prevent stroke width from scaling
    .attr('transform', d3.event.transform);
  }

console.log("fasfasd")

