/*global QUnit:false, module:false, test:false, asyncTest:false, expect:false*/
/*global start:false, stop:false, ok:false, equal:false, notEqual:false, deepEqual:false*/
/*global notDeepEqual:false, strictEqual:false, notStrictEqual:false, raises:false*/
/*global jQuery:false*/
/*global KNET:false*/

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

    module('landing', {
        setup: function () {
            this.container = $('#qunit-fixture');
            this.messages = $('<ul id="messages" />').appendTo(this.container);
            this.messageSel = '#messages';
            this.form = $('<form class="lead-form"></form>').appendTo(this.container);
            this.formSel = '.lead-form';
            this.button = $('<button type="submit"></button>').appendTo(this.form);
        },
        teardown: function () {
            this.container.empty().off('click change');
        }
    });

    test('messages are removed when form is submitted', function () {
        expect(1);

        $('<li class="message" />').appendTo(this.messages);
        KNET.clearOnFormSubmit(this.formSel, this.messageSel);
        this.button.trigger('click');

        strictEqual(this.messages.children().length, 0, 'messages cleared on form submit');
    });

}(KNET, jQuery));
