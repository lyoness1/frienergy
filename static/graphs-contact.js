// gets contact-id from hidden div on page for use globally
var contactId = $("#contact-id").data('id');


// CONTACT LINE GRAPH
// defines the line graph object globally for use in update function
var myLineChart;

// defines the line graph options
var lineOptions = {
  responsive: true,
};

// grabs the location of the line graph from the DOM
var ctx_line_contact = $("#contactLineGraph").get(0).getContext("2d");

// draws the line graph on page load
$.post("/frienergy-per-time-for-contact.json",
    data={'id': contactId, 'scale': 'all-time'},
    function (data) {
        myLineChart = new Chart(ctx_line_contact, 
        {type: 'line', data: data, options: lineOptions
    });
});

// listens for a change in time scale from the buttons on the panel and 
// redraws graph with new data scale 
$('.toggle-graph').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    timeScale = $(this).children().val();
    $.post("/frienergy-per-time-for-contact.json",
        data={'id': contactId, 'scale': timeScale},
        function (data) {
            myLineChart.config.data = data;
            myLineChart.update();
        });
});


// CONTACT PIE CHART
// defines pie chart options
var pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  legend: {
            display: false,
          }
};

// grabs the location of the pie chart canvas element from the DOM
var ctx_pie_contact = $("#contactPieChart");

// draws the line chart on page load
$.post("/frienergy-per-int-for-contact.json", data={'id': contactId}, function (data) {
  var myPieChart = new Chart(ctx_pie_contact, 
    {type: 'pie', data: data, options: pieOptions});
});
