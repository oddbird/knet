from django.test.utils import override_settings

from knet.landing.models import Lead



@override_settings(ENABLE_LOGIN=True)
def test_login_button(client):
    """Login link is in banner."""
    resp = client.get('/')

    assert len(resp.html.findAll('a', 'fb-login')) == 1


@override_settings(ENABLE_LOGIN=False)
def test_login_disabled(client):
    """No login link if disabled in settings."""
    resp = client.get('/')

    assert len(resp.html.findAll('a', 'fb-login')) == 0


def test_submit_lead(client):
    """Can submit a lead."""
    form = client.get('/').forms[0]
    form['email'] = 'some@example.com'
    resp = form.submit().follow()

    resp.mustcontain('Thanks for your interest')
    leads = list(Lead.objects.all())
    assert len(leads) == 1
    assert leads[0].email == 'some@example.com'


def test_submit_lead_error(client):
    """Get an error message if lead submitted."""
    form = client.get('/').forms[0]
    form['email'] = ''
    resp = form.submit()

    resp.mustcontain('look like an email')
    assert not Lead.objects.exists()


def test_submit_lead_ajax(no_csrf_client):
    """Can submit a lead via ajax."""
    resp = no_csrf_client.post(
        '/', {'email': 'some@example.com'}, ajax=True)

    leads = list(Lead.objects.all())
    assert len(leads) == 1
    assert leads[0].email == 'some@example.com'

    assert set(resp.json.keys()) == {'messages', 'html'}


def test_submit_lead_ajax_error(no_csrf_client):
    """Form errors are returned via a user message."""
    resp = no_csrf_client.post('/', {'email': ''}, ajax=True)

    assert not Lead.objects.exists()
    msg = resp.json['messages'][0]
    assert msg == {
        'message': "That doesn't look like an email address; double-check it?",
        'level': 40,
        'tags': 'error',
        }
