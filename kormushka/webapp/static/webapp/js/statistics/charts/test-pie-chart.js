$(document).ready(function () {

    //  http://www.chartjs.org/docs/#doughnut-pie-chart
    //  https://github.com/nnnick/Chart.js/blob/master/samples/pie.html

    var pieData = [
        {
            value: 1000,
            color:"#F7464A",
            highlight: "#FF5A5E",
            label: "Red"
        },
        {
            value: 1200,
            color: "#46BFBD",
            highlight: "#5AD3D1",
            label: "Green"
        },
        {
            value: 2000,
            color: "#FDB45C",
            highlight: "#FFC870",
            label: "Yellow"
        },
        {
            value: 500,
            color: "#949FB1",
            highlight: "#A8B3C5",
            label: "Grey"
        },
        {
            value: 650,
            color: "#4D5360",
            highlight: "#616774",
            label: "Dark Grey"
        }
    ];

    var ctx = $("#test-piechart")[0].getContext("2d"); //https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
    var testPieChart = new Chart(ctx);
    testPieChart.Pie(pieData);


    //  update data if you need
    /*
    var newPieData = [
        {
            value: 1000,
            color:"#F7464A",
            highlight: "#FF5A5E",
            label: "Red"
        },
        {
            value: 400,
            color: "#46BFBD",
            highlight: "#5AD3D1",
            label: "Green"
        }
    ];
    testPieChart.Pie(newPieData);
    */
});