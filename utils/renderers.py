from rest_framework import renderers
import json


class CustomJSONRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type, renderer_context):

        response = ""

        if "ErrorDetail" in str(data):
            response = json.dumps(
                {
                    "error": data,
                    "statusCode": renderer_context.get("response").status_code,
                }
            )

        else:
            response = json.dumps(
                {
                    "data": data,
                    "statusCode": renderer_context.get("response").status_code,
                }
            )

        return response