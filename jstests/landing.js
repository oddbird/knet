/*global QUnit:false, module:false, test:false, asyncTest:false, expect:false*/
/*global start:false, stop:false, ok:false, equal:false, notEqual:false, deepEqual:false*/
/*global notDeepEqual:false, strictEqual:false, notStrictEqual:false, raises:false*/
/*global jQuery:false*/
/*global sinon:false*/
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

    module('landingForm', {
        setup: function () {
            this.container = $('#qunit-fixture');
            this.formSel = '.test-form';
            this.messageListSel = '#test-messages';
            this.messageList = this.container.find(this.messageListSel);
            this.form = this.container.find(this.formSel);
            this.input = this.form.find('.test-email');
            this.xhr = sinon.useFakeXMLHttpRequest();
            var requests = this.requests = [];
            this.xhr.onCreate = function (req) {
                requests.push(req);
            };
            KNET.landingForm(this.formSel, this.messageListSel);
        },
        teardown: function () {
            this.xhr.restore();
        }
    });

    test('form submits via ajax', function () {
        expect(3);

        this.input.val('test@test.test');
        this.form.trigger('submit');

        strictEqual(this.requests.length, 1, 'one xhr request was sent');
        strictEqual(this.requests[0].method, 'POST', 'xhr was sent with method POST');
        strictEqual(this.requests[0].requestBody, 'test-email=test%40test.test', 'xhr was sent with input value in requestBody');
    });

    test('form is reset after being submitted', function () {
        expect(2);

        this.input.val('test@test.test');

        strictEqual(this.input.val(), 'test@test.test', 'form input has val');

        this.form.trigger('submit');
        this.requests[0].respond(200);

        strictEqual(this.input.val(), '', 'form input val is reset');
    });

    test('messages are removed when form is submitted', function () {
        expect(2);

        $('<li class="message" />').appendTo(this.messageList);

        strictEqual(this.messageList.children().length, 1, 'one message exists');

        this.form.trigger('submit');

        strictEqual(this.messageList.children().length, 0, 'message is cleared on form submit');
    });

}(KNET, jQuery));
