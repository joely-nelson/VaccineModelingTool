// alpha, beta, gamma, eps, vac_start_day, uptake_per, num_vac_days, vac_rate

var default_params;
var in1; // alpha
var in2; // beta
var in3; // epsilon
var in4; // gamma
var in5; // vac_start_day
var in6; // uptake_per
var in7; // num_vac_days
var in8; // vac_rate
var simResults;


// get default parameters
d3.json("http://localhost:8000/json_io_files/default_params.json").then(function(data){
    default_params = data;
    in1 = default_params.in1;
    in2 = default_params.in2;
    in3 = default_params.in3;
    in4 = default_params.in4;
    in5 = default_params.in5;
    in6 = default_params.in6;
    in7 = default_params.in7;
    in8 = default_params.in8;

    
    // Initial value for inputs
    in1Update(in1);
    in2Update(in2);
    in3Update(in3);
    in4Update(in4);
    in5Update(in5);
    in6Update(in6);
    in7Update(in7);
    in8Update(in8);
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

d3.select("#input4").on("input", function() {
    in4Update(+this.value);
});

d3.select("#input5").on("input", function() {
    in5Update(+this.value);
});

d3.select("#input6").on("input", function() {
    in6Update(+this.value);
});

d3.select("#input7").on("input", function() {
    in7Update(+this.value);
});

d3.select("#input8").on("input", function() {
    in8Update(+this.value);
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

// update input4 val
function in4Update(input4) {
    in4 = input4;
    // adjust the text on the range slider
    d3.select("#input4-value").text(in4);
    d3.select("#input4").property("value", in4);
    console.log(in4);
}

// update input5 val
function in5Update(input5) {
    in5 = input5;
    // adjust the text on the range slider
    d3.select("#input5-value").text(in5);
    d3.select("#input5").property("value", in5);
    console.log(in5);
}

// update input6 val
function in6Update(input6) {
    in6 = input6;
    // adjust the text on the range slider
    d3.select("#input6-value").text(in6);
    d3.select("#input6").property("value", in6);
    console.log(in6);
}

// update input7 val
function in7Update(input7) {
    in7 = input7;
    // adjust the text on the range slider
    d3.select("#input7-value").text(in7);
    d3.select("#input7").property("value", in7);
    console.log(in7);
}

// update input8 val
function in8Update(input8) {
    in8 = input8;
    // adjust the text on the range slider
    d3.select("#input8-value").text(in8);
    d3.select("#input8").property("value", in8);
    console.log(in8);
}



// trigger model simulation
function simulate() {
    console.log("Click");
    var url = "http://localhost:8000/?alpha="+in1+
				     "&beta="+in2+
                                     "&eps="+in3+
				     "&gamma="+in4+
                                     "&vac_start_day="+in5+
				     "&uptake_per="+in6+
                                     "&num_vac_days="+in7+
                                     "&vac_rate="+in8;

    d3.json(url)
     .then(function(data) {
    console.log(data);
    simResults = data;
    }); 
}