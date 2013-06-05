from django.core.urlresolvers import reverse
import pytest

from knet.stories.models import Story
from ..factories import UserFactory
from ..stories.factories import StoryFactory
from ..utils import redirects_to, is_deleted, refresh
from .factories import TeacherProfileFactory



def test_submit_story_anonymously(client):
    """User can submit a story anonymously on the teacher profile page."""
    teacher = TeacherProfileFactory.create()
    url = reverse('teacher_detail', kwargs={'username': teacher.user.username})
    form = client.get(url).forms[0]
    form['body'] = "It was a dark and stormy night."
    resp = form.submit()

    assert resp.status_code == 302, resp
    assert redirects_to(resp) == url
    s = Story.objects.get()
    assert s.body == "It was a dark and stormy night."



def test_submit_story_requires_body(client):
    """User can submit a story anonymously on the teacher profile page."""
    teacher = TeacherProfileFactory.create()
    url = reverse('teacher_detail', kwargs={'username': teacher.user.username})
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
    tp = TeacherProfileFactory.create()
    s = StoryFactory.create(teacher=tp.user)
    url = reverse('teacher_detail', kwargs={'username': s.teacher.username})
    form = client.get(url, user=s.teacher, status=200).forms[1]

    resp = form.submit('delete-story', status=302)

    assert redirects_to(resp) == url
    assert is_deleted(s)



def test_delete_story_ajax(no_csrf_client):
    """Can delete a story on my profile page via ajax."""
    tp = TeacherProfileFactory.create()
    s = StoryFactory.create(teacher=tp.user)
    url = reverse('teacher_detail', kwargs={'username': s.teacher.username})

    resp = no_csrf_client.post(
        url, {'delete-story': s.id}, user=s.teacher, status=200, ajax=True)

    assert resp.json['success'] == True
    assert resp.json['messages'][0]['message'] == "Story deleted."
    assert is_deleted(s)



def test_publish_story(client):
    """Can publish a story on my profile page."""
    tp = TeacherProfileFactory.create()
    s = StoryFactory.create(teacher=tp.user, private=False, published=False)
    url = reverse('teacher_detail', kwargs={'username': s.teacher.username})
    form = client.get(url, user=s.teacher, status=200).forms[1]

    resp = form.submit('publish-story', status=302)

    assert redirects_to(resp) == url
    assert refresh(s).published



def test_publish_story_ajax(no_csrf_client):
    """Can publish a story on my profile page via ajax."""
    tp = TeacherProfileFactory.create()
    s = StoryFactory.create(teacher=tp.user, private=False, published=False)
    url = reverse('teacher_detail', kwargs={'username': s.teacher.username})

    resp = no_csrf_client.post(
        url, {'publish-story': s.id}, user=s.teacher, status=200, ajax=True)

    assert resp.json['success'] == True
    assert 'html' in resp.json
    assert refresh(s).published



def test_hide_story(client):
    """Can hide a story on my profile page."""
    tp = TeacherProfileFactory.create()
    s = StoryFactory.create(teacher=tp.user, private=False, published=True)
    url = reverse('teacher_detail', kwargs={'username': s.teacher.username})
    form = client.get(url, user=s.teacher, status=200).forms[1]

    resp = form.submit('hide-story', status=302)

    assert redirects_to(resp) == url
    assert not refresh(s).published



def test_hide_story_ajax(no_csrf_client):
    """Can hide a story on my profile page via ajax."""
    tp = TeacherProfileFactory.create()
    s = StoryFactory.create(teacher=tp.user, private=False, published=True)
    url = reverse('teacher_detail', kwargs={'username': s.teacher.username})

    resp = no_csrf_client.post(
        url, {'hide-story': s.id}, user=s.teacher, status=200, ajax=True)

    assert resp.json['success'] == True
    assert 'html' in resp.json
    assert not refresh(s).published



@pytest.mark.parametrize('action', ['publish-story', 'hide-story'])
def test_bad_story_id(no_csrf_client, action):
    """Bad story id just returns success: False."""
    tp = TeacherProfileFactory.create()
    url = reverse('teacher_detail', kwargs={'username': tp.user.username})

    resp = no_csrf_client.post(
        url, {action: '7'}, user=tp.user, status=200, ajax=True)

    assert resp.json['success'] == False
    assert 'html' not in resp.json
