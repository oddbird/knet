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
        var headerTeacherName = $('header .meta .teacher-name');
        var profileTeacherName = container.find('.teacher-name');
        var addTeacherName = function () {
            if (teacherNameInput.val() !== '') {
                var name = teacherNameInput.val().toString();
                headerTeacherName.text(name).closest('.vcard').removeClass('empty');
                profileTeacherName.text(name);
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

    KNET.selectLearnerName = function () {
        var labelSel = 'label[for="topic-select-toggle"]';
        var headerLearnerName = $('header .meta .learner-name');
        var profileLearnerName = container.find('.learner-name');

        container.one('click', labelSel, function () {
            headerLearnerName.text('Peter K').closest('.vcard').removeClass('empty');
            profileLearnerName.text('Peter K');
        });
    };

    KNET.initializeTimer = function () {
        var timer = container.find('.learning-session-content .timer');
        var timerStartSel = 'label[for="learning-session-toggle"]';
        var timerStopSel = 'label[for="results-toggle"]';
        var sessionTime = container.find('.session-time');
        var addStopHandler = function () {
            container.one('click', timerStopSel, function () {
                timer.stopwatch('stop');
                sessionTime.text(timer.text());
            });
        };

        container.one('click', timerStartSel, function () {
            timer.stopwatch().stopwatch('start');
            addStopHandler();
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
        var resultsTopics = container.find('.results-table tr');
        var updateTopic = function () {
            var selectedTopic = topicInputs.filter(':checked');
            var id = selectedTopic.get(0).id;
            var text = container.find('label[for="' + id + '"]').find('.topic').text();
            var thisResult = resultsTopics.removeClass('yay').filter(function () {
                return $(this).data('id') === id;
            }).addClass('yay');
            targets.text(text);
            resultsTopics.find('.after').each(function () {
                var el = $(this);
                el.text(el.data('orig'));
            });
            var count = parseInt(thisResult.find('.after').text(), 10);
            thisResult.find('.after').text(++count);
        };

        container.on('change', topicSel, function () {
            updateTopic();
        });

        updateTopic();
    };

    $(function () {
        KNET.inputTeacherName();
        KNET.selectLearnerName();
        KNET.initializeTimer();
        KNET.initFeedbackButtons();
        KNET.selectTopic();
    });

    return KNET;

}(KNET || {}, jQuery));
