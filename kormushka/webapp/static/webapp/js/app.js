var App = {};

$(document).ready(function () {

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
})