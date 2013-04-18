def test_home(client):
    """Home page loads without error."""
    client.get('/', status=200)

