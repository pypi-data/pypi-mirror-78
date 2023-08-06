# SalesForce API wrapper

# Installation

Install using `pip`...

    pip install salesforce-wrapper

Or

    git clone https://github.com/bzdvdn/salesforce-wrapper.git

    python3 setup.py

# Usage

```python
from salesforce import  SalesForceAPI as API
api = API("<your salesforce instance_url>", "<access_token>", "<refresh_token>") # init salaesforce api

users = api.user.list() # return list of users
user = api.user.get("<id>")
data = {"name": "test"}
new_user = api.user.create(data=data) # creating user


```

# TODO
* full documentation(all salesforce methods)
* examples
* async version
* tests
