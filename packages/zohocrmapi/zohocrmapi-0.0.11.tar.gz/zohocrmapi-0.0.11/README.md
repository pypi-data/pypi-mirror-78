# Zoho CRM API
This API is for people who are having trouble with the official Zoho API. 

* Supports Zoho API v2

For full documentation visit [zoho-crm-api.readthedocs.io](https://zoho-crm-api.readthedocs.io).

## Quickstart

Install:

```
$ pip install zohocrmapi
```

Get a Client ID, Client Secret, and Grant Token from Zoho, then create a `ZohoCRMRestClient` object and generate an access token:

```python
from zohocrm import ZohoCRMRestClient

client_id = '<paste your Zoho client id>'
client_secret = '<paste your Zoho client secret>'
redirect_uri = '<paste your Redirect URL>'
grant_token = '<paste your newly created token>'
zoho_client = ZohoCRMRestClient(client_id, client_secret, redirect_uri)

zoho_client.generate_access_token(grant_token)
```

Download a Record from the API, for example a Contact:

```python
from zohocrm import ZohoCRMContact

contact_id = 1234023423424
contact = ZohoCRMContact.fetch(
    zoho_client,
    contact_id
)
```

Create a new record:

```python
contact = ZohoCRMContact(zoho_client)
contact.Last_Name = "John"
```

Update or save a Record:

```python
# no id? insert
contact.save()  # or contact.insert()

# id = <int>? update
contact.id = 12232423423
contact.save()  # or contact.update()
```

Delete a Record:

```python
# delete loaded record
contact.delete()

# delete non-loaded record from ID
ZohoCRMContact.delete_id(zoho_client, contact_id)
```
