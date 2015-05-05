$(document).ready(function () {
    //  vars
    var departSidebarItems = $("#departs-sidebar .depart-sidebar-item");
    var usersDiv = $("#users-by-depart");

    var userTemplate = _.template("<li data-user-id='<%= id %>'><%= fullName %></li>");
    var userTemplateEmpty = _.template("В этом отделе пока еще нет сотрудников...");

    //  functions
    var getUsersByDepart = function(departId) {
        return $.ajax({
            url: "/get-users/",
            type: "POST",
            dataType: "json",
            data: {
                "csrfmiddlewaretoken" : csrf_token,
                "departId": departId
            }
        });
    }

    var fillUsersDiv = function(users) {
        if ($.isArray(users) && users.length!=0) {
            usersDiv.html("");
            _.each(users, function(v) {
                usersDiv.append(userTemplate(v));
            });
        } else {
            usersDiv.html(userTemplateEmpty());
        }
    };

    //  init view
    departSidebarItems.removeClass("active");
    departSidebarItems.first().parents("li").addClass("active");
    var departId = departSidebarItems.first().attr("data-depart-id");
    getUsersByDepart(departId)
    .done(function(result) {
        fillUsersDiv(result);
    })
    .fail(function(e) {
        console.log(e);
    });

    //  listeners
    departSidebarItems.click(function() {
        departSidebarItems.parents("li").removeClass("active");
        $(this).parents("li").addClass("active");

        var departId = $(this).attr("data-depart-id");

        getUsersByDepart(departId)
        .done(function(result) {
            fillUsersDiv(result);
        })
        .fail(function(e) {
            console.log(e);
        });
    });

});