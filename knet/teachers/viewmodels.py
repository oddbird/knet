from django.db.models import Q


class ViewTeacher:
    """View model for a ``TeacherProfile`` and associated ``User``."""
    def __init__(self, teacher_profile):
        self._profile = teacher_profile
        self.user = self._profile.user
        self.school = self._profile.school
        self.date_joined = self.user.date_joined
        self.bio = self._profile.bio
        self.full_name = str(self.user)


    def __str__(self):
        """String representation is that of the user."""
        return self.full_name


    def stories(self, visible_to=None):
        """
        Yield all the stories on this profile as ``ViewStory`` instances.

        If ``visible_to`` is provided it should be a ``User`` instance, and
        only stories visible to that user will be shown.

        """
        qs = self._profile.stories.order_by('-created')
        if visible_to and (visible_to != self.user):
            filters = Q(published=True)
            if visible_to.is_authenticated():
                filters = filters | Q(submitter=visible_to)
            qs = qs.filter(filters)
        for story in qs:
            yield ViewStory(story)



class ViewStory:
    """View model for a ``Story``."""
    def __init__(self, story):
        self._story = story
        self.id = story.id
        self.body = story.body
        self.private = story.private
        self.published = story.published
        self.date = story.nominal_date or story.created.date()
        self.attribution = story.submitter_name or (
            story.submitter.first_name if story.submitter else '')
