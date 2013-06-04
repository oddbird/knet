from knet.stories.forms import StoryForm

from ..factories import UserFactory
from ..stories.factories import StoryFactory
from ..utils import render_to_soup, innerhtml
from .factories import TeacherProfileFactory



def test_bio_rendered_with_markdown():
    """Bio on teacher profile renders through markdown."""
    tp = TeacherProfileFactory.build(user__bio="Some *text*")
    bio = render_to_soup(
        'teacher_detail.html',
        {'teacher': tp.user, 'form': StoryForm(tp.user)},
        ).find('div', 'teacher-bio')

    assert innerhtml(bio) == '<p>Some <em>text</em></p>'


def test_stories_rendered_with_markdown():
    """Stories on teacher profile render through markdown."""
    s = StoryFactory.build(body="Some *text*")
    soup = render_to_soup('_story.html', {'story': s})
    body = soup.find('div', 'story-body')

    assert innerhtml(body) == '<p>Some <em>text</em></p>'


def test_only_published_stories_shown():
    """Non-published story not shown to the public."""
    s = StoryFactory.build(published=False)
    u = UserFactory.build(id=1)
    soup = render_to_soup(
        '_story.html', {'story': s, 'teacher': s.teacher, 'user': u})

    assert str(soup).strip() == ''


def test_unpublished_story_shown_to_me():
    """I can see unpublished stories on my own profile."""
    s = StoryFactory.build(published=False)
    soup = render_to_soup(
        '_story.html', {'story': s, 'teacher': s.teacher, 'user': s.teacher})

    assert len(soup.findAll('article', 'story')) == 1


def test_no_story_controls_on_someone_elses_profile():
    """I don't get publish/private story controls on someone else's profile."""
    s = StoryFactory.build(private=False, published=True)
    u = UserFactory.build(id=1)
    soup = render_to_soup(
        '_story.html', {'story': s, 'teacher': s.teacher, 'user': u})

    assert len(soup.findAll('button')) == 0
