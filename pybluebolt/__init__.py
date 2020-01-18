"""Base Python Class file for BlueBOLT"""

import json
import time
import logging
import requests

from pybluebolt.const import (BLUEBOLT_USER_AGENT, BB_AUTH_URL, 
                              BB_LOCATION_LIST_URL,
                              BB_LOCATION_DETAILS_URL,
                              BB_DEVICE_LIST_URL,
                              BB_DEVICE_STATUS_URL,
                              BB_OUTLET_STATUS_URL)
                              
LOG = logging.getLogger(__name__)

METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_POST = 'POST'

class PyBlueBOLT(object):
    """Base object for BlueBOLT."""

    def __init__(self, username=None, password=None):
        """Create a PyBlueBOLT object.
        :param username: BlueBOLT user email
        :param password: BlueBOLT user password
        :returns PyBlueBOLT base object
        """
        self._session = requests.Session()
        self._headers = {}
        self._params = {}
        self.clear_cache()
        
        self._auth_token = None
        self._username = username
        self._password = password  # should we store this in memory...
        self.login()

    def __repr__(self):
        """Object representation."""
        return "<{0}: {1}>".format(self.__class__.__name__, self._username)

    def login(self):
        """Login to the BlueBOLT account and generate access token"""
        self._reset_headers()

        vars = {
            'username': self._username,
            'password': self._password
        }
        
        LOG.debug(f"Authenticating BlueBOLT account {self._username} via {BB_AUTH_URL}")

        url = BB_AUTH_URL.format(**vars)
        response = requests.post(url, headers=self._headers)
            # Example response:
            # {"data":{"auth":true,"activated":true}}

        json_response = response.json()
        #LOG.debug("BlueBOLT user %s authentication results %s : %s", self._username, BB_AUTH_URL, json_response)
        
        if 'data' in json_response:
            # note: 'login' cookie contains credentials
            auth = json_response['data'].get('auth')
            if auth and auth == 'true':
                self._auth_token = 'FIXME'
                self._auth_token_expiry = time.time() + 604800
                return # success

        LOG.error(f"Failed authenticating BlueBOLT user {self._username}")

    @property
    def is_connected(self):
        """Connection status of client with BlueBOLT cloud service."""
        return bool(self._auth_token) and time.time() < self._auth_token_expiry

    def _reset_headers(self):
        """Reset the headers and params."""
        self._headers = {
            'User-Agent':    BLUEBOLT_USER_AGENT,
            'Content-Type':  'application/json',
            'Accept':        'application/json'
        }
        self.__params = {}

    def query(self, url, method=METHOD_POST, extra_params=None, extra_headers=None, retry=3, force_login=True):
        """
        Returns a JSON object for an HTTP request (no caching included)
        :param url: API URL
        :param method: Specify the method GET, POST or PUT (default=POST)
        :param extra_params: Dictionary to be appended on request.body
        :param extra_headers: Dictionary to be apppended on request.headers
        :param retry: Retry attempts for the query (default=3)
        """
        response = None
        self._reset_headers() # ensure the headers and params are reset to the bare minimum

        # reconnect, if disconnected
        if force_login and not self.is_connected:
            self.login()

        loop = 0
        while loop <= retry:

            # override request.body or request.headers dictionary
            params = self._params
            if extra_params:
                params.update(extra_params)
            LOG.debug("Params: %s", params)

            headers = self._headers
            if extra_headers:
                headers.update(extra_headers)
            LOG.debug("Headers: %s", headers)

            loop += 1
            LOG.debug("Querying %s on attempt: %s/%s", url, loop, retry)

            # define connection method
            request = None
            if method == METHOD_GET:
                request = self._session.get(url, headers=headers)
            elif method == METHOD_PUT:
                request = self._session.put(url, headers=headers, json=params)
            elif method == METHOD_POST:
                request = self._session.post(url, headers=headers, json=params)
            else:
                LOG.error("Invalid request method '%s'", method)
                return None

            if request and (request.status_code == 200):
                response = request.json()
                break # success!

        return response

    def clear_cache(self):
        self._cached_data = None
        self._cached_locations = {}

    def locations(self, use_cached=True):
        """Return all locations registered with the BlueBOLT account."""
        return self.query(BB_LOCATIONS_URL, method='GET')

    def location_details(self, location_id, use_cached=True):
        """Return details on all devices at a location"""
        vars = {
            'site_id': location_id
        }
        return self.query(BB_LOCATION_DETAILS_URL.format(**vars), method='GET')

    
    def devices(self, location_id, use_cached=True):
        """Return details on all devices at a location"""
        vars = {
            'site_id': location_id
        }
        return self.query(BB_DEVICE_LIST_URL.format(**vars), method='GET')

    def device(self, location_id, device_id):
        """Return details on a specific device"""
        vars = {
            'site_id': location_id,
            'device_id': device_id
        }
        return self.query(BB_DEVICE_STATUS_URL.format(**vars), method='GET')

    def turn_outlet_on(self, device_id, outlet_num):
        url = f"{BB_V2_API_PREFIX}/devices/{device_id}"
        self.query(url, extra_params={ "valve": { "target": "open" }})

    def turn_outlet_off(self, device_id, outlet_num):
        url = f"{BB_V2_API_PREFIX}/devices/{device_id}"
        self.query(url, extra_params={ "valve": { "target": "closed" }})
