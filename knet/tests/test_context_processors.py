from django.test.utils import override_settings

from knet import context_processors


def test_story_cache_timeout():
    with override_settings(STORY_CACHE_TIMEOUT=600):
        d = context_processors.settings(None)
        assert d['STORY_CACHE_TIMEOUT'] == 600


def test_google_analytics():
    with override_settings(GOOGLE_ANALYTICS_ID='foo'):
        d = context_processors.settings(None)
        assert d['GOOGLE_ANALYTICS_ID'] == 'foo'


def test_enable_login():
    with override_settings(ENABLE_LOGIN=False):
        d = context_processors.settings(None)
        assert d['ENABLE_LOGIN'] == False

def test_base_url():
    with override_settings(BASE_URL=False):
        d = context_processors.settings(None)
        assert d['BASE_URL'] == False
