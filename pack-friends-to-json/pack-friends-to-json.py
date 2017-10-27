from fbchat import Client
from fbchat.models import *
import json

client = Client("<username>", "<password>")

table = {}
users = client.fetchAllUsers()

for user in users:
    #converts from special type to direct string lookup
    try:
        table[str(user.name)] = user.uid
    except UnicodeEncodeError:
        table[user.name] = user.uid

# use this lookup table in another program by reading the file and calling json.loads()
f = open("namesjson.txt", "w")
f.write(json.dumps(table))
f.close()
