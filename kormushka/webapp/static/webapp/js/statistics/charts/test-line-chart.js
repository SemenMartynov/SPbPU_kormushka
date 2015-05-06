$(function () {

    //  select template and inner elements for work
    var template = $("#test-chart-template");
    if (!template[0]) return;

    var listChartContainer = template.find("#test-linechart");

    //  http://www.chartjs.org/docs/#line-chart
    // https://github.com/nnnick/Chart.js/blob/master/samples/line.html

    var lineChartData = {
        labels : ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],
        datasets : [
            {
                label: "My First dataset",
                fillColor : "rgba(151,187,205,0.2)",
                strokeColor : "rgba(151,187,205,1)",
                pointColor : "rgba(151,187,205,1)",
                pointStrokeColor : "#fff",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(220,220,220,1)",
                data : [
                    1000,
                    2000,
                    500,
                    490,
                    3000,
                    200,
                    0,
                    700,
                    1100,
                    30,
                    12,
                    1000
                ]
            }
        ]
    }

    //  check selected element
    if (!!listChartContainer) {
        var ctx = listChartContainer[0].getContext("2d"); //https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
        var testLineChart = new Chart(ctx);
        testLineChart.Line(lineChartData, {
            responsive: true
        });

        //  data update if you need
        /*
        lineChartData.datasets[0].data = [
            100,
            2000,
            500,
            490,
            3000,
            200,
            0,
            700,
            1100,
            30,
            12,
            1000
        ];
        testLineChart.Line(lineChartData);
        */
    }


});