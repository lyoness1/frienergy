// gets contact-id from hidden div on page for use globally
var contactId = $("#contact-id").data('id');

// sets options for the graphs and charts
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
var ctx_line_contact = $("#contactLineGraph").get(0).getContext("2d");

$.post("/frienergy-per-time-for-contact.json", data={'id': contactId}, function (data) {
var myLineChart = new Chart(ctx_line_contact, 
    {type: 'line', data: data, options: lineOptions});
});


// creates a pie chart of how much frienergy per interaction over time
var ctx_pie_contact = $("#contactPieChart").get(0).getContext("2d");

$.post("/frienergy-per-int-for-contact.json", data={'id': contactId}, function (data) {
  var myPieChart = new Chart(ctx_pie_contact, 
    {type: 'pie', data: data, options: pieOptions});
});
