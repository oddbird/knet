/*global QUnit:false, module:false, test:false, asyncTest:false, expect:false*/
/*global start:false, stop:false, ok:false, equal:false, notEqual:false, deepEqual:false*/
/*global notDeepEqual:false, strictEqual:false, notStrictEqual:false, raises:false*/
/*global jQuery:false*/
/*global sinon:false*/

(function ($) {

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

    module('ajaxError', {
        setup: function () {
            this.messageList = $('#messages').get(0);
            var messagesSpy = this.messagesSpy = sinon.spy();
            $.fn.messages = function () { messagesSpy($(this), arguments); };
            this.xhr = sinon.useFakeXMLHttpRequest();
            var requests = this.requests = [];
            this.xhr.onCreate = function (req) {
                requests.push(req);
            };
        },
        teardown: function () {
            this.xhr.restore();
        }
    });

    test('ajax 403 error triggers an error message', function () {
        expect(4);

        var expected = "Sorry, you don't have permission to perform this action.";
        $.ajax('/test/url/');
        this.requests[0].respond(403);

        ok(this.messagesSpy.calledOnce, 'messages() was called once');
        strictEqual(this.messagesSpy.args[0][0][0], this.messageList, 'messages() was called on #messages');
        strictEqual(this.messagesSpy.args[0][1][0], 'add', 'messages() was called with method "add"');
        deepEqual(this.messagesSpy.args[0][1][1], {tags: 'error', message: expected},
            'messages() was called with error tag and correct message text');
    });

    test('ajax 404 error triggers an error message', function () {
        expect(2);

        var expected = "Sorry, but we were unable to complete your request. Try reloading the page.";
        $.ajax('/test/url/');
        this.requests[0].respond(404);

        ok(this.messagesSpy.calledOnce, 'messages() was called once');
        deepEqual(this.messagesSpy.args[0][1][1], {tags: 'error', message: expected},
            'messages() was called with error tag and correct message text');
    });

    test('ajax 500 error triggers an error message', function () {
        expect(2);

        var expected = "Whoops! We've encountered an error, but rest assured that we're working on fixing it.";
        $.ajax('/test/url/');
        this.requests[0].respond(500);

        ok(this.messagesSpy.calledOnce, 'messages() was called once');
        deepEqual(this.messagesSpy.args[0][1][1], {tags: 'error', message: expected},
            'messages() was called with error tag and correct message text');
    });

    test('ajax error with json response triggers error msg if response.error', function () {
        expect(4);

        $.ajax('/test/url/');
        this.requests[0].respond(400, {'content-type': 'application/json'}, '{"error": "Test Error"}');

        ok(this.messagesSpy.calledOnce, 'messages() was called once');
        strictEqual(this.messagesSpy.args[0][0][0], this.messageList, 'messages() was called on #messages');
        strictEqual(this.messagesSpy.args[0][1][0], 'add', 'messages() was called with method "add"');
        deepEqual(this.messagesSpy.args[0][1][1], {tags: 'error', message: 'Test Error'},
            'messages() was called with error tag and correct message text');
    });

    test('no ajax error msg if xhr returns with error other than 403, 404, 500', function () {
        expect(1);

        $.ajax('/test/url/');
        this.requests[0].respond(400);

        ok(!this.messagesSpy.called, 'messages() was never called');
    });

}(jQuery));
