from knet.stories.forms import StoryForm

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
