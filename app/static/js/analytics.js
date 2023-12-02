
let packects_sent_chart =    new Chart("myChart", {
                type: "line",
                data: {
                  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                  datasets: [{
                    fill: false,
                    lineTension: 0,
                    backgroundColor: "rgba(0,0,255,1.0)",
                    borderColor: "rgba(0,0,255,0.1)",
                    data: []
                  }]
                },
                options: {
                  title: {display: true, text: "Family Outreach By Month"},
                  legend: {display: false},
                  // scales: {
                  //   yAxes: [{ticks: {min: 0, max: {{ max_month_packets_sent }} }}],
                  // }
                }
              });

let packects_status_chart =  new Chart("myChart2", {
  type: "doughnut",
  data: {
    labels: ["Returned", "Not Returned", "Waiting"],
    datasets: [{
      backgroundColor: [
        "#b91d47",
        "#00aba9",
        "#2b5797",
        "#e8c3b9",
        "#1e7145"
      ],
      data: []
    }]
  },
  options: {
    title: {
        display: true,
        text: "Packets by Status"
    },
    tooltips: {
        callbacks: {
            label: function (tooltipItem, data) {
                var dataset = data.datasets[tooltipItem.datasetIndex];
                var total = dataset.data.reduce(function (previousValue, currentValue, currentIndex, array) {
                    return previousValue + currentValue;
                });
                var currentValue = dataset.data[tooltipItem.index];
                var percentage = Math.floor(((currentValue / total) * 100) + 0.5);
                return currentValue + " | " + percentage + "%";
            }
        }
    }
}
});

let children_enrolled_chart =  new Chart("myChart3", {
  type: "line",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: []
    }]
  },
  options: {
    title: {display: true, text: "Children Enrolled by Month"},
    legend: {display: false},
    // scales: {
    //   yAxes: [{ticks: {min: 0, max:{{ max_children_enrolled }} }}],
    // }
  }
});

let children_not_enrolled_chart =  new Chart("myChart4", {
  type: "line",
  data: {
    labels:  ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: []
    }]
  },
  options: {
    title: {display: true, text: "Children Not Enrolled by Month"},
    legend: {display: false},
    // scales: {
    //   yAxes: [{ticks: {min: 0, max:{{max_children_not_enrolled}} }}],
    // }
  }
});

let children_not_enrolled_reasons_chart=  new Chart("myChart5", {
type: "bar",
data: {
labels: ["Does not meet employment/activity requirement", "Fee too high", "No Child Care Slots",
"No longer in Dallas County", "No longer needing services", "No packet received",
"No Provider Choice", "Not a Priority", "Not working/training", "On leave/STD",
"Over the income guidelines", "Unable to Reach Client", "Under participation requirement",
"Verification Docs Needed", "Other"],
datasets: [{
label: 'Number of families not Enrolled',
backgroundColor: [
    "#b91d47",
    "#00aba9",
    "#2b5797",
    "#e8c3b9",
    "#1e7145",
    "#800000",
    "#9A6324",
    "#808000",
    "#469990",
    "#000075",
    "#f58231",
    "#42d4f4",
    "#911eb4",
    "#f032e6",
    "#fabed4"
    ],
data: []
}]
},
options: {
title: {
display: true,
text: "Not Enrolled Reasons"
},
scales: {
xAxes: [{
ticks: {
callback: function(t) {
var maxLabelLength = 5;
if (t.length > maxLabelLength) return t.substr(0, maxLabelLength) + '...';
else return t;
}
}
}]
}
}
});

let processing_time_chart =  new Chart("myChart6", {
  type: "bar",
  data: {
    labels: ["0-10 days", "11-20 days", "21-30 days", "31+ days", "Not Processed Yet"],
    datasets: [{
      backgroundColor: ["red", "green","blue","orange","black"],
      data: []
    }]
  },
  options: {
    legend: {display: false},
    title: {
      display: true,
      text: "Processing Time"
    }

  }
});



function get_packets_sent_data(year){
    console.log(year)
    $.ajax({
        url: '/analytics/packets_sent?year=' + year,
        type: 'GET',
        success: function(response) {
            console.log(response)
            console.log(packects_sent_chart)

            
            packects_sent_chart.reset();
            packects_sent_chart.data.datasets[0].data = response.data;
            packects_sent_chart.update();
        },
        error: function(error) {
            console.error('Error fetching Graph data:', error);
        }
    });
}

function get_packets_status_data(year){

    $.ajax({
        url: '/analytics/packets_status?year=' + year,
        type: 'GET',
        success: function(response) {
            
            packects_status_chart.reset();
            packects_status_chart.data.datasets[0].data = response.data;
            packects_status_chart.update();
            
        },
        error: function(error) {
            console.error('Error fetching Graph data:', error);
        }
    });
}

function get_children_enrolled_data(year){
    $.ajax({
        url: '/analytics/children_enrolled?year=' + year,
        type: 'GET',
        success: function(response) {
            children_enrolled_chart.reset();
            children_enrolled_chart.data.datasets[0].data = response.data;
            children_enrolled_chart.update();
        },
        error: function(error) {
            console.error('Error fetching Graph data:', error);
        }
    });
}

