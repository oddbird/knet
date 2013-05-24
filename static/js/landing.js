var KNET = (function (KNET, $) {

    'use strict';

    KNET.landingForm = function (formSel) {
        var form = $(formSel);
        if (form.length) {
            form.ajaxForm({resetForm: true});
        }
    };

    KNET.clearOnFormSubmit = function (formSel, messagesSel) {
        var form = $(formSel);
        var messages = $(messagesSel);

        form.on('submit', function () {
            messages.empty();
            return true;
        });
    };

    return KNET;

}(KNET || {}, jQuery));
