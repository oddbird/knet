from knet.landing.models import Lead


def test_landing(client):
    """Landing page loads without error."""
    client.get('/', status=200)


def test_submit_lead(client):
    """Can submit a lead."""
    form = client.get('/').forms[0]
    form['email'] = 'some@example.com'
    resp = form.submit().follow()

    resp.mustcontain('Thanks for your interest')
    leads = list(Lead.objects.all())
    assert leads[0].email == 'some@example.com'


def test_submit_lead_ajax(no_csrf_client):
    """Can submit a lead via ajax."""
    resp = no_csrf_client.post(
        '/', {'email': 'some@example.com'}, ajax=True)

    leads = list(Lead.objects.all())
    assert leads[0].email == 'some@example.com'

    assert set(resp.json.keys()) == {'messages', 'html'}


def test_demo(client):
    """Demo page loads without error."""
    client.get('/demo/', status=200)
