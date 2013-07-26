from knet.assets.css import RCSSMinCompressor


def test_compress_css():
    c = RCSSMinCompressor(verbose=False)
    out = c.compress_css('body { display: none; } /* foo */')
    assert out == 'body{display:none}'
