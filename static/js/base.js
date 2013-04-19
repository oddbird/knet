var KNET = (function (KNET, $) {

    'use strict';

    var teacherNameInput = $('#teacher-name');
    var teacherNameButton = $('.teacher-login-content .next-button');
    var teacherName = $('header .meta .teacher span');
    var learnerName = $('header .meta .learner span');
    var timer = $('.learning-session-content .timer');
    var timerStart = $('label[for="learning-session-toggle"]');
    var timerStop = $('label[for="results-toggle"]');

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
        timerStart.one('click', function () {
            timer.stopwatch().stopwatch('start');
        });
        timerStop.one('click', function () {
            timer.stopwatch('stop');
        });
    };

    $(function () {
        KNET.inputTeacherName();
        KNET.initializeTimer();
    });

    return KNET;

}(KNET || {}, jQuery));
