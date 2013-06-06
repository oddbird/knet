class ViewTeacher(object):
    """View model for a ``TeacherProfile`` and associated ``User``."""
    def __init__(self, teacher_profile):
        self._profile = teacher_profile
        self.user = self._profile.user
        self.school = self._profile.school
        self.date_joined = self.user.date_joined
        self.bio = self.user.bio
        self.full_name = str(self.user)


    def __str__(self):
        """String representation is that of the user."""
        return self.full_name


    def stories(self):
        """Return all the stories on this profile."""
        return self._profile.stories.all()
