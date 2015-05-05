/**********
    elements validator
    can validation input elements and show message after input field
**********/

App.Validator = function() {
    this.template = _.template("<span class='help-block help-validator'><%= message %></span>");
    this.regexps = {
        "name": /^[a-zA-Zа-яА-Я.()/\0-9]{4,30}$/,
        "int": /^\d+$/
    };
    this.validate = function(data) {
        var ctx = this;
        var result = true;

        _.each(data, function(v) {
            var el = $(v.selector);
            var val = el.val();
            var regexp = ctx.regexps[v.type];
            var message = v.message;

            if ( el.is("input") && regexp ) {
                var fGroup = el.parents(".form-group");

                var nextElement = el.next();
                if (nextElement.hasClass("help-block help-validator")) nextElement.remove();

                fGroup.removeClass("has-error has-success has-warning");

                if ( regexp.test(val) ) {
                    fGroup.addClass("has-success");
                } else {
                    fGroup.addClass("has-error");
                    el.after(ctx.template({
                        message: message
                    }));
                    el.next().click(function() {
                        $(this).remove();
                    });
                    result = false;
                }
            }
        });

        return result;
    }
}