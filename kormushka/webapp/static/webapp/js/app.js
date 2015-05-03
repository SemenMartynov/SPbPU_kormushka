$(document).ready(function () {

$('#buy').click(function(e){
	listUserId = [];
    $(".party").each(function() {listUserId.push($(this).attr("data-user-id"))});
    if (listUserId.length == 0) {
    	e.preventDefault();
    }
	$('#purchase').append('<input type="hidden" name="userpk" value="' + listUserId + '">')
	
	listDepartId = [];
	$(".party").each(function() {listDepartId.push($(this).attr("data-depart-id"))});
	if (listDepartId.length == 0) {
    	e.preventDefault();
    }
	$('#purchase').append('<input type="hidden" name="departpk" value="' + listDepartId + '">')
});

$('.showMembers').click(function(){
	$('#block-partner').html("");
	data = {
				'csrfmiddlewaretoken' : csrf_token,
				purchaseId: $(this).attr("data-id"),
	},
	$.ajax({
          	url: "/get-purchase-users/",
			type: "POST",
			dataType: "json",
			data: data,
            success: function( data ) {
            	if (data == 'error'){
            		var str = '<div class="party">Пользователь не состоит в этой покупке</div>';
            		$('#block-partner').append(str);
            	}
            	else{
            		_.each(data,function(el){
            		var str = '<div class="party">' +  el.label + ' (' + el.depart + ')</div>';
            		$('#block-partner').append(str);
            		}); 
            	}           	
         	}
        });
	});

$(function() {
 
    $( "#user-member" ).autocomplete({
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
            	console.log(data);
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
   			var str = '<div data-user-id="' + ui.item.userid + '" data-depart-id="' + ui.item.departid + '" class="party">' +  ui.item.value + '</div>';
    		$('#block-partner-add').append(str);
      },
      open: function() { //открытие списка
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
      },
      close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
      }
    });
  });
})