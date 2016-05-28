// sets options for graphs and charts
var lineOptions = {
  responsive: true,
};

var pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  legend: {
            display: false,
          }
}


// creates a line graph of frienergies and interactions over time
var ctx_line = $("#lineGraph").get(0).getContext("2d");

$.get("/frienergy-per-time.json", function (data) {
  var myLineChart = new Chart(ctx_line, 
    {type: 'line', data: data, options: lineOptions});
});


// creates a pie chart of how much frienergy per interaction over time
var ctx_pie = $("#pieChart").get(0).getContext("2d");

$.get("/frienergy-per-int.json", function (data) {
  var myPieChart = new Chart(ctx_pie, 
    {type: 'pie', data: data, options: pieOptions});
});
