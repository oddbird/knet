from ..factories import UserFactory



def test_get_name():
    """get_name returns value of name field, if present."""
    u = UserFactory.build(name="Someone")

    assert u.get_name() == "Someone"


def test_get_name_first_last_fallback():
    """If name field is empty, returns first_name and last_name."""
    u = UserFactory.build(first_name="Some", last_name="One")

    assert u.get_name() == "Some One"


def test_get_name_username_fallback():
    """If name, first_name, and last_name empty, returns username."""
    u = UserFactory.build(username="someone")

    assert u.get_name() == "someone"


def test_str():
    """String representation is value of get_name() method."""
    u = UserFactory.build(name="Someone")

    assert str(u) == "Someone"
