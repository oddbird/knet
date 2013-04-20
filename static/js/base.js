var KNET = (function (KNET, $) {

    'use strict';

    var container = $('.demo');
    var teacherNameInput = $('#teacher-name');
    var teacherNameButton = container.find('.teacher-login-content .next-button');
    var teacherName = $('header .meta .teacher span');
    var learnerName = $('header .meta .learner span');
    var timer = container.find('.learning-session-content .timer');
    var timerStartSel = 'label[for="learning-session-toggle"]';
    var timerStopSel = 'label[for="results-toggle"]';
    var feedbackButtons = container.find('.feedback-item button');

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
        var addTeacherName = function () {
            if (teacherNameInput.val() !== '') {
                var name = teacherNameInput.val().toString();
                teacherName.text(name).closest('.vcard').removeClass('empty');
                teacherNameInput.val('');
            }
        };

        teacherNameInput.keydown(function (e) {
            if (e.keyCode === KNET.keycodes.ENTER) {
                addTeacherName();
            }
        });

        teacherNameButton.click(function (e) {
            addTeacherName();
        });
    };

    KNET.initializeTimer = function () {
        container.one('click', timerStartSel, function () {
            timer.stopwatch().stopwatch('start');
        });
        container.one('click', timerStopSel, function () {
            timer.stopwatch('stop');
        });
    };

    KNET.initFeedbackButtons = function () {
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

    $(function () {
        KNET.inputTeacherName();
        KNET.initializeTimer();
        KNET.initFeedbackButtons();
    });

    return KNET;

}(KNET || {}, jQuery));
