import json
from datetime import datetime, date
from urllib.parse import urljoin
from typing import Union
import requests
from requests.auth import HTTPBasicAuth, AuthBase
from requests import HTTPError


class DatabaseAlreadyExistError(Exception):
    pass


class CollectionAlreadyExistError(Exception):
    pass


class DocumentDotExist(Exception):
    pass


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class TokenAuth(AuthBase):
    def __init__(self, token):
        self._token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Token {self._token}'
        return r


class FreedbClient:
    def __init__(self, baseurl, token: Union[str, tuple]):
        self._baseurl = baseurl
        session = requests.Session()
        if isinstance(token, str):
            session.auth = TokenAuth(token)
        else:
            session.auth = token
        self.session = session

    def _urljoin(self, path):
        return urljoin(self._baseurl, path) 

    def create_database(self, db_name):
        session = self.session
        try:
            response = session.post(self._urljoin('/api/databases'), data={'name': db_name})
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 409:
                raise DatabaseAlreadyExistError() from ex
            raise

    def create_collection(self, db_name, col_name):
        session = self.session
        try:
            response = session.post(self._urljoin(f'/api/databases/{db_name}/collections'), data={'name': col_name})
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 409:
                raise CollectionAlreadyExistError() from ex
            raise

    def save_document(self, db_name, col_name, doc):
        response = self.session.post(self._urljoin(f'/api/databases/{db_name}/collections/{col_name}/documents'), 
            data=json.dumps(doc, cls=DateTimeEncoder), 
            headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()[0]

    def query(self, db_name, col_name, query=None, skip=None):
        params = {}
        if query:
            params['query'] = json.dumps(query)
        if skip:
            params['skip'] = skip
        response = self.session.get(self._urljoin(f'/api/databases/{db_name}/collections/{col_name}'), params=params)
        response.raise_for_status()
        return response.json()

    def get_collection(self, db_name, col_name):
        response = self.session.get(self._urljoin(f'/api/databases/{db_name}/collections/{col_name}'))
        response.raise_for_status()
        return response.json()

    def get_document(self, db_name, col_name, doc_id):
        response = self.session.get(self._urljoin(f'/api/databases/{db_name}/collections/{col_name}/documents/{doc_id}'))
        try:
            response.raise_for_status()
        except HTTPError as ex:
            if ex.response.status_code == 404:
                raise DocumentDotExist()
            raise
        return response.json()
