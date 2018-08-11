/**
 * Created by santa on 06.07.17.
 */

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


    /*let update = {
     appForm: '#updateApplication',
     init: function () {
     this.registerFormSubmitEvent();
     },
     registerFormSubmitEvent() {
     $(this.appForm).on('submit', function () {
     $.ajax({
     type: 'POST', url: '/app_update', data: $('#updateApplication').serialize(),
     success: function (response) {
     console.log(response);
     $('#buildDialog').modal('hide');
     parseAction(response)
     }
     });
     return false
     });
     }
     };*/