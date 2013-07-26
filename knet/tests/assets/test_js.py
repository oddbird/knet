from knet.assets.js import RJSMinCompressor


def test_compress_js():
    c = RJSMinCompressor(verbose=False)
    out = c.compress_js('/* foo */\nvar foo = "bar";')
    assert out == 'var foo="bar";'
