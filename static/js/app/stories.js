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
                if (!container.children('.story').length) {
                    var noStoriesMsg = KNET.tpl('no_stories_msg');
                    container.html(noStoriesMsg);
                }
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
            }
        });
    };

    return KNET;

}(KNET || {}, jQuery));
