// LINE GRAPH
// sets options for the line graph
var lineOptions = {
  responsive: true,
};

// decales the line chart object globally for access by update function
var myLineChart;

// grabs the location of the line graph canvas element from the DOM
var ctx_line = $("#lineGraph");

// draws the line graph when page loads with 'all-time' as the first time scale
$.get("/frienergy-per-time.json", {'scale': 'all-time'}, function (data) {
    myLineChart = Chart.Line(ctx_line, {data: data, options: lineOptions});
  });

// listens for a change in time scale from the buttons on the panel and 
// redraws graph with new data scale 
$('.toggle-graph').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    timeScale = $(this).children().val();
    $.get("/frienergy-per-time.json", {'scale': timeScale}, function (data) {
    myLineChart.config.data = data;
    myLineChart.update();
  });
});


// PIE CHART
// defines chart options
var pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  legend: {
            display: false,
          }
}

// grabs the location of the canvas element from the DOM
var ctx_pie = $("#pieChart");

// draws the pie chart when page loads
$.get("/frienergy-per-int.json", function (data) {
  var myPieChart = new Chart(ctx_pie, 
    {type: 'pie', data: data, options: pieOptions});
});
