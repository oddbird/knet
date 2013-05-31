from django.core.urlresolvers import reverse

from knet.stories.models import Story
from ..factories import UserFactory
from ..utils import redirects_to



def test_submit_story_anonymously(client):
    """User can submit a story anonymously on the teacher profile page."""
    teacher = UserFactory.create()
    url = reverse('teacher_detail', kwargs={'teacher_id': teacher.id})
    form = client.get(url).forms[0]
    form['body'] = "It was a dark and stormy night."
    resp = form.submit()

    assert resp.status_code == 302, resp
    assert redirects_to(resp) == url
    s = Story.objects.get()
    assert s.body == "It was a dark and stormy night."



def test_submit_story_requires_body(client):
    """User can submit a story anonymously on the teacher profile page."""
    teacher = UserFactory.create()
    url = reverse('teacher_detail', kwargs={'teacher_id': teacher.id})
    form = client.get(url).forms[0]
    resp = form.submit()

    assert resp.status_code == 200
    assert Story.objects.count() == 0
    resp.mustcontain("field is required")



def test_404_on_nonexistent_teacher_id(client):
    """404 is returned for a nonexistent teacher ID."""
    url = reverse('teacher_detail', kwargs={'teacher_id': 7})
    client.get(url, status=404)
