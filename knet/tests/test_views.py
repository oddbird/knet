def test_home(client):
    """Home page loads without error."""
    client.get('/', status=200)

def test_demo(client):
    """Demo page loads without error."""
    client.get('/demo/', status=200)

