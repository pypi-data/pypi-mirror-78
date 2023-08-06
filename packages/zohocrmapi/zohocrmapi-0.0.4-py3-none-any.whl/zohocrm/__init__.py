import time
import requests
# import json


class ZohoCRMOAuthToken:
    """Zoho access token."""

    access_token = None
    refresh_token = None
    api_domain = None
    token_type = None
    expiry_timestamp = None

    def __init__(self, json_data):
        """Initialize."""
        self.load_json(json_data)

    def to_json(self):
        """Output to JSON."""
        data = {
            'access_token': self.access_token,
            'api_domain': self.api_domain,
            'token_type': self.token_type,
            'expiry_timestamp': self.expiry_timestamp,
        }
        if self.refresh_token is not None:
            data['refresh_token'] = self.refresh_token
        return data

    def load_json(self, json_data):
        """Convert from JSON."""
        self.access_token = json_data['access_token']
        self.api_domain = json_data['api_domain']
        self.token_type = json_data['token_type']
        if 'expires_in' in json_data:
            self.expiry_timestamp = json_data['expires_in'] + time.time()
        if 'expiry_timestamp' in json_data:
            self.expiry_timestamp = json_data['expiry_timestamp']
        if 'refresh_token' in json_data:
            self.refresh_token = json_data['refresh_token']

    def is_expired(self):
        """Return True if this code is expired."""
        return time.time() >= self.expiry_timestamp


class ZohoCRMRestClient:
    """Zoho rest client."""

    api_base_url = 'https://www.zohoapis.com'
    api_version = 'v2'
    accounts_url = 'https://accounts.zoho.com'

    client_id = None
    client_secret = None
    redirect_uri = None

    oauth_access_token = None
    oauth_refresh_token = None

    def __init__(self, client_id, client_secret, redirect_uri):
        """Initialize REST client."""
        self.client_id = client_id,
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def generate_access_token(self, grant_token):
        """Generate access token."""
        url = '{accounts_url}/oauth/{api_version}/token'.format(
            accounts_url=self.accounts_url,
            api_version=self.api_version
        )
        post_parameters = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': grant_token,
        }
        response = requests.post(url, data=post_parameters)
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                access_token = ZohoCRMOAuthToken(response.json())
                return access_token
            else:
                raise ValueError(response_json['error'])
        else:
            raise ValueError(response_json['message'])

    def generate_refresh_token(self):
        """Generate access token."""
        url = '{accounts_url}/oauth/{api_version}/token'.format(
            accounts_url=self.accounts_url,
            api_version=self.api_version
        )
        query_parameters = {
            'refresh_token': self.oauth_access_token.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }
        response = requests.post(url, params=query_parameters)
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4))
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                access_token = ZohoCRMOAuthToken(response.json())
                return access_token
            else:
                raise ValueError(response_json['error'])
        else:
            raise ValueError(response_json['message'])

    def is_logged_in(self, access_token):
        """Return true if access_token is active."""
        return access_token.is_expired() is False

    def api_fetch(self, endpoint, method='GET', headers=None, params=None, json_data=None):
        """Fetch from endpoint."""
        url = '{api_base_url}/crm/{api_version}/{endpoint}'.format(
            api_base_url=self.api_base_url,
            api_version=self.api_version,
            endpoint=endpoint
        )
        if headers is None:
            headers = {}
        if self.oauth_refresh_token is None:
            headers['Authorization'] = 'Zoho-oauthtoken {}'.format(self.oauth_access_token.access_token)
        else:
            headers['Authorization'] = 'Zoho-oauthtoken {}'.format(self.oauth_refresh_token.access_token)
        response = requests.request(
            method,
            url=url,
            headers=headers,
            params=params,
            json=json_data
        )
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4))
        return response


