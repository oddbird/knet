from django.core.urlresolvers import reverse
import pytest

from knet.teachers.models import Story

from ..factories import UserFactory
from ..utils import redirects_to, is_deleted, refresh
from .factories import TeacherProfileFactory, StoryFactory



class TestTeacherDetail:
    def test_submit_story_authenticated(self, client):
        """Authenticated user can submit a story on a teacher's profile page."""
        user = UserFactory.create()
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        form = client.get(url, user=user).forms['add-story-form']
        form['body'] = "It was a dark and stormy night."
        resp = form.submit()

        assert resp.status_code == 302, resp
        assert redirects_to(resp) == url
        s = Story.objects.get()
        assert s.body == "It was a dark and stormy night."
        assert s.submitter == user


    def test_cant_submit_story_anonymously(self, client):
        """No form to submit a story anonymously."""
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        resp = client.get(url)

        assert len(resp.html.find_all('form', 'add-story-form')) == 0


    def test_submit_story_requires_body(self, client):
        """Can't submit a story without a... story."""
        user = UserFactory.create()
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        form = client.get(url, user=user).forms['add-story-form']
        resp = form.submit()

        assert resp.status_code == 200
        assert Story.objects.count() == 0
        resp.mustcontain("left your story blank")


    def test_submit_story_to_own_profile(self, client):
        """Can submit a story to own profile with overridden name/date."""
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        form = client.get(url, user=profile.user).forms['add-story-form']
        form['body'] = "It was a dark and stormy night."
        form['submitter_name'] = "Somebody"
        form['nominal_date'] = "3/21/2013"
        resp = form.submit()

        assert resp.status_code == 302, resp
        assert redirects_to(resp) == url
        s = Story.objects.get()
        assert s.body == "It was a dark and stormy night."
        assert s.submitter == profile.user
        assert s.submitter_name == "Somebody"
        assert s.nominal_date.isoformat() == '2013-03-21'


    def test_submit_story_ajax(self, no_csrf_client):
        """User can submit a story via AJAX."""
        user = UserFactory.create()
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        resp = no_csrf_client.post(
            url,
            {'body': "It was a dark and stormy night."},
            user=user,
            status=200,
            ajax=True,
            )

        assert resp.json['success']
        assert resp.json['messages'] == [{
                'level': 25,
                'tags': 'success',
                'message': "Thanks for submitting your story!",
                }]
        assert 'stormy night' in resp.json['html']
        s = Story.objects.get()
        assert s.body == "It was a dark and stormy night."


    def test_no_anonymous_story_ajax(self, no_csrf_client):
        """User can't submit a story anonymously via AJAX."""
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        no_csrf_client.post(
            url,
            {'body': "It was a dark and stormy night."},
            status=403,
            ajax=True,
            )


    def test_submit_story_ajax_requires_body(self, no_csrf_client):
        """Error if story submitted via ajax with no body."""
        user = UserFactory.create()
        profile = TeacherProfileFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': profile.user.username})
        resp = no_csrf_client.post(
            url, {'body': ""}, status=200, ajax=True, user=user)

        assert not resp.json['success']
        assert resp.json['messages'] == [{
                'level': 40,
                'tags': 'error',
                'message': "You seem to have left your story blank.",
                }]
        assert not Story.objects.count()


    def test_404_on_nonexistent_teacher(self, client):
        """404 is returned for a nonexistent teacher username."""
        url = reverse('teacher_detail', kwargs={'username': 'foo'})
        client.get(url, status=404)


    def test_404_on_non_teacher_user(self, client):
        """404 is returned for a user with no teacher profile."""
        u = UserFactory.create()
        url = reverse('teacher_detail', kwargs={'username': u.username})
        client.get(url, status=404)


    def test_delete_story(self, client):
        """Can delete a story on my profile page."""
        s = StoryFactory.create()
        u = s.profile.user
        url = reverse('teacher_detail', kwargs={'username': u.username})
        form = client.get(url, user=u, status=200).forms[
            'story-%s-actions-form' % s.id]

        resp = form.submit('delete-story', status=302)

        assert redirects_to(resp) == url
        assert is_deleted(s)


    def test_delete_story_ajax(self, no_csrf_client):
        """Can delete a story on my profile page via ajax."""
        s = StoryFactory.create()
        u = s.profile.user
        url = reverse('teacher_detail', kwargs={'username': u.username})

        resp = no_csrf_client.post(
            url, {'delete-story': s.id}, user=u, status=200, ajax=True)

        assert resp.json['success'] == True
        assert len(resp.json['messages']) == 1
        assert resp.json['messages'][0]['message'] == "Story deleted."
        assert is_deleted(s)


    @pytest.mark.parametrize('action', ['publish-story', 'hide-story'])
    def test_publish_or_hide_story(self, client, action):
        """Can publish/hide a story on my profile page."""
        initially_published = (action == 'hide-story')
        s = StoryFactory.create(private=False, published=initially_published)
        u = s.profile.user
        url = reverse('teacher_detail', kwargs={'username': u.username})
        form = client.get(url, user=u, status=200).forms[
            'story-%s-actions-form' % s.id]

        resp = form.submit(action, status=302)

        assert redirects_to(resp) == url
        assert refresh(s).published == (not initially_published)


    @pytest.mark.parametrize('action', ['publish-story', 'hide-story'])
    def test_publish_or_hide_story_ajax(self, no_csrf_client, action):
        """Can publish a story on my profile page via ajax."""
        initially_published = (action == 'hide-story')
        s = StoryFactory.create(private=False, published=initially_published)
        u = s.profile.user
        url = reverse('teacher_detail', kwargs={'username': u.username})

        resp = no_csrf_client.post(
            url, {action: s.id}, user=u, status=200, ajax=True)

        assert resp.json['success'] == True
        assert 'csrfmiddlewaretoken' in resp.json['html']
        assert refresh(s).published == (not initially_published)


    @pytest.mark.parametrize('action',
                             ['publish-story', 'hide-story', 'delete-story'])
    def test_cant_modify_stories_on_other_profile(self, no_csrf_client, action):
        """No deleting/hiding/publishing stories on someone else's profile."""
        s = StoryFactory.create()
        u = UserFactory.create()
        url = reverse(
            'teacher_detail', kwargs={'username': s.profile.user.username})

        no_csrf_client.post(url, {action: s.id}, user=u, status=403, ajax=True)


    @pytest.mark.parametrize('action', ['publish-story', 'hide-story'])
    def test_bad_story_id(self, no_csrf_client, action):
        """Bad story id just returns success: False."""
        tp = TeacherProfileFactory.create()
        url = reverse('teacher_detail', kwargs={'username': tp.user.username})

        resp = no_csrf_client.post(
            url, {action: '7'}, user=tp.user, status=200, ajax=True)

        assert resp.json['success'] == False
        assert 'html' not in resp.json
        assert resp.json['messages'][0] == {
            'message': "That story has been removed.",
            'level': 40,
            'tags': 'error',
            }



