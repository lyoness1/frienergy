
var options = {
  responsive: true
};


var ctx_line = $("#lineGraph").get(0).getContext("2d");

$.get("/frienergy-per-time.json", function (data) {
  var myLineChart = new Chart(ctx_line, {type: 'line',
                                         data: data,
                                         options: options});
  $("#lineLegend").html(myLineChart.generateLegend());
});
