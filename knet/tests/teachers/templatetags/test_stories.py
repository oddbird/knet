from pretend import stub

from knet.teachers.templatetags.stories import stories_visible_to


class TestVisibleTo:
    def test_passes_through(self):
        """Just calls teacher's stories() method with user."""
        user = stub()
        teacher = stub(stories=lambda u: ('stories of', u))

        assert stories_visible_to(teacher, user) == ('stories of', user)
