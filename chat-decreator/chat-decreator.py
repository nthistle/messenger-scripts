## Chat De-Creator v1.1
## @author Ankur Mishra, Neil Thistlethwaite
## based off of Neil's Chat Re-Creator

import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client, ThreadType
import time

vname = "De-Creator v1.1"
print("Chat De-Creator v1.0")
print("(C) 2017 Ankur Mishra, Neil Thistlethwaite")
print("")

# Authenticate
cli = get_user_client("Please Login")

# Ask for Group Chat ID to re-create
cid = int(input("Chat ID: "))

# Send info messages
cli.send(Message(text=("%s initiated, destroying this chat..."%vname)),
         thread_id=cid, thread_type=ThreadType.GROUP)

time.sleep(0.2)

time.sleep(0.1)

group_info = cli.fetchGroupInfo(cid)[str(cid)]

for user in group_info.participants:
    if user==cli.uid:
        continue
    try:
        cli.removeUserFromGroup(int(user), thread_id=cid)
        sleep(0.2)
    except:
        pass

cli.removeUserFromGroup(int(cli.uid), thread_id=cid)

print("Chat de-creation process completed")
