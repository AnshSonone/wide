from rest_framework import renderers
import json

class UserRenderers(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'Execption' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)

        return response
