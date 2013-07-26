from pipeline.compressors import CompressorBase
from rjsmin import jsmin


class RJSMinCompressor(CompressorBase):
    def compress_js(self, js):
        return jsmin(js)
