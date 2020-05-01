var endpoint="/invoice/graphMonthly/";
var defaultData=[];
var labels=[];
$.ajax({
    method:"GET",
    url:endpoint,
    success: function(data){

        labels=data.labels;
        defaultData=data.data1;
        var d = [];
        var l = [];
        for (var i=0;i<defaultData.length;i++) {

            const date = new Date(labels[i]);

            const month = date.toLocaleString('default', { month: 'long' });
            if(month==a1){
                d.push(defaultData[i])
                l.push(labels[i])
            }
        }

        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: l,
                datasets: [{
                    label: 'Monthly Invoice Tracking',
                    data: d,
                    backgroundColor: [
                        "#66e0ff",
                    ],
                    borderColor: [
                        "#008fb3",
                    ],
                    pointRadius:5,
                    pointColor:"blue",
                    borderWidth: 2,
                    hoverBackgroundColor:"#99ffff",
                    maxBarThickness: 100,

                }]
            },
            options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                gridLines: {
                    color: "white",
                    zeroLineColor: 'black',
                }
            }],
            xAxes: [{
                ticks: {
                    beginAtZero: true
                },
                gridLines: {
                color: "white",
                zeroLineColor: 'black',
                },
            }],
        }
    }
        })
    },
    error: function(error_data){
        console.log("error")
        console.log("error_data")
    }

})

$.ajax({
    method:"GET",
    url:endpoint,
    success: function(data){
        if(a1=="January"){
            d=data.jan_data;
            l=data.jan_label;
        }else if(a1=="February"){
            d=data.feb_data;
            l=data.feb_label;
        }else if(a1=="March"){
            d=data.mar_data;
            l=data.mar_label;
        }else if(a1=="April"){
            d=data.apr_data;
            l=data.apr_label;
        }else if(a1=="May"){
            d=data.may_data;
            l=data.may_label;
        }else if(a1=="June"){
            d=data.jun_data;
            l=data.jun_label;
        }else if(a1=="July"){
            d=data.jul_data;
            l=data.jul_label;
        }else if(a1=="August"){
            d=data.aug_data;
            l=data.aug_label;
        }else if(a1=="September"){
            d=data.sep_data;
            l=data.sep_label;
        }else if(a1=="October"){
            d=data.oct_data;
            l=data.oct_label;
        }else if(a1=="November"){
            d=data.nov_data;
            l=data.nov_label;
        }else if(a1=="December"){
            d=data.dec_data;
            l=data.dec_label;
        }else {
            d=[];
            l=[];
        }

        var ctx = document.getElementById('myChart1').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: l,

                datasets: [{
                    label: 'Monthly Companywise Invoice Tracking',
                    data: d,
                    backgroundColor: [
                        "blue","red","green","#800000","#333300","red","blue","red","green","#800000","#333300","red","blue","red","green","#800000","#333300","red","blue","red","green","#800000","#333300","red",
                    ],
                    borderColor: [
                        "white","white","white","white","white","white","white","white","white","white","white","white","white","white","white",

                    ],
                    borderWidth: 1,
                    hoverBackgroundColor:"#99ffff",
                    maxBarThickness: 100,


                }]
            },
            options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                gridLines: {
                    color: "white",
                    zeroLineColor: 'black',
                }
            }],
            xAxes: [{
                ticks: {
                    beginAtZero: true
                },
                gridLines: {
                color: "white",
                zeroLineColor: 'black',
                },
            }],
        }
    }
        })
    },
    error: function(error_data){
        console.log("error")
        console.log("error_data")
    }

})