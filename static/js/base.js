var KNET = (function (KNET, $) {

    'use strict';

    // Store keycode variables for easier readability
    KNET.keycodes = {
        SPACE: 32,
        ENTER: 13,
        TAB: 9,
        ESC: 27,
        BACKSPACE: 8,
        SHIFT: 16,
        CTRL: 17,
        ALT: 18,
        CAPS: 20,
        LEFT: 37,
        UP: 38,
        RIGHT: 39,
        DOWN: 40
    };

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