class ZohoCRMRecord:
    """Zoho Record."""

    _record_type = ''
    _rest_client = None

    def __init__(self, zoho_rest_client):
        """Initialize."""
        self._rest_client = zoho_rest_client

    def clear(self):
        """Clean the object."""
        for property, value in vars(self).items():
            if property[0] != '_':
                setattr(self, property, None)

    def to_json(self):
        """To JSON."""
        data = {}
        for property, value in vars(self).items():
            if property[0] != '_':
                data[property] = value
        return data

    def from_json(self, json_data):
        """From JSON."""
        for key, value in json_data.items():
            setattr(self, key, value)

    def save(self):
        """Save contact."""
        if hasattr(self, 'id') and self.id is not None:
            self.update()
        else:
            self.insert()

    def insert(self):
        """Insert."""
        data = {}
        for property, value in vars(self).items():
            if property[0] != '_':
                data[property] = value
        # print(json.dumps({'data': [data]}, indent=4))
        response = self._rest_client.api_fetch(
            '{record_type}'.format(record_type=self._record_type),
            method='POST',
            json_data={'data': [data]}
        )
        if response.status_code == 201:
            response_json = response.json()
            self.id = response_json['data'][0]['details']['id']
        else:
            raise ValueError(response.json()['message'])

    def update(self):
        """Update."""
        data = self.to_json()
        response = self._rest_client.api_fetch(
            '{record_type}/{record_id}'.format(record_type=self._record_type, record_id=self.id),
            method='POST',
            json_data=data
        )
        if response.status_code != 201:
            raise ValueError(response.json()['message'])

    def delete(self):
        """Delete."""
        response = self._rest_client.api_fetch(
            '{record_type}/{record_id}'.format(record_type=self._record_type, record_id=self.id),
            method='DELETE'
        )
        if response.status_code == 200:
            self.id = None
        else:
            raise ValueError(response.json()['message'])

    @classmethod
    def fetch(cls, zoho_rest_client, id):
        """Fetch by ID."""
        print(cls._record_type)
        obj = cls(zoho_rest_client)
        response = zoho_rest_client.api_fetch(
            '{record_type}/{id}'.format(record_type=cls._record_type, id=id),
            method='GET'
        )
        if response.status_code == 200:
            obj.from_json(response.json()['data'][0])
            return obj
        else:
            raise ValueError(response.json()['message'])

    @classmethod
    def delete_id(cls, zoho_rest_client, id):
        """Delete from ID."""
        response = zoho_rest_client.api_fetch(
            '{record_type}/{record_id}'.format(record_type=cls._record_type, record_id=id),
            method='DELETE'
        )
        if response.status_code != 200:
            raise ValueError(response.json()['message'])


class ZohoCRMUser(ZohoCRMRecord):
    """Zoho CRM User."""

    _record_type = 'users'
    _rest_client = None

    def fetch_current_user(self, access_token):
        """Fetch current User."""
        self.clear()
        response = self._rest_client.api_fetch(
            access_token,
            'users',
            params={
                'type': 'CurrentUser'
            }
        )
        if response.status_code == 200:
            self.from_json(response.json()['users'][0])
        else:
            raise ValueError(response.json()['message'])

    def fetch_user(self, access_token, user_id):
        """Fetch User."""
        self.clear()
        response = self._rest_client.api_fetch(
            access_token,
            'users/{user_id}'.format(user_id=user_id),
        )
        if response.status_code == 200:
            self.from_json(response.json()['users'][0])
        else:
            raise ValueError(response.json()['message'])


class ZohoCRMContact(ZohoCRMRecord):
    """Zoho CRM Contact."""

    _record_type = 'Contacts'


class ZohoCRMVendor(ZohoCRMRecord):
    """Zoho CRM Vendor."""

    _record_type = 'Vendors'


class ZohoCRMLead(ZohoCRMRecord):
    """Zoho CRM Lead."""

    _record_type = 'Leads'


class ZohoCRMAccount(ZohoCRMRecord):
    """Zoho CRM Account."""

    _record_type = 'Deal'


class ZohoCRMDeal(ZohoCRMRecord):
    """Zoho CRM Account."""

    _record_type = 'Deals'


class ZohoCRMCampaign(ZohoCRMRecord):
    """Zoho CRM Campaign."""

    _record_type = 'Campaigns'


class ZohoCRMTask(ZohoCRMRecord):
    """Zoho CRM Task."""

    _record_type = 'Tasks'


class ZohoCRMCase(ZohoCRMRecord):
    """Zoho CRM Case."""

    _record_type = 'Cases'


class ZohoCRMEvent(ZohoCRMRecord):
    """Zoho CRM Event."""

    _record_type = 'Events'


class ZohoCRMCall(ZohoCRMRecord):
    """Zoho CRM Call."""

    _record_type = 'Calls'


class ZohoCRMSolution(ZohoCRMRecord):
    """Zoho CRM Solution."""

    _record_type = 'Solutions'


class ZohoCRMProduct(ZohoCRMRecord):
    """Zoho CRM Product."""

    _record_type = 'Products'


class ZohoCRMQuote(ZohoCRMRecord):
    """Zoho CRM Quote."""

    _record_type = 'Quotes'


class ZohoCRMInvoice(ZohoCRMRecord):
    """Zoho CRM Invoice."""

    _record_type = 'Invoices'


class ZohoCRMCustom(ZohoCRMRecord):
    """Zoho CRM Custom."""

    _record_type = 'Custom'


class ZohoCRMActivity(ZohoCRMRecord):
    """Zoho CRM Activity."""

    _record_type = 'Activities'


class ZohoCRMPriceBook(ZohoCRMRecord):
    """Zoho CRM Price Book."""

    _record_type = 'pricebooks'


class ZohoCRMSalesOrder(ZohoCRMRecord):
    """Zoho CRM Sales Order."""

    _record_type = 'salesorders'


class ZohoCRMPurchaseOrder(ZohoCRMRecord):
    """Zoho CRM Purchase Order."""

    _record_type = 'purchaseorders'


class ZohoCRMNote(ZohoCRMRecord):
    """Zoho CRM Note."""

    _record_type = 'notes'
