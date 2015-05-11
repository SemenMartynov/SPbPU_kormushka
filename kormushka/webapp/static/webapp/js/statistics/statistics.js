$(document).ready(function () {

    var template = $("#test-chart-template");
    if (!template[0]) return;
    var listChartContainer = template.find("#test-linechart");

    var lineChartData = {
        labels : [],
        datasets : [
            {
                label: "My First dataset",
                fillColor : "rgba(151,187,205,0.2)",
                strokeColor : "rgba(151,187,205,1)",
                pointColor : "rgba(151,187,205,1)",
                pointStrokeColor : "#fff",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(220,220,220,1)",
                data : []
            },
        ]
    };

    var ctx = listChartContainer[0].getContext("2d"); //https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
    var chart = new Chart(ctx);
    var lineChart = chart.Line(lineChartData, {
        responsive: true,
    });

    function costsLineChart(data,labels,result){
        if(result){
            //  select template and inner elements for work
            //  http://www.chartjs.org/docs/#line-chart
            // https://github.com/nnnick/Chart.js/blob/master/samples/line.html
            //  check selected element

            lineChartData.labels = labels;
            lineChartData.datasets[0].data = data;

            lineChart.initialize(lineChartData);
        }
    }

    function getHtmlDetail(Days, Months, Years){
        var strHtml = "";
        if(Days){
            strHtml = strHtml + '<a class="detail-stat-day step-detail" data-type="day" data-toggle="modal" href="#">День</a>';
        }
        if(Months){
            strHtml = strHtml + '<a class="detail-stat-month step-detail" data-type="month" data-toggle="modal" href="#">Месяц</a>';
        }
        if(Years){
            strHtml = strHtml + '<a class="detail-stat-year step-detail" data-type="year" data-toggle="modal" href="#">Год</a>';
        }
        return strHtml;
    }

    function getDataGraph(data){
        App.sumOnСostsPaid = data['sumOnСostsPaid'];
        App.sumOnСostsNotPaid = data['sumOnСostsNotPaid'];
        App.sumOnСostsAll = data['sumOnСostsAll'];
        App.labels =  data['labels'];
        App.result = data['result'];
    }

    function conditionStatistics(href,typeDetailStat){
        var error = true;
        var ctx = $(href);
        var user = $('#user-stat').attr("data-id");
        var depart = $('#depart-stat').attr("data-id");
        var start_date = $('#datetimepicker1').data('date');
        var end_date = $('#datetimepicker2').data('date');
        var typeStat = "";
        var typeUser = "";
        var ajax_request = "";
        var inform = "";

        if(typeDetailStat == "first"){
            $('.costs-paid').html("");
            $('.costs-not-paid').html("");
            $('.costs-all').html("");
            $('.for-costs-all').html("");
            $('.number-paid').html("");
            $('.number-not-paid').html("");
            $('.number-all').html("");
            $('.for-number-all').html("");
            $(".linechart-text").html("");
            $(".detail-stat").html("");
        }
        resGraph();

        if(href == "#personal-statistics"){
            typeStat = "personal-stat";
            typeUser = "personal";
            error = false;
        } else if(href == "#users-statistics" && user){
            typeStat = "personal-stat";
            typeUser = "users";
            inform = " для пользователя: " + App.UserName;
            error = false;
        } else if(href == "#departs-statistics" && depart){
            typeStat = "depart-stat";
            inform = " для отдела: " + App.DepartName;
            error = false;
        } else if(href == "#organization-statistics"){
            typeStat = "organization-stat";
            inform = " для организации"
            error = false;
        }
        if(!error){
            if (ajax_request) {
                ajax_request.abort();
            }
            data = {
            'csrfmiddlewaretoken' : csrf_token,
            'typeUser': typeUser,
            'typeStat': typeStat,
            'typeDetailStat': typeDetailStat,
            'date1': start_date,            
            'date2': end_date,
            'userid': user,
            'departid': depart,
            };
            ajax_request = $.ajax({
                url: "/get-data-for-stat/",
                type: "POST",
                dataType: "json",
                data: data,
                success: function(data) {
                    console.log(data);
                    $(ctx).find('.show-graph').show();
                    $(ctx).find('.costs-paid').html(data['СostsPaid']);
                    $(ctx).find('.costs-not-paid').html(data['СostsNotPaid']);
                    $(ctx).find('.costs-all').html(data['СostsAll']);
                    $(ctx).find('.for-costs-all').html(data['ForСostsAll']);
                    $(ctx).find('.number-paid').html(data['NumberPaid']);
                    $(ctx).find('.number-not-paid').html(data['NumberNotPaid']);
                    $(ctx).find('.number-all').html(data['NumberAll']);
                    $(ctx).find('.for-number-all').html(data['ForAllNumber']);
                    
                    getDataGraph(data);//запись в глобальную переменную данных для графика

                    costsLineChart(App.sumOnСostsAll,App.labels,App.result);
                    $(".linechart-text").html("С <b>" + data['start_date'] + "</b> по <b>" + data['end_date'] + "</b>" + inform);
                    $('.detail-stat').html(getHtmlDetail(data['detailByDays'],data['detailByMonths'],data['detailByYears']));
                    addClickDetail(data['targetDetail']);
                    $(ctx).find(".show-graph:nth(2)").removeClass("glyphicon-eye-open").addClass("glyphicon-eye-close active")
                },
            });
        }else{
            $(ctx).find('.show-graph').hide();
            costsLineChart(App.sumOnСostsAll,App.labels,App.result);
        }
    }

	$('#statistics-tab a').click(function (e) {
        e.preventDefault();
        if($(this).parent().attr('class')!='active') {
            typeDetailStat = "first";
            clerEye();
            $(this).tab('show');
            var href = $(this).attr('href');
            conditionStatistics(href,typeDetailStat);
        }	
	})

    $('#button-show').click(function (e){
        typeDetailStat = "first";
        e.preventDefault()
        clerEye();
        var href = $('#statistics-tab li.active a').attr('href');
        conditionStatistics(href,typeDetailStat);
    })
	
	$( "#user-stat").autocomplete({
        source: function( request, response ) {
        data = {
            'csrfmiddlewaretoken' : csrf_token,
            name: request.term,
            type: 'all',
        },
        $.ajax({
            url: "/get-users-by-name/",
            type: "POST",
            dataType: "json",
            data: data,
            success: function( data ) {
                arr = [];
                _.each(data,function(el){
                    arr.push({
                        "value": el.label,
                        "label": el.label,
                        "userid":el.userid,
                        "departid":el.departid,
                    });
                });
                response(arr);
            }
        });
        },
        minLength: 3,
        select: function( event, ui ) { //Выбор пункта
        	$("#user-stat").attr("data-id",ui.item.userid);
            App.UserName = ui.item.label;
        },
        open: function() { //открытие списка
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });

	$( "#depart-stat").autocomplete({
        source: function( request, response ) {
        data = {
            'csrfmiddlewaretoken' : csrf_token,
            depart: request.term,
        },
        $.ajax({
            url: "/get-depart-by-name/",
            type: "POST",
            dataType: "json",
            data: data,
            success: function( data ) {
                arr = [];
                _.each(data,function(el){
                    arr.push({
                        "value": el.label,
                        "label": el.label,
                        "departid":el.departid,
                    });
                });
                response(arr);
            }
        });
        },
        minLength: 0,
        select: function( event, ui ) { //Выбор пункта
        	$("#depart-stat").attr("data-id",ui.item.departid);
            App.DepartName = ui.item.label;
        },
        open: function() { //открытие списка
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });

    $( ".period-purchase").click(function (){
        var type = $(this).attr('data-type');
        if(type == "all"){
            $('#datetimepicker1').data("DateTimePicker").date(null);
            $('#datetimepicker2').data("DateTimePicker").date(null);
        }else{
            data = {
                'csrfmiddlewaretoken' : csrf_token,
                'type': type,
            };
            $.ajax({
                url: "/get-date-for-period/",
                type: "POST",
                dataType: "json",
                data: data,
                success: function( data ) {
                    $('#datetimepicker1').data("DateTimePicker").date(data['date1']);
                    $('#datetimepicker2').data("DateTimePicker").date(data['date2']);
                }
            });
        } 
    });

    $(".show-graph").click(function(){
        if(!$(this).hasClass("active")){
            $(this).parents("table").find("span.show-graph.active").removeClass("active glyphicon-eye-close").addClass("glyphicon-eye-open")
            $(this).removeClass("glyphicon-eye-open").addClass("glyphicon-eye-close active")
            var type = $(this).attr('data-type');
            var sum = [];
            if (type == "paid"){
               sum = App.sumOnСostsPaid;
            }else if(type == "not-paid"){
                sum = App.sumOnСostsNotPaid;
            }else if(type == "all"){
               sum = App.sumOnСostsAll;
            }
            costsLineChart(sum,App.labels,App.result);
        }
    })

	$(function () {
        $('#datetimepicker1').datetimepicker({
            locale: 'ru',
            format: 'DD/MM/YYYY',
            viewMode: 'days'
        });
    });

	$(function () {
        $('#datetimepicker2').datetimepicker({
            locale: 'ru',
            format: 'DD/MM/YYYY',
            viewMode: 'days'
        });
    });

    function clerEye(){
        $('.show-graph').removeClass("active glyphicon-eye-close").addClass("glyphicon-eye-open");
    }

    function addClickDetail(target){
        $(".step-detail").click(function(e){
            typeDetailStat = $(this).attr('data-type');
            e.preventDefault()
            clerEye();
            var href = $('#statistics-tab li.active a').attr('href');
            conditionStatistics(href,typeDetailStat);
        });
        $(".step-detail." + target).addClass("target-detail");
    }

    var $range = $(".js-range-slider");

	conditionStatistics("#personal-statistics","first"); // Select tab by name
});