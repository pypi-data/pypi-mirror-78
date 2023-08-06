__version__ = "0.1.0"

import requests
import inflection

from . import api
from . import export

HTTP_ERROR = requests.exceptions.HTTPError


class _SessionData:
    def __init__(self, **session_data):
        for k, v in session_data.items():
            k = k.replace(".", "_")
            k = inflection.camelize(k)
            k = inflection.underscore(k)

            if isinstance(v, dict):
                self.__dict__[k] = _SessionData(**v)
            else:
                self.__dict__[k] = v


class FPODMS:
    """An F&P ODMS session.

    :param email_address: A string, a valid login email address.
    :param password: A string, a valid login email address.
    """

    def __init__(self, email_address, password):
        self.base_url = "https://fpdms.heinemann.com"
        self.session = requests.session()

        login_path = "/api/account/login"
        login_payload = {"emailAddress": email_address, "password": password}
        login_response = self._request(
            method="POST", path=login_path, content_type='json', data=login_payload
        )

        session_data = _SessionData(**login_response)
        self.preferences = session_data.preferences
        self.session_timeout_minutes = session_data.session_timeout_minutes
        self.state = session_data.state
        self.user = session_data.user

        self.api = api.API(self)
        self.export = export.Export(self)

    def _request(self, method, path, content_type, params={}, data={}):
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(method, url, params=params, json=data)
            response.raise_for_status()
            if content_type == 'json':
                return response.json().get("data")
            else:
                return response
        except HTTP_ERROR as e:
            print(e)
