$(document).ready(function () {
	$('#statistics-tab a').click(function (e) {
		e.preventDefault()
		$(this).tab('show')

		//Статистика личная
		if($(this).attr('href')=='#personal-statistics'){
        	$('.personal-costs-paid').html("");
        	$('.personal-costs-not-paid').html("");
    		$('.personal-costs-all').html("");
    		$('.for-personal-all').html("");

			data = {
            'csrfmiddlewaretoken' : csrf_token,
            'type': 'personal',
            'date1': $('#datetimepicker1').data('date'),			
            'date2': $('#datetimepicker2').data('date')
	        };
	        $.ajax({
	            url: "/personal-statistics/",
	            type: "POST",
	            dataType: "json",
	            data: data,
	            success: function( data ) {
	            	$('.personal-costs-paid').html(data['UserСostsPaid']);
	            	$('.personal-costs-not-paid').html(data['UserСostsNotPaid']);
            		$('.personal-costs-all').html(data['UserСostsAll']);
            		$('.for-personal-all').html(data['ForUserAll']);
	            },
	        });
		}

		//Статистика пользователя
		if($(this).attr('href')=='#users-statistics'){
			$('.user-costs-paid').html("");
        	$('.user-costs-not-paid').html("");
    		$('.user-costs-all').html("");
    		$('.for-user-all').html("");

			user = $('#user-stat').attr("data-id");
			if(user){
				data = {
		        	'csrfmiddlewaretoken' : csrf_token,
		        	'date1': $('#datetimepicker1').data('date'),			
		        	'date2': $('#datetimepicker2').data('date'),
		        	'type': 'users',
		        	'userid': user,
		        };
		        $.ajax({
		            url: "/personal-statistics/",
		            type: "POST",
		            dataType: "json",
		            data: data,
		            success: function( data ) {
		            	$('.user-costs-paid').html(data['UserСostsPaid']);
		            	$('.user-costs-not-paid').html(data['UserСostsNotPaid']);
		        		$('.user-costs-all').html(data['UserСostsAll']);
		        		$('.for-user-all').html(data['ForUserAll']);	
		            }
		        });
			}
		}

		//Статистика отдела
		if($(this).attr('href')=='#departs-statistics'){
            $('.depart-costs-paid').html("");
            $('.depart-costs-not-paid').html("");
            $('.depart-costs-all').html("");
            $('.for-depart-all').html("");

			depart = $('#depart-stat').attr("data-id");
            if(depart){
                data = {
                'csrfmiddlewaretoken' : csrf_token,
                'date1': $('#datetimepicker1').data('date'),            
                'date2': $('#datetimepicker2').data('date'),
                'departid': depart,
                };
                $.ajax({
                    url: "/departs-statistics/",
                    type: "POST",
                    dataType: "json",
                    data: data,
                    success: function( data ) {
                        $('.depart-costs-paid').html(data['DepartСostsPaid']);
                        $('.depart-costs-not-paid').html(data['DepartСostsNotPaid']);
                        $('.depart-costs-all').html(data['DepartСostsAll']);
                        $('.for-depart-all').html(data['ForDepartAll']);
                    }
                });
            }
		}

		//Статистика организации
		if($(this).attr('href')=='#organization-statistics'){

        	$('.costs-paid').html("");
        	$('.costs-not-paid').html("");
    		$('.costs-all').html("");
			
			data = {
		        'csrfmiddlewaretoken' : csrf_token,
		        'date1': $('#datetimepicker1').data('date'),			
		        'date2': $('#datetimepicker2').data('date')
	        };
	        $.ajax({
	            url: "/organization-statistics/",
	            type: "POST",
	            dataType: "json",
	            data: data,
	            success: function( data ) {
	            	$('.costs-paid').html(data['СostsNotPaid']);
	            	$('.costs-not-paid').html(data['СostsPaid']);
            		$('.costs-all').html(data['СostsAll']);
	            }
	        });
		}
	})
	
	$( "#user-stat").autocomplete({
        source: function( request, response ) {
        data = {
            'csrfmiddlewaretoken' : csrf_token,
            name: request.term,
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
        	$("#user-stat").attr("data-id",ui.item.userid)
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
        	$("#depart-stat").attr("data-id",ui.item.departid)
        },
        open: function() { //открытие списка
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });

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
	$('#statistics-tab a[href="#personal-statistics"]').click(); // Select tab by name
});