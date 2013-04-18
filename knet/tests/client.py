"""
Webapp integration test client.

"""
import django_webtest



class TestClient(django_webtest.DjangoTestApp):
    """
    A WebTest-based test client for webapp integration tests.

    """
    def get(self, *a, **kw):
        """Make a GET request."""
        return super(TestClient, self).get(*a, **self._ajax(kw))


    def post(self, *a, **kw):
        """Make a POST request."""
        return super(TestClient, self).post(*a, **self._ajax(kw))


    def _ajax(self, kw):
        """Support a boolean 'ajax' kwarg for simulating ajax requests."""
        if kw.pop('ajax', False):
            headers = kw.setdefault('headers', {})
            headers['X-Requested-With'] = 'XMLHttpRequest'
        return kw
