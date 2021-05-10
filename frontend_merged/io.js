var default_params;
var in1;
var in2;
var in3;

// get default parameters
d3.json("http://localhost:8000/json_io_files/default_params.json").then(function(data){
    default_params = data;
    in1 = default_params.in1;
    in2 = default_params.in2;
    in3 = default_params.in3;
    
    // Initial value for inputs
    in1Update(in1);
    in2Update(in2);
    in3Update(in3);
});

// Bind user input to function
d3.select("#input1").on("input", function() {
  in1Update(+this.value);
});

d3.select("#input2").on("input", function() {
    in2Update(+this.value);
});

d3.select("#input3").on("input", function() {
    in3Update(+this.value);
});

d3.select('#simulate').on("click", function() {
    simulate();
});

// update input1 val
function in1Update(input1) {
    in1 = input1;
    d3.select("#input1").property("value", in1);
    console.log(in1);  // for debugging
}

// update input2 val
function in2Update(input2) {
    in2 = input2;
    d3.select("#input2").property("value", in2);
    console.log(in2);  // for debugging
}

// update input3 val
function in3Update(input3) {
    in3 = input3;
    // adjust the text on the range slider
    d3.select("#input3-value").text(in3);
    d3.select("#input3").property("value", in3);
    console.log(in3);
}

// trigger model simulation
function simulate() {
    console.log("Click");
    var url = "http://localhost:8000/?input1="+in1+"&input2="+in2+"input3="+in3;
    d3.json(url)
     .then(function(data) {
    console.log(data);
    }); 
}