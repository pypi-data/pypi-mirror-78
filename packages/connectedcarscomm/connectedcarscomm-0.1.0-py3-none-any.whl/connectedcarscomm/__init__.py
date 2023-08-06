import aiohttp
from aiohttp.hdrs import ACCEPT, CONTENT_TYPE, AUTHORIZATION
import json
from typing import List

from .constants import URL_AUTH, URL_REQ, HEADER_NAMESPACE, TYPE_APP_JSON, API_REQUEST_RETIES, API_DEFAULT_TIMEOUT

class ConnectedCarsCommClient(object):
    """Client wrapping the ConnectedCars.io GraphQL API"""

    def __init__(self, username, password, namespace):
        """Class init"""
        self.user = username
        self.pwd = password
        self.namespace = namespace
        self.authtoken = None
        self.retries = 0

    async def async_refresh_authtoken(self, session, timeout = API_DEFAULT_TIMEOUT):
        """Refresh client authorization token"""
        headers = {
            ACCEPT: TYPE_APP_JSON,
            CONTENT_TYPE: TYPE_APP_JSON,
            HEADER_NAMESPACE: self.namespace
        }
        data = {
            'email': self.user,
            'password': self.pwd
        }

        try:
            async with session.post(URL_AUTH, headers = headers, json = data, timeout = timeout) as response:
                if response.status == 200:
                    data = await response.json(encoding = 'utf-8')
                    self.authtoken = data['token']
                else:
                    raise ConnectedCarsCommException("An unexpected response was received: '{}'".format(await response.text()))
                    
        except Exception as e:
            raise ConnectedCarsCommException from e

    async def async_query(self, query, timeout = API_DEFAULT_TIMEOUT):
        """Executes a query"""
        headers = {
            HEADER_NAMESPACE: self.namespace,
            AUTHORIZATION: 'Bearer {}'.format(self.authtoken),
            ACCEPT: TYPE_APP_JSON,
            CONTENT_TYPE: TYPE_APP_JSON
        }
        data = {
            'query': query 
        }
        
        try:
            async with aiohttp.ClientSession() as clientSession:
                if self.authtoken is None:
                    await self.async_refresh_authtoken(clientSession, timeout)

                while self.retries < API_REQUEST_RETIES:
                    async with clientSession.post(URL_REQ, headers = headers, json = data, timeout = timeout) as response:
                        if response.status == 200:
                            self.retries = 0
                            data = await response.json(encoding = 'utf-8')
                            return data
                        elif response.status == 401:
                            self.retries = self.retries + 1
                            await self.async_refresh_authtoken(clientSession, timeout)
                            continue
                        else:
                            raise ConnectedCarsCommException("An unexpected response was received: '{}'".format(await response.text()))

        except Exception as e:
            raise ConnectedCarsCommException from e

class ConnectedCarsCommException(Exception):
    pass