class TestCreateProfile:
    def test_create_profile(self, client):
        """User without profile can create one."""
        u = UserFactory.create()
        form = client.get(reverse('create_profile'), user=u).forms[
            'create-profile-form']
        form['school'] = "Sample Elementary"
        form['bio'] = "This is my song."
        resp = form.submit()

        tp = u.teacher_profile
        assert tp.bio == "This is my song."
        assert tp.school == "Sample Elementary"
        assert redirects_to(resp) == reverse(
            'teacher_detail', kwargs={'username': u.username})


    def test_school_required(self, client):
        """Must provide school name."""
        u = UserFactory.create()
        form = client.get(reverse('create_profile'), user=u).forms[
            'create-profile-form']
        resp = form.submit(status=200)

        resp.mustcontain('field is required')


    def test_already_has_profile(self, client):
        """If user already has profile, they are redirected to it."""
        tp = TeacherProfileFactory.create()
        profile_url = reverse(
            'teacher_detail', kwargs={'username': tp.user.username})
        create_url = reverse('create_profile')

        resp = client.get(create_url, user=tp.user, status=302)

        assert redirects_to(resp) == profile_url


    def test_login_required(self, client):
        """If user is not logged in, they are redirected to login page."""
        login_url = reverse('login')
        create_url = reverse('create_profile')
        resp = client.get(create_url, status=302)

        assert redirects_to(resp) == login_url + '?next=' + create_url
