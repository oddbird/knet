var KNET = (function (KNET, $) {

    'use strict';

    $(function () {
        // demo.js
        if ($('.demo').length) {
            KNET.inputTeacherName();
            KNET.selectLearnerName();
            KNET.initializeTimer();
            KNET.initFeedbackButtons();
            KNET.selectTopic();
        }
    });

    return KNET;

}(KNET || {}, jQuery));
