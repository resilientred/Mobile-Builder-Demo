/**
 * Created by gootax on 10.07.17.
 */
/**
 * Created by gootax on 29.06.17.
 */


(function ($) {
    let app = {
        appForm: '#saveApplication',
        init: function () {
            this.registerFormSubmitEvent();
        },
        registerFormSubmitEvent() {
            $(this.appForm).on('submit', function () {
                $.ajax({
                    type: 'POST', url: '/driver_app_save', data: $('#saveApplication').serialize(),
                    success: function (response) {
                        parseAction(response)
                    }
                });
                return false
            });
        }
    };
    app.init();
})(jQuery);

function parseAction(action) {
    let json_action = $.parseJSON(action);
    console.log(json_action);
    switch (json_action.action) {
        case "redirect":

            let url = json_action.data.url;
            if (url) {
               window.location = url
            }
            break;
        case "error":
            let message = json_action.data.message;
            if (message) {
                 console.log(json_action);
                alert(message)
            }
            break;
        default:
            break;
    }
}
