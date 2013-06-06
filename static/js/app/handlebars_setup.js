var KNET = (function (KNET, $) {

    'use strict';

    KNET.tpl = function (template, data) {
        // This will remove any top-level text nodes from rendered templates.
        // ...see http://bugs.jquery.com/ticket/12462 and https://github.com/wycats/handlebars.js/issues/162
        return $($.parseHTML(KNET.templates[template](data))).filter('*');
    };

    $(function () {
        // Handlebars.registerHelper('debug', function(optionalValue) {
        //     console.log('Current Context');
        //     console.log('====================');
        //     console.log(this);

        //     if (optionalValue) {
        //         console.log('Value');
        //         console.log('====================');
        //         console.log(optionalValue);
        //     }
        // });

        // Handlebars.registerHelper('join', function (arr, joiner) {
        //     var ret = '';
        //     for (var i = 0, j = arr.length; i < j; i++) {
        //         ret = ret + arr[i];
        //         if (i < j - 1) {
        //             ret = ret + joiner;
        //         }
        //     }
        //     return ret;
        // });

        // Handlebars.registerHelper('plural', function (arr, options) {
        //     if (arr.length === 1) {
        //         return options.inverse(this);
        //     }
        //     return options.fn(this);
        // });
    });

    return KNET;

}(KNET || {}, jQuery));
