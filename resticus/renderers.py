import yaml


class OpenAPIRenderer():
    media_type = 'application/vnd.oai.openapi'
    charset = None
    format = 'openapi'

    def __init__(self):
        assert yaml, 'Using OpenAPIRenderer, but `pyyaml` is not installed.'

    def render(self, data, media_type=None, renderer_context=None):
        return yaml.dump(data, default_flow_style=False, sort_keys=False).encode('utf-8')