function get_children_not_enrolled_data(year){
    $.ajax({
        url: '/analytics/children_not_enrolled?year=' + year,
        type: 'GET',
        success: function(response) {
            children_not_enrolled_chart.reset();
            children_not_enrolled_chart.data.datasets[0].data = response.data;
            children_not_enrolled_chart.update();
        },
        error: function(error) {
            console.error('Error fetching Graph data:', error);
        }
    });
}

function get_children_not_enrolled_reasons(year){
    $.ajax({
        url: '/analytics/children_not_enrolled_reasons?year=' + year,
        type: 'GET',
        success: function(response) {
            children_not_enrolled_reasons_chart.reset();
            children_not_enrolled_reasons_chart.data.datasets[0].data = response.data;
            children_not_enrolled_reasons_chart.update();
        },
        error: function(error) {
            console.error('Error fetching Graph data:', error);
        }
    });
}

function get_processing_time_data(year){
    $.ajax({
        url: '/analytics/processing_time?year=' + year,
        type: 'GET',
        success: function(response) {
            processing_time_chart.reset();
            processing_time_chart.data.datasets[0].data = response.data;
            processing_time_chart.update();
        },
        error: function(error) {
            console.error('Error fetching Graph data:', error);
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Fetch data from the Flask server
    var current_year;

    $.ajax({
        url: '/analytics/get_years',
        type: 'GET',
        success: function(response) {
            const years = response.data;
            const year_dropdown_packets_sent = $('#year_dropdown_packets_sent');
            year_dropdown_packets_sent.empty();
            year_dropdown_packets_sent.val('');

            year_dropdown_packets_status = $('#year_dropdown_packets_status');
            year_dropdown_packets_status.empty();
            year_dropdown_packets_status.val('');


            year_dropdown_child_enrolled = $('#year_dropdown_child_enrolled');
            year_dropdown_child_enrolled.empty();
            year_dropdown_child_enrolled.val('');

            year_dropdown_not_enrolled = $('#year_dropdown_not_enrolled');
            year_dropdown_not_enrolled.empty();
            year_dropdown_not_enrolled.val('');

            year_dropdown_reasons = $('#year_dropdown_reasons');
            year_dropdown_reasons.empty();
            year_dropdown_reasons.val('');

            year_dropdown_processing_time = $('#year_dropdown_processing_time');
            year_dropdown_processing_time.empty();
            year_dropdown_processing_time.val('');

            current_year = years[0];
            // console.log(current_year);

            years.forEach((year, index) => {
                year_dropdown_packets_sent.append($('<option></option>').attr('value', year).text(year));
                year_dropdown_packets_status.append($('<option></option>').attr('value', year).text(year));
                year_dropdown_child_enrolled.append($('<option></option>').attr('value', year).text(year));
                year_dropdown_not_enrolled.append($('<option></option>').attr('value', year).text(year));
                year_dropdown_reasons.append($('<option></option>').attr('value', year).text(year));
                year_dropdown_processing_time.append($('<option></option>').attr('value', year).text(year));
                // if (selectedRole && role.name === selectedRole) {
                //     roleDropdown.val(role.id);
                // }
            });
            var packets_sent = document.getElementById('year_dropdown_packets_sent');
            packets_sent.addEventListener('change', () => {
                // console.log(year_dropdown.value)
                get_packets_sent_data(packets_sent.value)
            
            });

            var packets_status = document.getElementById('year_dropdown_packets_status');
            packets_status.addEventListener('change', () => {
                // console.log(year_dropdown.value)
                get_packets_status_data(packets_status.value)
            
            });

            var children_enrolled = document.getElementById('year_dropdown_child_enrolled');
            children_enrolled.addEventListener('change', () => {
                // console.log(year_dropdown.value)
                get_children_enrolled_data(children_enrolled.value)
            
            });

            var children_not_enrolled = document.getElementById('year_dropdown_not_enrolled');
            children_not_enrolled.addEventListener('change', () => {
                // console.log(year_dropdown.value)
                get_children_not_enrolled_data(children_not_enrolled.value)
            
            });

            var children_not_enrolled_reasons = document.getElementById('year_dropdown_reasons');
            children_not_enrolled_reasons.addEventListener('change', () => {
                // console.log(year_dropdown.value)
                get_children_not_enrolled_reasons(children_not_enrolled_reasons.value)
            
            });

            var processing_time = document.getElementById('year_dropdown_processing_time');
            processing_time.addEventListener('change', () => {
                // console.log(year_dropdown.value)
                get_processing_time_data(processing_time.value)
            
            });



            get_packets_sent_data(current_year);
            get_packets_status_data(current_year);
            get_children_enrolled_data(current_year);
            get_children_not_enrolled_data(current_year);
            get_children_not_enrolled_reasons(current_year);
            get_processing_time_data(current_year);
        },
        error: function(error) {
            console.error('Error fetching roles:', error);
        }
    });

});