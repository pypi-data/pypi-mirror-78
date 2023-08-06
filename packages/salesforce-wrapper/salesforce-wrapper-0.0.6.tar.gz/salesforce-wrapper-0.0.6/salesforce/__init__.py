import requests
from urllib.parse import urlencode
from json import JSONDecodeError


class SalesForceException(Exception):
    def __init__(self, exception_data, *args, **kwargs):
        self.error_code = exception_data[0]['errorCode']
        self.message = exception_data[0]['message']
        super().__init__(args, kwargs)

    def __str__(self):
        return f"Error code: {self.error_code}, message: {self.message}"


class SalesForceSession(object):
    methods = {
        "create": "post",
        "delete": "delete",
        "get": "get",
        "list": "get",
        "update": "patch",
    }

    def __init__(
        self, crm_url, access_token, refresh_token, client_id='', client_secret=''
    ):
        self.api_url = f"{crm_url}/services/data/v39.0/"
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

    def _send_api_request(self, url, http_method, data=None):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.session.headers.update(**headers)
        request = getattr(self.session, http_method)
        try:
            response = request(url, json=data)
            if response.status_code > 399:
                raise SalesForceException(response.json())
            return response.json()
        except (requests.ConnectionError, JSONDecodeError) as e:
            exc_data = [
                {"errorCode": "ConnectionError_or_JsonDecodeerror", "message": str(e)}
            ]
            raise SalesForceException(exc_data)

    def send_api_request(self, request):
        api_object_url = (
            f"{self.api_url}sobjects/"
            if request._method_name['service'] != "query"
            else self.api_url
        )
        if request._object_id:
            url = f"{api_object_url}{request._method_name['service']}/{request._object_id}"
        else:
            url = f"{api_object_url}{request._method_name['service']}"
        method = request._method_name['method']
        params = request._method_args
        if (method == 'update' or method == 'get') and not request._object_id:
            raise ValueError("object_id must be implemented in update or get methods")
        elif method == 'create' and not params:
            raise ValueError("data must be implemented in create method")
        http_method = self.methods[method]
        return self._send_api_request(url, http_method, params)


class SalesForceAPI(object):
    def __init__(
        self, crm_url, access_token, refresh_token, client_id="", client_secret=""
    ):
        self._session = SalesForceSession(
            crm_url,
            access_token,
            refresh_token,
            client_id=client_id,
            client_secret=client_secret,
        )

    def update_tokens(self):
        url = "https://login.salesforce.com/services/oauth2/token"
        data = {
            'grant_type': 'refresh_token',
            'client_id': self._session.client_id,
            'client_secret': self._session.client_secret,
            'refresh_token': self._session.refresh_token,
            'format': 'json',
        }
        r = requests.post(f'{url}?{urlencode(data)}').json()
        self.access_token = r['access_token']

    def __getattr__(self, method_name):
        if method_name == 'update_tokens':
            return self.update_tokens()
        return Request(self, method_name)

    def __call__(self, method_name, method_kwargs={}):
        return getattr(self, method_name)(method_kwargs)


class Request(object):
    __slots__ = ('_api', '_method_name', '_method_args', '_object_id')

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name

    def __getattr__(self, method_name):
        return Request(self._api, {'service': self._method_name, 'method': method_name})

    def q(self, params):
        return Request(self._api, {'service': self._method_name, 'method': "get"})(
            f"?q={params}"
        )

    def __call__(self, object_id=None, data={}):
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")
        self._method_args = data
        self._object_id = object_id
        return self._api._session.send_api_request(self)
