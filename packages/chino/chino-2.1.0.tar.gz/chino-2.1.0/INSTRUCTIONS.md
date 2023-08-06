#  CHINO.io Python client <!-- omit in toc -->

*Official* Python wrapper for **CHINO.io** API,

Docs is available [here](http://docs.chino.io)

- - -
### Table of Content <!-- omit in toc -->
- [Usage instructions](#usage-instructions)
  - [API client](#api-client)
      - [requests.Session()](#requestssession)
    - [AUTH](#auth)
    - [User](#user)
    - [Group](#group)
    - [Permission](#permission)
    - [Repository](#repository)
    - [Schemas](#schemas)
    - [Document](#document)
    - [BLOB](#blob)
    - [SEARCH](#search)
    - [UserSchemas](#userschemas)
    - [Collections](#collections)
    - [Consents](#consents)
    - [OTHER](#other)
      - [`_id`](#id)
      - [DOC](#doc)
  - [For contributions:](#for-contributions)
    - [Build for pip (internal notes)](#build-for-pip-internal-notes)

- - -

## Install via pip

`pip install chino`

# Usage instructions

## API client
First create a variable from the `ChinoApiClient` class, passing your `customer_id` and `customer_key`. This will give you access to the API.

### Customer credentials <!-- omit in toc -->
If you are using the API as an admin:

```python
from chino.api import ChinoAPIClient
chino = ChinoAPIClient("your-customer-id", customer_key="your-customer-key")
```

### OAuth (Bearer Token) <!-- omit in toc -->
If you are using the API on behalf of a User that sent a `access_token`:

```python
from chino.api import ChinoAPIClient
chino = ChinoAPIClient("your-customer-id", access_token="user-access-token")
```

- - -

**Parameters**

-`customer_id` : the Customer ID of the Chino.io platform
-`customer_key` : (*optional*) one of the Customer Keys associated to your ID
-`access_token`:  (*optional*) a OAuth Bearer Token sent by a user.
**NOTE:  if `customer_key` is set, API calls are authenticated as admin (Customer). If `access_token` is set, the authentication is of a User.**
Admin has precedence in case both are set.

-`url`: the API URL you are targeting, default is the **production** API: `https://api.chino.io/`. You can also use the **test** API URL `https://api.test.chino.io`.
-`version`: the version of the API. Currently we only have `v1`
-`timeout`: timeout for the requests in seconds, default is `30`. You'll get an exception if any API request takes more than this.
- `session`: default: `True`. See section below.

#### requests.Session()
To improve the performances the Python SDKs uses `requests` and [`requests.Session()`](http://docs.python-requests.org/en/master/user/advanced/?highlight=session). The session keeps the connection open and does not add overhead on the request.
This has a *huge* improvment in the performances. It's 4 times faster!
You can, however, disable this functionality setting `session=False` when creating the `ChinoAPIClient()`

### AUTH
Class that manages the auth, `chino.auth`. **In 99% of the cases this class does not need to be used.**

- `init`:
    -`customer_id` : the Customer ID of the Chino.io platform
    -`customer_key` : (*optional*) one of the Customer Keys associated to your ID
    -`access_token`:  (*optional*) a OAuth Bearer Token sent by a user.
**NOTE:  if `customer_key` is set, API calls are authenticated as admin (Customer). If `access_token` is set, the authentication is of a User.**
Admin has precedence in case both are set.
- `set_auth_admin` to set the auth as admin
- `set_auth_user` to set the auth as the user
- `get_auth` to get the Auth object


### User
Class to manage the user, `chino.users`

- `login`
- `current`
- `logout`
- `list`
- `detail`
- `create`
- `update`
- `partial_update`
- `delete`

### Group
`chino.groups`

- `list`
- `detail`
- `create`
- `update`
- `delete`
- `add_user`
- `del_user`

### Permission
`chino.permissions`

- `resources`
- `resource`
- `resource_children`
- `read_perms`
- `read_perms_doc`
- `read_perms_user`
- `read_perms_group`

### Repository
`chino.repotiories`

- `list`
- `detail`
- `create`
- `update`
- `delete`

### Schemas
`chino.schemas`

- `list`
- `create`
- `detail`
- `update`
- `delete`

### Document
`chino.documents`

- `list`
- `create`
- `detail`
- `update`
- `delete`


### BLOB
`chino.blobs`

- `send`: help function to upload a blob, returns `BlobDetail('bytes', 'blob_id', 'sha1', 'document_id', 'md5')`
- `start`
- `chunk`
- `commit`
- `detail`: returns `Blob(filename, content)``
- `delete`

### SEARCH
`chino.searches`

- `search`: **Note: to be tested**

### UserSchemas
`chino.user_schemas`

- `list`
- `create`
- `detail`
- `update`
- `delete`

### Collections
`chino.collections`

- `list`
- `create`
- `detail`
- `update`
- `delete`
- `list_documents`
- `add_document`
- `rm_document`
- `search`

### Consents
`chino.consents`

- `list`
- `create`
- `detail`
- `history`
- `update`
- `withdraw`
- `delete` (only available for test API)

### OTHER
*Plus methods that are utils for auth and to manage communications*

**Note**

The calls returns Objects (see `object.py`) of the type of the call (e.g. `documents` return Documents) or raise an Exception if there's an error. Thus, you can catch the Exception in the code if something bad happens.
In case of `list` it reutrns a ListResult, which is composed of:
- `paging`:
    - `offest`: int
    - `count`: int
    - `total_count`: int
    - `limit`: int
- `documents` *(name of the object in plural)*: list *(the actual list of objects)*

**all the objects, except Blob and BlobDetail have a method to be transformed into a dict (`obj.to_dict()`) and to read the id (`obj.id`)**

#### ID: `_id`
each element has a `_id()` function that returns the `id` of the entity


### Iterating
from version `2.0` all the `Paginated Results` can be iterated using its returned object, example:
```python
repositories=chino.repositories.list()
for repo in repositories:
    print(repo)
```

#### DOC
Not completed. Can be compiled with [sphinx](sphinx-doc.org).

requires the following package (via pip)

- sphinx-autobuild
- sphinx-autodoc-annotation
- sphinx-rtd-theme

## For contributions:

See [CONTRIBUTING.md](./CONTRIBUTING.md)

### Build for pip (internal notes)

    rm -r dist/*
    python setup.py bdist_wheel --universal
    twine upload dist/*
