$(document).ready(function () {

    /**********
        buy click handler
    **********/
    $('#buy').click(function(e){

        //form validation
        var validator = new App.Validator();
        var check = validator.validate([
            {
                selector: "#name",
                type: "name",
                message: "введите корректное название"
            },
            {
                selector: "#cost",
                type: "int",
                message: "введите корректную сумму"
            }
        ]);
        if (!check) {
            e.preventDefault();
        }

        //other operation
        listUserId = [];
        $(".party").each(function() {listUserId.push($(this).attr("data-user-id"))});
        if (listUserId.length == 0) {
            e.preventDefault();
        }
        $('#purchase').append('<input type="hidden" name="userpk" value="{0}">'.replace("{0}",listUserId))

        listDepartId = [];
        $(".party").each(function() {listDepartId.push($(this).attr("data-depart-id"))});
        if (listDepartId.length == 0) {
            e.preventDefault();
        }
        $('#purchase').append('<input type="hidden" name="departpk" value="{0}">'.replace("{0}", listDepartId))
    });


    /**********
        add autocomplete for members in purchase
    **********/
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
            var span = '<span class="glyphicon glyphicon-remove remove-party"></span>';
            $('#block-partner-add').children('.party[data-user-id={0}]'.replace('{0}',ui.item.userid)).remove();
            if (ui.item.userid ==  App.currentUserId){                
                var template = '<div data-user-id="' + ui.item.userid + '" data-depart-id="' + ui.item.departid + '" class="party">' + ui.item.value + '</div>';
                $('#block-partner-add').prepend(template);
            } else
            {
                var template = '<div data-user-id="' + ui.item.userid + '" data-depart-id="' + ui.item.departid + '" class="party">' + span +  ui.item.value + '</div>';
                $('#block-partner-add').append(template);
            }
            $('#block-partner-add .remove-party').last().click(function(){
                $(this).parent().remove();
            });
            
        },
        open: function() { //открытие списка
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });

    $( "#depart" ).change(function() {
        var UserId = App.currentUserId;
        var selectId = $(this).children("option:selected").val();
        var selectDepart = $(this).children("option:selected").text();
        $('#block-partner-add').children('.party[data-user-id={0}]'.replace('{0}',UserId)).remove();
        var template = '<div data-user-id="' + UserId + '" data-depart-id="' + selectId + '" class="party">' +  App.currentUserFullName + ' (' + selectDepart + ')</div>';
        $('#block-partner-add').prepend(template);
    });

    
    
});