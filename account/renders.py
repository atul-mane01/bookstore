from email import charset
from urllib import response
from rest_framework import renderers


import json

class UserRender(renderers.JSONRenderer):
    charset='utf8'
    def render(self,data,accepted_media_type=None,renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            response=json.dumps({'errors':data})
        else:
            response=json.dumps(data)

        return response
