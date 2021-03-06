from knet.teachers.forms import StoryForm
from knet.teachers.viewmodels import ViewTeacher, ViewStory

from ..factories import UserFactory
from ..utils import render_to_soup, innerhtml
from .factories import TeacherProfileFactory, StoryFactory



def test_bio_rendered_with_markdown():
    """Bio on teacher profile renders through markdown."""
    tp = TeacherProfileFactory.build(bio="Some *text*")
    bio = render_to_soup(
        'stories/_teacher_info.html',
        {'teacher': ViewTeacher(tp)},
        ).find('div', 'teacher-bio')

    assert innerhtml(bio) == '<p>Some <em>text</em></p>'


def test_stories_rendered_with_markdown():
    """Stories on teacher profile render through markdown."""
    s = StoryFactory.build(body="Some *text*")
    soup = render_to_soup('stories/_story.html', {'story': ViewStory(s)})
    body = soup.find('div', 'story-content')

    assert innerhtml(body) == '<p>Some <em>text</em></p>'


def test_only_published_stories_shown(db):
    """Non-published story not shown to the public."""
    s = StoryFactory.create(published=False)
    p = s.profile
    u = UserFactory.build(id=1)
    soup = render_to_soup(
        'stories/teacher_detail.html',
        {'teacher': ViewTeacher(p), 'user': u, 'form': StoryForm(u, p)},
        )

    assert not len(soup.findAll('article', 'story'))


def test_unpublished_story_shown_to_me(db):
    """I can see unpublished stories on my own profile."""
    s = StoryFactory.create(published=False)
    p = s.profile
    soup = render_to_soup(
        'stories/teacher_detail.html',
        {
            'teacher': ViewTeacher(p),
            'user': p.user,
            'form': StoryForm(p.user, p),
            },
        )

    assert len(soup.findAll('article', 'story')) == 1


def test_no_story_controls_on_someone_elses_profile():
    """I don't get publish/private story controls on someone else's profile."""
    s = StoryFactory.build(private=False, published=True)
    u = UserFactory.build(id=1)
    soup = render_to_soup(
        'stories/_story.html',
        {'story': ViewStory(s), 'teacher': ViewTeacher(s.profile), 'user': u},
        )

    assert len(soup.findAll('button')) == 0
