var KNET = (function (KNET, $) {

    'use strict';

    $(function () {
        // plugins
        $('#messages').messages({
            handleAjax: true,
            transientDelay: 5000,
            closeCallback: function (el) {
                el.addClass('closed');
                $.doTimeout(800, function () { el.remove(); });
            },
            transientCallback: function (el) {
                el.addClass('closed-timeout');
                $.doTimeout(800, function () { el.remove(); });
            }
        });

        // demo.js
        if ($('.demo').length) {
            KNET.inputTeacherName();
            KNET.selectLearnerName();
            KNET.initializeTimer();
            KNET.initFeedbackButtons();
            KNET.selectTopic();
        }

        // landing.js
        KNET.landingForm('form.signup', '#messages');

        // stories.js
        KNET.removeStory('.story .story-actions .delete-story', '.teacher-detail');
    });

    return KNET;

}(KNET || {}, jQuery));
