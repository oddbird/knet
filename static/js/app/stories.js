var KNET = (function (KNET, $) {

    'use strict';

    KNET.ajaxStoryActions = function (triggerSel, containerSel, callback) {
        var container = $(containerSel);
        container.on('click', triggerSel, function (e) {
            e.preventDefault();
            var button = $(this);
            var form = button.closest('form');
            var story = button.closest('.story');
            var data = {};
            data[button.attr('name')] = button.val().toString();
            story.loadingOverlay();
            form.ajaxSubmit({
                data: data,
                success: function (response, status, xhr, form) {
                    story.loadingOverlay('remove');
                    if (response && response.success) {
                        callback(response, form);
                    }
                },
                error: function () {
                    story.loadingOverlay('remove');
                }
            });
        });
    };

    KNET.removeStory = function (triggerSel, containerSel) {
        var callback = function (response, form) {
            var story = form.closest('.story');
            var container = $(containerSel);
            $.when(story.fadeOut()).done(function () {
                story.remove();
                KNET.updateNoStoriesMsg('.story', '.no-stories-message', containerSel);
            });
        };
        KNET.ajaxStoryActions(triggerSel, containerSel, callback);
    };

    KNET.changeStoryStatus = function (triggerSel, containerSel) {
        var callback = function (response, form) {
            if (response.html && response.html.length) {
                var newStory = $.parseHTML(response.html);
                form.closest('.story').replaceWith(newStory);
            }
        };
        KNET.ajaxStoryActions(triggerSel, containerSel, callback);
    };

    KNET.addStory = function (formSel, formToggleSel) {
        var form = $(formSel);
        form.ajaxForm({
            beforeSubmit: function () {
                form.loadingOverlay();
            },
            success: function (response) {
                form.loadingOverlay('remove');
                if (response && response.success) {
                    form.get(0).reset();
                    $(formToggleSel).prop('checked', true);
                }
            },
            error: function () {
                form.loadingOverlay('remove');
            }
        });
    };

    KNET.updateNoStoriesMsg = function (storySel, msgSel, containerSel) {
        var container = $(containerSel);
        if (container.children(storySel).length) {
            container.find(msgSel).remove();
        } else {
            var teacher = container.data('teacher');
            var teacherName = container.data('teacher-name');
            var user = container.data('user');
            var url = container.data('url');
            var data = {
                my_profile: teacher === user,
                teacher_name: teacherName,
                profile_url: url
            };
            var noStoriesMsg = KNET.tpl('no_stories_msg', data);
            container.html(noStoriesMsg);
        }
    };

    return KNET;

}(KNET || {}, jQuery));
