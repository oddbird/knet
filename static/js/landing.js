var KNET = (function (KNET, $) {

    'use strict';

    KNET.landingForm = function (formSel) {
        var form = $(formSel);
        if (form.length) {
            form.ajaxForm({
                resetForm: true
                // success: function (response, status, xhr, form) {
                //     // console.log('success');
                // },
                // target: form,
                // replaceTarget: true
            });
        }
    };

    return KNET;

}(KNET || {}, jQuery));
