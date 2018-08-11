

(function ($) {
    let build = {
        appForm: '#buildForm',
        init: function () {
            this.registerFormSubmitEvent();
        },
        registerFormSubmitEvent() {
            $(this.appForm).on('submit', function () {
                $.ajax({
                    type: 'POST', url: '/driver_app_build', data: $('#buildForm').serialize(),
                    success: function (response) {
                        parseAction(response)
                    }
                });
                return false
            });

            let email_build_selector = $('.js-build-email');
            let build_company_selector = $('.js-build-company');
            let company_id = $('.js-company_id');

            email_build_selector.hide();
            build_company_selector.hide();
            company_id.hide();
        }
    };
    build.init();
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
