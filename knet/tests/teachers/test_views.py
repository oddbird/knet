from django.core.urlresolvers import reverse
import pytest

from knet.teachers.models import Story

from ..factories import UserFactory
from ..utils import redirects_to, is_deleted, refresh
from .factories import TeacherProfileFactory, StoryFactory



def test_submit_story_anonymously(client):
    """User can submit a story anonymously on the teacher profile page."""
    profile = TeacherProfileFactory.create()
    url = reverse('teacher_detail', kwargs={'username': profile.user.username})
    form = client.get(url).forms[0]
    form['body'] = "It was a dark and stormy night."
    resp = form.submit()

    assert resp.status_code == 302, resp
    assert redirects_to(resp) == url
    s = Story.objects.get()
    assert s.body == "It was a dark and stormy night."



def test_submit_story_requires_body(client):
    """User can submit a story anonymously on the teacher profile page."""
    profile = TeacherProfileFactory.create()
    url = reverse('teacher_detail', kwargs={'username': profile.user.username})
    form = client.get(url).forms[0]
    resp = form.submit()

    assert resp.status_code == 200
    assert Story.objects.count() == 0
    resp.mustcontain("field is required")



def test_404_on_nonexistent_teacher(client):
    """404 is returned for a nonexistent teacher username."""
    url = reverse('teacher_detail', kwargs={'username': 'foo'})
    client.get(url, status=404)



def test_404_on_non_teacher_user(client):
    """404 is returned for a user with no teacher profile."""
    u = UserFactory.create()
    url = reverse('teacher_detail', kwargs={'username': u.username})
    client.get(url, status=404)



def test_delete_story(client):
    """Can delete a story on my profile page."""
    s = StoryFactory.create()
    u = s.profile.user
    url = reverse('teacher_detail', kwargs={'username': u.username})
    form = client.get(url, user=u, status=200).forms[1]

    resp = form.submit('delete-story', status=302)

    assert redirects_to(resp) == url
    assert is_deleted(s)



def test_delete_story_ajax(no_csrf_client):
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
def test_publish_or_hide_story(client, action):
    """Can publish/hide a story on my profile page."""
    initially_published = (action == 'hide-story')
    s = StoryFactory.create(private=False, published=initially_published)
    u = s.profile.user
    url = reverse('teacher_detail', kwargs={'username': u.username})
    form = client.get(url, user=u, status=200).forms[1]

    resp = form.submit(action, status=302)

    assert redirects_to(resp) == url
    assert refresh(s).published == (not initially_published)



@pytest.mark.parametrize('action', ['publish-story', 'hide-story'])
def test_publish_or_hide_story_ajax(no_csrf_client, action):
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



@pytest.mark.parametrize('action', ['publish-story', 'hide-story'])
def test_bad_story_id(no_csrf_client, action):
    """Bad story id just returns success: False."""
    tp = TeacherProfileFactory.create()
    url = reverse('teacher_detail', kwargs={'username': tp.user.username})

    resp = no_csrf_client.post(
        url, {action: '7'}, user=tp.user, status=200, ajax=True)

    assert resp.json['success'] == False
    assert 'html' not in resp.json
    assert resp.json['messages'][0] == {
        'message': "That story has been removed.", 'level': 40, 'tags': 'error'}
