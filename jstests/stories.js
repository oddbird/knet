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

    module('ajaxStoryActions', {
        setup: function () {
            this.containerSel = '#qunit-fixture';
            this.container = $(this.containerSel);
            this.buttonSel = '.test-trigger';
            this.button = $('<button name="test-key" value="test-val" class="test-trigger">Test Button</button>');
            this.container.find('form').append(this.button);
            this.xhr = sinon.useFakeXMLHttpRequest();
            var requests = this.requests = [];
            this.xhr.onCreate = function (req) {
                requests.push(req);
            };
        },
        teardown: function () {
            this.xhr.restore();
            this.container.off('click');
        }
    });

    test('form submits via ajax', function () {
        expect(3);

        KNET.ajaxStoryActions(this.buttonSel, this.containerSel);
        this.button.click();

        strictEqual(this.requests.length, 1, 'one xhr request was sent');
        strictEqual(this.requests[0].method, 'POST', 'xhr was sent with method POST');
        strictEqual(this.requests[0].requestBody, 'test-key=test-val', 'xhr was sent with button value in requestBody');
    });

    test('callback is called when request returns successfully', function () {
        expect(3);

        var callbackSpy = this.spy();
        KNET.ajaxStoryActions(this.buttonSel, this.containerSel, callbackSpy);
        this.button.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        ok(callbackSpy.calledOnce, 'callbackSpy() was called once');
        ok(callbackSpy.calledWith({success: true}), 'callbackSpy() is passed the xhr response');
        strictEqual(callbackSpy.args[0][1].get(0), this.button.closest('form').get(0), 'callbackSpy() is passed the form');
    });

    test('callback is not called if xhr request returns without success: true', function () {
        expect(1);

        var callbackSpy = this.spy();
        KNET.ajaxStoryActions(this.buttonSel, this.containerSel, callbackSpy);
        this.button.click();
        this.requests[0].respond(200);

        ok(!callbackSpy.called, 'callbackSpy() was not called');
    });

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
            this.container.off('click');
        }
    });

    test('story is removed after form is successfully submitted', function () {
        expect(2);

        KNET.removeStory(this.removeButtonSel, this.containerSel);

        strictEqual(this.container.children().length, 1, 'one story exists');

        this.removeButton.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        strictEqual(this.container.children().length, 0, 'no stories exist');
    });

    module('changeStoryStatus', {
        setup: function () {
            this.containerSel = '#qunit-fixture';
            this.container = $(this.containerSel);
            this.statusButtonSel = '.story-status';
            this.statusButton = this.container.find(this.statusButtonSel);
            this.xhr = sinon.useFakeXMLHttpRequest();
            var requests = this.requests = [];
            this.xhr.onCreate = function (req) {
                requests.push(req);
            };
        },
        teardown: function () {
            this.xhr.restore();
            this.container.off('click');
        }
    });

    test('story is replaced after form is successfully submitted', function () {
        expect(1);

        var responseHTML = '<div>New Test Story</div>';
        KNET.changeStoryStatus(this.statusButtonSel, this.containerSel);
        this.statusButton.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true, "html": "' + responseHTML + '"}');

        strictEqual(this.container.html().trim(), responseHTML, 'story has been replaced by response.html');
    });

    test('story is not replaced if xhr request returns without response.html', function () {
        expect(1);

        var html = this.container.html();
        KNET.changeStoryStatus(this.statusButtonSel, this.containerSel);
        this.statusButton.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        strictEqual(this.container.html(), html, 'story html has not changed');
    });

}(KNET, jQuery));
