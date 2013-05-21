var KNET = (function (KNET, $) {

    'use strict';

    var container = $('.demo');

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
            var counter = button.siblings('.count');
            var id = button.data('id');
            var results = container.find('.results-table.soft .' + id);

            button.on('click.feedback', function () {
                var count = parseInt(counter.text(), 10) + 1;
                counter.text('+' + count);
                results.text('+' + count);
                if (count === 5) {
                    button.off('click.feedback');
                    button.attr('disabled', 'disabled');
                }
            });
        });
    };

    KNET.selectTopic = function () {
        var topicSel = 'input[type="radio"][name="select-topic"]';
        var topicInputs = container.find(topicSel);
        var targets = container.find('.selected-topic');
        var resultsTopics = container.find('.results-table.hard tr');
        var updateTopic = function () {
            var selectedTopic = topicInputs.filter(':checked');
            if (selectedTopic.length) {
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
            }
        };

        container.on('change', topicSel, function () {
            updateTopic();
        });

        updateTopic();
    };

    return KNET;

}(KNET || {}, jQuery));
