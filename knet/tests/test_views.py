def test_demo(client):
    """Demo page loads without error."""
    client.get('/demo/', status=200)
