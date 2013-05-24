var KNET = (function (KNET, $) {

    'use strict';

    $(function () {
        // plugins
        $('#messages').messages({
            handleAjax: true,
            transientDelay: 5000
        });

        // demo/demo.js
        if ($('.demo').length) {
            KNET.inputTeacherName();
            KNET.selectLearnerName();
            KNET.initializeTimer();
            KNET.initFeedbackButtons();
            KNET.selectTopic();
        }

        // landing.js
        KNET.landingForm('form.signup');
        KNET.clearOnFormSubmit('form.signup', '#messages');
    });

    return KNET;

}(KNET || {}, jQuery));
