

(function ($) {
    let build = {
        appForm: '#buildForm',
        init: function () {
            this.registerFormSubmitEvent();
        },
        registerFormSubmitEvent() {
            $(this.appForm).on('submit', function () {
                $.ajax({
                    type: 'POST', url: '/app_build', data: $('#buildForm').serialize(),
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


$("input[name=build_type]").on('click', function () {
    let platform = $(this).val();
    onUpdatePlatform(platform);
});


function onUpdatePlatform(platform) {
    console.log("init platform " + platform);
    let email_build_selector = $('.js-build-email');
    let build_company_selector = $('.js-build-company');
    let company_id = $('.js-company_id');
    switch (platform) {
        case "android":
            let is_android_existing = getCookie("is_android_existing");
            platformChange(is_android_existing);
            email_build_selector.hide();
            build_company_selector.hide();
            company_id.hide();
            break;
        case "ios":
            let is_ios_existing = getCookie("is_ios_existing");
            platformChange(is_ios_existing);
            email_build_selector.show();
            build_company_selector.show();
            company_id.show();
            break;
        default:
            console.log("Unknown type");
            break;
    }
}


function platformChange(is_platform_existing) {
    console.log("platformChange " + is_platform_existing);
    if (is_platform_existing === "False") {
        $('.js-configure-project')
            .prop("checked", true)
            .prop("disabled", true);
        $('.js-configure-project-hidden').val("true")
    } else {
        $('.js-configure-project')
            .prop("disabled", false);
        $('.js-configure-project-hidden').val("false")
    }
}


function getCookie(key) {
    let name = key + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1);
        if (c.indexOf(name) !== -1) return c.substring(name.length, c.length);
    }
    return ""
}