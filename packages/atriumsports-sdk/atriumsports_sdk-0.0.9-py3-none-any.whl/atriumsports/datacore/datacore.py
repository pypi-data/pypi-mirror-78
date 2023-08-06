""" File containing class to handle connections to datacore """

import json
import requests
from ..atrium_response import AtriumResponse

class DatacoreAPI:
    """ A class to handle the connection to AtriumSports Datacore """

    DEFAULT_LIMIT = 10
    MAX_LIMIT = 200

    def __init__(self, options):
        """ initialise the class """
        self._options = {
            'sport': options.get('sport', 'basketball'),
            'credential_id': options.get('credential_id'),
            'credential_secret': options.get('credential_secret'),
            'organizations': options.get('organizations', []),
            'org_group': options.get('org_group'),
            'environment': options.get('environment', 'production'),
            'token': options.get('token'),
            'headers': options.get('headers', {}),
            'version': 1, # version
        }
        self._headers = self._options.get('headers', {})
        self._auth_token = self._options.get('token')
        self._resources = {}
        self._auth_error = ''

    def post(self, url, **kwargs):
        """ POST method"""

        if not kwargs.get('body'):
            self._return_error('POST method requries a body parameter')
        return self.call('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """ PUT method"""
        if not kwargs.get('body'):
            self._return_error('PUT method requries a body parameter')
        return self.call('PUT', url, **kwargs)

    def get(self, url, **kwargs):
        """ GET method"""
        return self.call('GET', url, **kwargs)

    def delete(self, url, **kwargs):
        """ DELETE method"""
        return self.call('DELETE', url, **kwargs)

    def _generate_token(self):
        """ generate an auth token """
        self._auth_token = ''
        self._auth_error = ''
        auth_url = self._get_url('auth')
        auth_data = {
            'credentialId': self._options.get('credential_id', ''),
            'credentialSecret': self._options.get('credential_secret', ''),
            'sport': self._options.get('sport'),
            'organization': {},
        }
        if self._options.get('org_group'):
            auth_data['organization']['group'] = self._options.get('org_group')
        else:
            auth_data['organization']['id'] = self._options.get('organizations')
        result = self._api_call_internal('post', auth_url, body=auth_data)
        if result:
            if result.success():
                self._auth_token = result.data().get('token')
            else:
                self._auth_error = result.error_string()
        return self._auth_token

    def _get_auth_token(self):
        """ Return an auth token """
        if self._auth_token:
            return self._auth_token
        return self._generate_token()

    def call(self, method, url, **kwargs):
        """ make the api call """
        method = method.lower()
        limit = kwargs.get('limit', self.DEFAULT_LIMIT)

        call_headers = self._headers.copy()
        call_headers.update(kwargs.get('headers', {}))
        token = self._get_auth_token()
        if not token:
            return self._return_error('Authentication Error: {}'.format(self._auth_error))
        call_headers['Authorization'] = "Bearer {}".format(token)
        call_headers['Content-Type'] = "application/json"
        url = "{}/v{}/{}{}".format(
            self._get_url('api'),
            self._options.get('version'),
            self._options.get('sport'), url
        )
        self._resources = {}
        kwargs['limit'] = self._get_limit(limit)
        kwargs['headers'] = call_headers

        done = False
        response = AtriumResponse()
        while not done:
            resp = self._api_call_internal(
                method,
                url,
                **kwargs
            )
            response.merge(resp)
            if not resp.success():
                done = True
            else:
                if resp.links('next'):
                    call_limit = self._get_limit(limit - response.data_count())
                    if call_limit <= 0:
                        done = True
                else:
                    done = True
        return response

    def _get_limit(self, limit):
        """ make sure limit doesn't exceed MAX_LIMIT """
        if limit > self.MAX_LIMIT:
            return self.MAX_LIMIT
        return limit

    def _api_call_internal(self, method, url, **kwargs):
        """ make the api call """
        try:
            response = self._make_request(method, url, **kwargs)
            return AtriumResponse(response)
        except requests.exceptions.RequestException as err:
            return self._return_error(err)
        return None

    @staticmethod
    def _make_request(method, url, **kwargs):
        """ Lets seperate the actual request code """
        body = json.dumps(kwargs.get('body', {}))
        limit = kwargs.get('limit', 10)
        offset = kwargs.get('offset', 0)
        headers = kwargs.get('headers', {})
        response = None
        if method == 'get':
            if not '?' in url:
                url = url + '?'
            url = url+"&limit={}&offset={}".format(limit, offset)
            response = requests.get(url, headers=headers)
        elif method == 'post':
            response = requests.post(url, headers=headers, data=body)
        elif method == 'put':
            response = requests.put(url, headers=headers, data=body)
        elif method == 'delete':
            response = requests.delete(url, headers=headers, data=body)
        return response

    def _get_url(self, url_type):
        """ return urls for the atriumsports environments """
        # Can we handle localhost?????
        envs = {
            'auth': {
                'production': 'https://token.prod.cloud.atriumsports.com/v1/oauth2/rest/token',
                'nonprod': 'https://token.nonprod.cloud.atriumsports.com/v1/oauth2/rest/token',
                'sandpit': 'https://token.sandpit.cloud.atriumsports.com/v1/oauth2/rest/token',
                'localhost': 'http://localhost:XXXX',
            },
            'api': {
                'production': 'https://api.dc.prod.cloud.atriumsports.com',
                'nonprod': 'https://api.dc.nonprod.cloud.atriumsports.com',
                'sandpit': 'https://api.dc.sandpit.cloud.atriumsports.com',
                'localhost': 'http://localhost:XXXX',
            }
        }
        if not envs.get(url_type):
            return None
        url = envs[url_type].get(self._options.get('environment')) or ''
        return url

    @staticmethod
    def _return_error(error):
        """ Return an error response """
        response = AtriumResponse()
        response.set_error(error)
        return response
