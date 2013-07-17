var KNET = (function (KNET, $) {

    'use strict';

    KNET.landingForm = function (formSel, messagesSel) {
        var form = $(formSel);
        var messages = $(messagesSel);
        form.ajaxForm({
            beforeSubmit: function () {
                messages.empty();
            },
            resetForm: true
        });
    };

    return KNET;

}(KNET || {}, jQuery));
