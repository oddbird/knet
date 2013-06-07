/**
 * jQuery Ajax Loading Overlay 0.1.2
 *
 * Copyright (c) 2012, Jonny Gerig Meyer
 * All rights reserved.
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */

/*jslint    browser:    true,
            indent:     4 */
/*global    jQuery */

(function ($) {

    'use strict';

    var methods = {
        init: function (opts) {
            var options = $.extend({}, $.fn.loadingOverlay.defaults, opts);
            var target = $(this).addClass(options.loadingClass);
            var overlay = '<div class="' + options.overlayClass + '"><p class="' + options.spinnerClass + '">' + options.loadingText + '</p></div>';
            target.prepend($(overlay));
        },

        remove: function (opts) {
            var options = $.extend({}, $.fn.loadingOverlay.defaults, opts);
            var target = $(this);
            target.find('.' + options.overlayClass).detach();
            if (target.hasClass(options.loadingClass)) {
                target.removeClass(options.loadingClass);
            } else {
                target.find('.' + options.loadingClass).removeClass(options.loadingClass);
            }
        }
    };

    $.fn.loadingOverlay = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.ajax-loading-overlay');
        }
    };

    /* Setup plugin defaults */
    $.fn.loadingOverlay.defaults = {
        loadingClass: 'loading',            // Class added to `target` while loading
        overlayClass: 'loading-overlay',    // Class added to loading overlay (to be styled in CSS)
        spinnerClass: 'loading-spinner',    // Class added to loading overlay spinner
        loadingText: 'loading'              // Text within loading overlay
    };

}(jQuery));
