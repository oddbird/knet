def redirects_to(response):
    """Assert that the given response redirects to the given URL."""
    return response.headers['location'].replace('http://localhost:80', '')
