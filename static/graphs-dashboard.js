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

// grabs the value of the time scale from the button group for use on first load
var timeScale = "all-time";

// draws the line graph on the canvas
function drawLineGraph(timeScale) {
  $.get("/frienergy-per-time.json", {'scale': timeScale}, function (data) {
  var myLineChart = new Chart(ctx_line, 
    {type: 'line', data: data, options: lineOptions});
  });
}

// creates a line graph of frienergies and interactions over time
var ctx_line = $("#lineGraph").get(0).getContext("2d");
drawLineGraph(timeScale);

// creates a pie chart of how much frienergy per interaction over time
var ctx_pie = $("#pieChart").get(0).getContext("2d");

// draws the pie chart
$.get("/frienergy-per-int.json", function (data) {
  var myPieChart = new Chart(ctx_pie, 
    {type: 'pie', data: data, options: pieOptions});
});

// listens for a change in time scale from the buttons on the panel and 
// redraws graph with new data scale 
$('.toggle-graph').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    timeScale = $(this).children().val();
    drawLineGraph(timeScale);
});
