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
            this.containerSel = '.teacher-stories';
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

    test('loadingOverlay is added before form submission', function () {
        expect(1);

        var story = this.button.closest('.story');
        KNET.ajaxStoryActions(this.buttonSel, this.containerSel);
        this.button.click();

        ok(story.hasClass('loading'), 'story has loadingOverlay');
    });

    test('loadingOverlay is removed on xhr success', function () {
        expect(2);

        var story = this.button.closest('.story');
        KNET.ajaxStoryActions(this.buttonSel, this.containerSel);
        this.button.click();

        ok(story.hasClass('loading'), 'story has loadingOverlay');

        this.requests[0].respond(200);

        ok(!story.hasClass('loading'), 'story does not have loadingOverlay');
    });

    test('loadingOverlay is removed on xhr error', function () {
        expect(2);

        var story = this.button.closest('.story');
        KNET.ajaxStoryActions(this.buttonSel, this.containerSel);
        this.button.click();

        ok(story.hasClass('loading'), 'story has loadingOverlay');

        this.requests[0].respond(404);

        ok(!story.hasClass('loading'), 'story does not have loadingOverlay');
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
            this.containerSel = '.teacher-stories';
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

        $.fx.off = true;
        KNET.removeStory(this.removeButtonSel, this.containerSel);

        strictEqual(this.container.children('.story').length, 1, 'one story exists');

        this.removeButton.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        strictEqual(this.container.children('.story').length, 0, 'no stories exist');

        $.fx.off = false;
    });

    test('updateNoStoriesMsg() is called after form is successfully submitted', function () {
        expect(2);

        $.fx.off = true;
        this.stub(KNET, 'updateNoStoriesMsg');
        KNET.removeStory(this.removeButtonSel, this.containerSel);
        this.removeButton.click();
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        ok(KNET.updateNoStoriesMsg.calledOnce, 'updateNoStoriesMsg() was called once');
        ok(KNET.updateNoStoriesMsg.calledWith('.story', '.no-stories-message', this.containerSel),
            'updateNoStoriesMsg() was called with correct args');

        $.fx.off = false;
    });

    module('changeStoryStatus', {
        setup: function () {
            this.containerSel = '.teacher-stories';
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

    module('addStory', {
        setup: function () {
            this.containerSel = '.add-story';
            this.container = $(this.containerSel);
            this.formSel = '.add-story-form';
            this.form = this.container.find(this.formSel);
            this.formToggleSel = '#story-form-toggle';
            this.formToggle = this.container.find(this.formToggleSel);
            this.bodyInput = this.form.find('#id_body');
            this.privateInput = this.form.find('#id_private');
            this.storiesContainerSel = '.teacher-stories';
            this.storiesContainer = $(this.storiesContainerSel);
            this.xhr = sinon.useFakeXMLHttpRequest();
            var requests = this.requests = [];
            this.xhr.onCreate = function (req) {
                requests.push(req);
            };
            KNET.addStory(this.storiesContainerSel, this.formSel, this.formToggleSel);
        },
        teardown: function () {
            this.xhr.restore();
        }
    });

    test('form submits via ajax', function () {
        expect(3);

        var expected = 'body=Test+Story&private=on';
        this.bodyInput.val('Test Story');
        this.privateInput.prop('checked', true);
        this.form.trigger('submit');

        strictEqual(this.requests.length, 1, 'one xhr request was sent');
        strictEqual(this.requests[0].method, 'POST', 'xhr was sent with method POST');
        strictEqual(this.requests[0].requestBody, expected, 'xhr is sent with serialized form data');
    });

    test('story is added after form is successfully submitted', function () {
        expect(2);

        this.bodyInput.val('New Test Story');
        this.form.trigger('submit');
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true, "html": "<article class=\\"story new\\">New Test Story</article>"}');

        strictEqual(this.storiesContainer.children('.story').length, 2, 'now we have two stories');
        ok(this.storiesContainer.children('.story').eq(0).hasClass('new'), 'story from response.html has been prepended to stories list');
    });

    test('loadingOverlay is added before form submission', function () {
        expect(1);

        this.form.trigger('submit');

        ok(this.form.hasClass('loading'), 'form has loadingOverlay');
    });

    test('loadingOverlay is removed on xhr success', function () {
        expect(2);

        this.form.trigger('submit');

        ok(this.form.hasClass('loading'), 'form has loadingOverlay');

        this.requests[0].respond(200);

        ok(!this.form.hasClass('loading'), 'form does not have loadingOverlay');
    });

    test('loadingOverlay is removed on xhr error', function () {
        expect(2);

        this.form.trigger('submit');

        ok(this.form.hasClass('loading'), 'form has loadingOverlay');

        this.requests[0].respond(404);

        ok(!this.form.hasClass('loading'), 'form does not have loadingOverlay');
    });

    test('form is reset when submitted successfully', function () {
        expect(2);

        this.bodyInput.val('Test Story');
        this.privateInput.prop('checked', true);
        this.form.trigger('submit');
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        strictEqual(this.bodyInput.val(), '', 'Body has been reset.');
        strictEqual(this.privateInput.prop('checked'), false, 'Private checkbox has been reset.');
    });

    test('form is not reset if xhr request returns without success: true', function () {
        expect(2);

        this.bodyInput.val('Test Story');
        this.privateInput.prop('checked', true);
        this.form.trigger('submit');
        this.requests[0].respond(200);

        strictEqual(this.bodyInput.val(), 'Test Story', 'Body has not been reset.');
        strictEqual(this.privateInput.prop('checked'), true, 'Private checkbox has not been reset.');
    });

    test('form is hidden when submitted successfully', function () {
        expect(1);

        this.formToggle.prop('checked', false);
        this.bodyInput.val('Test Story');
        this.form.trigger('submit');
        this.requests[0].respond(200, {'content-type': 'application/json'}, '{"success": true}');

        ok(this.formToggle.prop('checked'), 'form is hidden');
    });

    test('form is not hidden if xhr request returns without success: true', function () {
        expect(1);

        this.formToggle.prop('checked', false);
        this.bodyInput.val('Test Story');
        this.form.trigger('submit');
        this.requests[0].respond(200);

        ok(!this.formToggle.prop('checked'), 'form is still open');
    });

    module('updateNoStoriesMsg', {
        setup: function () {
            this.containerSel = '.teacher-stories';
            this.container = $(this.containerSel);
            this.storySel = '.story';
            this.msgSel = '.no-stories-message';
        },
        teardown: function () {
        }
    });

    test('"no stories" msg is added if no stories exist, viewing your own profile', function () {
        expect(1);

        this.container.empty();
        this.container.data({
            'teacher': 1,
            'user': 1
        });
        KNET.updateNoStoriesMsg(this.storySel, this.msgSel, this.containerSel);

        strictEqual(this.container.html(), KNET.tpl('no_stories_msg', {my_profile: true}).get(0).outerHTML, '"no stories" msg exists');
    });

    test('"be the first to leave a story" msg is added if no stories exist, viewing someone else\'s profile', function () {
        expect(1);

        this.container.empty();
        this.container.data({
            'teacher': 1,
            'user': 2,
            'teacher-name': 'tester'
        });
        var data = {
            'my_profile': false,
            'teacher_name': 'tester'
        };
        KNET.updateNoStoriesMsg(this.storySel, this.msgSel, this.containerSel);

        strictEqual(this.container.html(), KNET.tpl('no_stories_msg', data).get(0).outerHTML, '"be the first to leave a story" msg exists');
    });

    test('"no stories" msg is removed if stories exist', function () {
        expect(2);

        var msg = KNET.tpl('no_stories_msg', {});
        this.container.append(msg);

        ok(this.container.find(this.msgSel).length, '"no stories" msg exists');

        KNET.updateNoStoriesMsg(this.storySel, this.msgSel, this.containerSel);

        ok(!this.container.find(this.msgSel).length, '"no stories" msg has been removed');
    });

}(KNET, jQuery));
