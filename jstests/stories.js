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

    module('removeStory', {
        setup: function () {
            this.containerSel = '#qunit-fixture';
            this.container = $(this.containerSel);
            this.removeButtonSel = '.delete-story';
            this.removeButton = this.container.find(this.removeButtonSel);
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

    test('form submits via ajax', function () {
        expect(3);

        KNET.removeStory(this.removeButtonSel, this.containerSel);
        this.removeButton.click();

        strictEqual(this.requests.length, 1, 'one xhr request was sent');
        strictEqual(this.requests[0].method, 'POST', 'xhr was sent with method POST');
        strictEqual(this.requests[0].requestBody, 'delete-story=1', 'xhr was sent with button value in requestBody');
    });

    test('story is removed after form is successfully submitted', function () {
        expect(2);

        KNET.removeStory(this.removeButtonSel, this.containerSel);

        strictEqual(this.container.children().length, 1);

        this.removeButton.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        strictEqual(this.container.children().length, 0);
    });

    test('story is not removed if xhr request returns without success: true', function () {
        expect(2);

        KNET.removeStory(this.removeButtonSel, this.containerSel);

        strictEqual(this.container.children().length, 1);

        this.removeButton.click();
        this.requests[0].respond(200);

        strictEqual(this.container.children().length, 1);
    });

}(KNET, jQuery));
