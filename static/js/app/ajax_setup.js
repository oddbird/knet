(function ($) {

    'use strict';

    $(function () {
        $.ajaxSetup({
            timeout: 30000,
            dataType: 'json'
        });

        $(document).ajaxError(function (event, request, settings, error) {
            var json, msg;

            if (request && request.status === 403) {
                msg = "Sorry, you don't have permission to perform this action.";
            }
            if (request && request.status === 404) {
                msg = "Sorry, but we were unable to complete your request. Try reloading the page.";
            }
            if (request && request.status === 500) {
                msg = "Whoops! We've encountered an error, but rest assured that we're working on fixing it.";
            }

            if (msg) {
                $('#messages').messages('add', { tags: 'error', message: msg });
            }

            try {
                json = $.parseJSON(request.responseText);
            } catch (e) {
                json = false;
            }

            if (json && json.error) {
                $('#messages').messages('add', {message: json.error, tags: 'error'});
            }
        });
    });

}(jQuery));
