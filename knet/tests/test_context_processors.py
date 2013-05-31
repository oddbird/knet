from django.test.utils import override_settings

from knet import context_processors


def test_google_analytics():
    with override_settings(GOOGLE_ANALYTICS_ID='foo'):
        d = context_processors.services(None)
        assert d['GOOGLE_ANALYTICS_ID'] == 'foo'
