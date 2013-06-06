from knet.stories.templatetags.stories import stories_visible_to
from knet.teachers.viewmodels import ViewTeacher

from ...factories import UserFactory
from ..factories import StoryFactory


class TestVisibleTo(object):
    def test_unpublished_visible_to_self(self, db):
        """I can see my own unpublished stories."""
        s = StoryFactory.create(published=False)

        visible = stories_visible_to(ViewTeacher(s.profile), s.profile.user)

        assert visible.count() == 1


    def test_published_visible_to_other(self, db):
        """Anyone can see my published stories."""
        s = StoryFactory.create(published=True)
        u = UserFactory.build()

        visible = stories_visible_to(ViewTeacher(s.profile), u)

        assert visible.count() == 1


    def test_unpublished_invisible_to_other(self, db):
        """No-one else can see my unpublished stories."""
        s = StoryFactory.create(published=False)
        u = UserFactory.build()

        visible = stories_visible_to(ViewTeacher(s.profile), u)

        assert visible.count() == 0
