var endpoint="/invoice/graph/";
var defaultData=[];
var labels=[];
var pie_label=[];
var pie_data=[];

$.ajax({
    method:"GET",
    url:endpoint,
    success: function(data){
        labels=data.labels;
        defaultData=data.default

        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Monthly Invoice Tracking',
                    data: defaultData,
                    backgroundColor: ["blue","red","green","#800000","#333300","red","blue","red","green","#800000","#333300","red",],
                    borderColor: ["black","black","black","black","black","black","black","black","black","black","black","black","black",],
                    borderWidth: 1,
                    hoverBackgroundColor:"#99ffff",
                    maxBarThickness: 100,
                        }]},
        options: {
        scales: {
            yAxes: [{ticks: {beginAtZero: true},gridLines: {color: "white",zeroLineColor: 'black',}}],
            xAxes: [{ticks: {beginAtZero: true},gridLines: {color: "white",zeroLineColor: 'black',},}],
            }}}) },
    error: function(error_data){
        console.log("error")
        console.log("error_data")
    }})

$.ajax({
    method:"GET",
    url:endpoint,
    success: function(data){
        pie_label=data.pie_label;
        pie_data=data.pie_data;
        var ctx = document.getElementById('myChart1').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: pie_label,
                datasets: [{
                    label: 'Companywise Invoice Tracking',
                    data: pie_data,
                    backgroundColor: ["#0175D8","#0175D8","#0175D8","#0175D8","#0175D8",],
                    borderColor: ["white","white","white","white","white","white",],
                    borderWidth: 1,
                    maxBarThickness: 100,
                    }]},
            options: {
            responsive: true,
            }})},
    error: function(error_data){
        console.log("error")
        console.log("error_data")}})


$.ajax({
    method:"GET",
    url:endpoint,
    success: function(data){
        noi_label=data.noi_label;
        noi_data=data.noi_data;

        var ctx = document.getElementById('myChart2').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: noi_label,
                datasets: [{
                    label: 'Companywise Invoice Tracking',
                    data: noi_data,
                    backgroundColor: [
                        "#DD4646","#FDC131","#077AFB","#67D190","#065687",
                    ],
                    borderColor: [
                        "white","white","white","white","white","white",

                    ],
                    borderWidth: 1,
                    
                    maxBarThickness: 100,

                }]
            },
            options: {
            responsive: true,
        
    }
        })
    },
    error: function(error_data){
        console.log("error")
        console.log("error_data")
    }

})