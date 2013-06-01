from django.core.urlresolvers import reverse

from knet.stories.models import Story
from ..factories import UserFactory
from ..utils import redirects_to
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
    u = UserFactory()
    url = reverse('teacher_detail', kwargs={'username': u.username})
    client.get(url, status=404)
