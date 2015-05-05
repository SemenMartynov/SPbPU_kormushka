var App = {};
App.currentUserId;

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
                    var tempalte = '<div class="party">Пользователь не состоит в этой покупке</div>';
                    $('#block-partner').append(tempalte);
                }
                else{
                    _.each(data,function(el){
                    var tempalte = '<div class="party">{0} ({1})</div>'.replace('{0}', el.label)
                                                                       .replace('{1}', el.depart);
                    $('#block-partner').append(tempalte);
                    });
                }
            }
        });
    });

})