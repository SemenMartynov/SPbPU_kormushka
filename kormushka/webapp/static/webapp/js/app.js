$(document).ready(function () {

$('#buy').click(function(e){
	l = [];
    $(".party").each(function() {l.push($(this).attr("data-pk"))});
    if (l.length == 0) {
    	e.preventDefault();
    }
	$('#purchase').append('<input type="hidden" name="userpk" value="' + l + '">')
});

$('.showMembers').click(function(){
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
            	$('#block-partner').html("");
            	_.each(data,function(el){
            		var str = '<div class="party">' +  el.label + '</div>';
    				$('#block-partner').append(str);
            	}); 

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
            			"pk":el.value
            		});
            	});
            	response(arr);
         	}
        });
      },
      minLength: 3,
      select: function( event, ui ) { //Выбор пункта
   			var str = '<div data-pk="' + ui.item.pk + '" class="party">' +  ui.item.value + '</div>';
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