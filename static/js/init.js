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
        $('.email').defuscate();

        // stories.js
        KNET.removeStory('.story .story-actions .delete-story', '.teacher-stories');
        KNET.changeStoryStatus('.story .story-actions .story-status', '.teacher-stories');
        KNET.addStory('.teacher-stories', '.add-story-form', '#story-form-toggle');
        KNET.updateNoStoriesMsg('.story', '.no-stories-message', '.teacher-stories');
    });

    return KNET;

}(KNET || {}, jQuery));
