$(document).ready(function () {

    var departSidebarItems = $("#departs-sidebar .depart-sidebar-item");
    var usersDiv = $("#users-by-depart");

    var userTemplate = _.template("<li data-user-id='<%= id %>'><%= fullName %></li>");
    var userTemplateEmpty = _.template("В этом отделе пока еще нет сотрудников...");

    departSidebarItems.click(function() {
        var departId = $(this).attr("data-depart-id");

        $.ajax({
            url: "/get-users/",
            type: "POST",
            dataType: "json",
            data: {
                "csrfmiddlewaretoken" : csrf_token,
                "departId": departId
            },
            success: function(data) {
                if ($.isArray(data) && data.length!=0) {
                    usersDiv.html("");
                    _.each(data, function(v) {
                        usersDiv.append(userTemplate(v));
                    });
                } else {
                    usersDiv.html(userTemplateEmpty());
                }
            },
            error: function(e) {
                console.log(e);
            }
        });
    });

});