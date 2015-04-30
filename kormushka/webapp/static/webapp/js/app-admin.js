$(document).ready(function () {
    $("#ldap-sync").click(function() {
        var data = {'csrfmiddlewaretoken' : csrf_token};
        $.ajax({
            url: "/ldap-sync/",
            type: "POST",
            dataType: "json",
            data: data,
            success: function (data) {
                console.log(data);
            },
            error: function (data) {
                console.log('error');
            }
        });
    });
})