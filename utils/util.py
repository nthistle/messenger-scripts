## Utils
from getpass import getpass
from fbchat import *
from fbchat.models import *

## Collects login credentials from command line in a safe way,
## without displaying the password as you type it (usually)
## *NOT RECOMMENDED* to set safe_pass=False
def get_login_creds(prompt=None, safe_pass=True):
    if prompt:
        print(prompt)
    email = input("Email Address: ")
    password = getpass("Password: ") if safe_pass else input("Password: ")
    return (email, password)

## Calls get_login_creds, and uses them to create a client. This
## is mostly intended as an example for best practice to do this,
## for instantiating custom Client subclasses as well, so that
## your password is never saved in a local variable somewhere.
def get_user_client(prompt=None):
    return Client(*get_login_creds(prompt))
