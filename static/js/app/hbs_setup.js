var KNET = (function (KNET, $) {

    'use strict';

    KNET.tpl = function (template, data) {
        // This will remove any top-level text nodes from rendered templates.
        // ...see http://bugs.jquery.com/ticket/12462 and https://github.com/wycats/handlebars.js/issues/162
        return $($.parseHTML(KNET.templates[template](data))).filter('*');
    };

    return KNET;

}(KNET || {}, jQuery));
