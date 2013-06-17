from datetime import datetime, date

from knet.teachers.viewmodels import ViewTeacher, ViewStory

from ..factories import UserFactory
from .factories import TeacherProfileFactory, StoryFactory


class TestViewTeacher:
    def test_str(self):
        """Passes through string representation of teacher."""
        tp = TeacherProfileFactory.build(user__name="A Song")
        vt = ViewTeacher(tp)

        assert str(vt) == "A Song"


    def test_attributes(self):
        """Some attributes pass through to user or profile."""
        tp = TeacherProfileFactory.build()
        vt = ViewTeacher(tp)

        assert vt.user == tp.user
        assert vt.school == tp.school
        assert vt.date_joined == tp.user.date_joined
        assert vt.bio == tp.bio
        assert vt.full_name == str(tp.user)


    def test_stories(self, db):
        """By default gets all stories for profile, most recent first."""
        s1 = StoryFactory.create(created=datetime(2013, 6, 11))
        s2 = StoryFactory.create(
            created=datetime(2013, 6, 10), profile=s1.profile)
        s3 = StoryFactory.create(
            created=datetime(2013, 6, 12), profile=s1.profile)

        vt = ViewTeacher(s1.profile)

        assert [s.id for s in vt.stories()] == [s3.id, s1.id, s2.id]


    def test_unpublished_visible_to_self(self, db):
        """I can see unpublished stories on my own profile."""
        s = StoryFactory.create(published=False)

        visible = ViewTeacher(s.profile).stories(s.profile.user)

        assert len(list(visible)) == 1


    def test_published_visible_to_other(self, db):
        """Anyone can see my published stories."""
        s = StoryFactory.create(published=True)
        u = UserFactory.build()

        visible = ViewTeacher(s.profile).stories(u)

        assert len(list(visible)) == 1


    def test_unpublished_invisible_to_other(self, db):
        """No-one else can see my unpublished stories."""
        s = StoryFactory.create(published=False)
        u = UserFactory.build()

        visible = ViewTeacher(s.profile).stories(u)

        assert len(list(visible)) == 0


    def test_can_see_my_own_unpublished(self, db):
        """I can see unpublished stories I posted to someone's profile."""
        me = UserFactory.create()
        s = StoryFactory.create(published=False, submitter=me)

        visible = ViewTeacher(s.profile).stories(me)

        assert len(list(visible)) == 1



class TestViewStory:
    def test_id(self):
        """``id`` attr is story ID."""
        s = StoryFactory.build(id=7)
        vs = ViewStory(s)

        assert vs.id == 7


    def test_published(self):
        """``published`` attr is story ``published`` attr."""
        s = StoryFactory.build(published=True)
        vs = ViewStory(s)

        assert vs.published


    def test_private(self):
        """``private`` attr is story ``private`` attr."""
        s = StoryFactory.build(private=True)
        vs = ViewStory(s)

        assert vs.private


    def test_body(self):
        """``body`` attr is story ``body`` attr."""
        s = StoryFactory.build(body='Foo')
        vs = ViewStory(s)

        assert vs.body == 'Foo'


    def test_date_nominal_date(self):
        """Nominal date takes precedence, if present."""
        s = StoryFactory.build(
            nominal_date=date(2013, 12, 11), created=datetime(2012, 1, 1))
        vs = ViewStory(s)

        assert vs.date == date(2013, 12, 11)


    def test_date_falls_back_to_created(self):
        """If no nominal date, fall back to created date."""
        s = StoryFactory.build(
            nominal_date=None, created=datetime(2012, 11, 10, 9, 8, 7))
        vs = ViewStory(s)

        assert vs.date == date(2012, 11, 10)


    def test_attribution_override(self):
        """``submitter_name``, if present, takes precedence."""
        s = StoryFactory.build(submitter_name='Foo')
        vs = ViewStory(s)

        assert vs.attribution == 'Foo'


    def test_attribution_fallback(self):
        """If no ``submitter_name`` falls back to submitting user first name."""
        s = StoryFactory.build(submitter__first_name='Bar')
        vs = ViewStory(s)

        assert vs.attribution == 'Bar'


    def test_self_posted(self):
        """If submitter is same as profile, story is self-posted."""
        u = UserFactory.build()
        s = StoryFactory.build(submitter=u, profile__user=u)
        vs = ViewStory(s)

        assert vs.self_posted


    def test_not_self_posted(self):
        s = StoryFactory.build(submitter__id=1, profile__user__id=2)
        vs = ViewStory(s)

        assert not vs.self_posted
