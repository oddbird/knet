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
    assert len(leads) == 1
    assert leads[0].email == 'some@example.com'


def test_demo(client):
    """Demo page loads without error."""
    client.get('/demo/', status=200)
