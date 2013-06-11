from django.core.urlresolvers import reverse



def test_styleguide(client):
    """Styleguide loads without error."""
    client.get(reverse('styleguide'), status=200)
