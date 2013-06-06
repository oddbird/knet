var KNET = (function (KNET, $) {

    'use strict';

    KNET.ajaxStoryActions = function (triggerSel, containerSel, callback) {
        var container = $(containerSel);
        container.on('click', triggerSel, function (e) {
            e.preventDefault();
            var button = $(this);
            var form = button.closest('form');
            var data = {};
            data[button.attr('name')] = button.val().toString();
            form.ajaxSubmit({
                data: data,
                success: function (response, status, xhr, form) {
                    if (response && response.success) {
                        callback(response, form);
                    }
                }
            });
        });
    };

    KNET.removeStory = function (triggerSel, containerSel) {
        var callback = function (response, form) {
            form.closest('.story').remove();
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

    return KNET;

}(KNET || {}, jQuery));
