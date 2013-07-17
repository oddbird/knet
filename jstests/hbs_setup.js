/*global QUnit:false, module:false, test:false, asyncTest:false, expect:false*/
/*global start:false, stop:false, ok:false, equal:false, notEqual:false, deepEqual:false*/
/*global notDeepEqual:false, strictEqual:false, notStrictEqual:false, raises:false*/
/*global jQuery:false*/
/*global sinon:false*/

(function (KNET, $) {

    'use strict';

    /*
    ======== A Handy Little QUnit Reference ========
    http://docs.jquery.com/QUnit

    Test methods:
        expect(numAssertions)
        stop(increment)
        start(decrement)
    Test assertions:
        ok(value, [message])
        equal(actual, expected, [message])
        notEqual(actual, expected, [message])
        deepEqual(actual, expected, [message])
        notDeepEqual(actual, expected, [message])
        strictEqual(actual, expected, [message])
        notStrictEqual(actual, expected, [message])
        raises(block, [expected], [message])
    */

    module('tpl', {
        setup: function () {
            KNET.templates = KNET.templates || {};
            KNET.templates.test_tpl = Handlebars.compile('<div>Test Template</div>');
            KNET.templates.test_tpl2 = Handlebars.compile('<div>{{text}}</div>');
        }
    });

    test('returns template as jQuery object', function () {
        expect(1);

        var expected = '<div>Test Template</div>';
        var actual = KNET.tpl('test_tpl').get(0).outerHTML;

        strictEqual(actual, expected, 'hbs template is returned rendered as jQuery object');
    });

    test('renders data passed to template', function () {
        expect(1);

        var expected = '<div>Another Test Template</div>';
        var actual = KNET.tpl('test_tpl2', {text: 'Another Test Template'}).get(0).outerHTML;

        strictEqual(actual, expected, 'hbs template is returned with data rendered');
    });

}(KNET, jQuery));
