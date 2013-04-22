var KNET = (function (KNET, $) {

    'use strict';

    var container = $('.demo');

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

    KNET.inputTeacherName = function () {
        var teacherNameInput = $('#teacher-name');
        var teacherNameButton = container.find('label[for="learner-login-toggle"]');
        var teacherName = $('header .meta .teacher span');
        var learnerName = $('header .meta .learner span');
        var addTeacherName = function () {
            if (teacherNameInput.val() !== '') {
                var name = teacherNameInput.val().toString();
                teacherName.text(name).closest('.vcard').removeClass('empty');
                teacherNameInput.val('');
            }
        };

        teacherNameInput.keydown(function (e) {
            if (e.keyCode === KNET.keycodes.ENTER) {
                teacherNameButton.first().click();
            }
        });

        teacherNameButton.click(function (e) {
            addTeacherName();
        });
    };

    KNET.initializeTimer = function () {
        var timer = container.find('.learning-session-content .timer');
        var timerStartSel = 'label[for="learning-session-toggle"]';
        var timerStopSel = 'label[for="results-toggle"]';

        container.one('click', timerStartSel, function () {
            timer.stopwatch().stopwatch('start');
        });
        container.one('click', timerStopSel, function () {
            timer.stopwatch('stop');
        });
    };

    KNET.initFeedbackButtons = function () {
        var feedbackButtons = container.find('.feedback-item button');

        feedbackButtons.each(function () {
            var button = $(this);
            var counter = button.siblings('span');

            button.on('click.feedback', function () {
                var count = parseInt(counter.text(), 10) + 1;
                counter.text('+' + count);
                if (count === 5) {
                    button.off('click.countdown');
                    button.attr('disabled', 'disabled');
                }
            });
        });
    };

    KNET.selectTopic = function () {
        var topicSel = 'input[type="radio"][name="select-topic"]';
        var topicInputs = container.find(topicSel);
        var targets = container.find('.selected-topic');
        var updateTopic = function () {
            var text = topicInputs.filter(':checked').siblings('label').find('.topic').text();
            targets.text(text);
        };

        container.on('change', topicSel, function () {
            updateTopic();
        });

        updateTopic();
    };

    $(function () {
        KNET.inputTeacherName();
        KNET.initializeTimer();
        KNET.initFeedbackButtons();
        KNET.selectTopic();
    });

    return KNET;

}(KNET || {}, jQuery));
