
"""This module contains FB client."""

import os
import requests

import settings


class FBGraphAPI(object):

    """Simple FB client. It is just overhead on requests lib."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.api_version = settings.DEFAULT_VERSION
        self.session = requests.Session()

    def get(self, node_id, **args):
        """Get object from the FB by it {node-id}."""
        return self.request('{0}/{1}'.format(self.api_version, node_id), args)

    def request(self, path, method=None, args=None):
        """Make requests to FB."""
        if args is None:
            args = dict()

        method = method or 'get'

        for k, v in [('debug', 'all'), ('format', 'json'), ('method', method),
                     ('pretty', '0'), ('suppress_http_code', 1)]:
            args[k] = v

        if 'access_token' not in args:
            args['access_token'] = self.access_token

        try:
            response = self.session.request(
                method,
                os.path.join(settings.FACEBOOK_GRAPH_API_URL, path),
                params=args
            )

        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise FBGraphAPIError(response)

        if 'json' in response.headers['content-type']:
            result = response.json()
        else:
            raise FBGraphAPIError('Unsupported MIME type received')

        if 'error' in result:
            raise FBGraphAPIError(result)

        return result


class FBGraphAPIError(Exception):
    def __init__(self, result):
        self.result = result
        self.code = None
        try:
            self.type = result["error_code"]
        except:
            self.type = ""

        # OAuth 2.0 Draft 10
        try:
            self.message = result["error_description"]
        except:
            # OAuth 2.0 Draft 00
            try:
                self.message = result["error"]["message"]
                self.code = result["error"].get("code")
                if not self.type:
                    self.type = result["error"].get("type", "")
            except:
                # REST server style
                try:
                    self.message = result["error_msg"]
                except:
                    self.message = result

        Exception.__init__(self, self.message)

