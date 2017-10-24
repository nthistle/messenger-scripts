## Chat Re-Creator v1.0
## @author Neil Thistlethwaite
import getpass
from fbchat.models import *
from fbchat import log, Client, ThreadType
import time

vname = "RecreateBot v1.0"
print("Chat Re-Creator v1.0")
print("(C) 2017 Neil Thistlethwaite")
print("")

# Authenticate
print("Please Login")
email = input("Email: ")
password = getpass.getpass("Password: ")
cli = Client(email,password)

# Ask for Group Chat ID to re-create
cid = int(input("Chat ID: "))

# Ask for Group Chat ID to use as new chat
newcid = int(input("New Chat ID: "))

# Send info messages
cli.send(Message(text=("%s initiated, recreating this chat..."%vname)),
         thread_id=cid, thread_type=ThreadType.GROUP)

time.sleep(0.2)

cli.send(Message(text=("%s initiated, recreating into this chat..."%vname)),
         thread_id=newcid, thread_type=ThreadType.GROUP)

time.sleep(0.1)

# Fetch old group info
group_info = cli.fetchGroupInfo(cid)[str(cid)]

# Fetch new group info, to check against double-adding, and verify it exists
ngroup_info = cli.fetchGroupInfo(newcid)[str(newcid)]

# Add all the users to new chat
users_to_add = [user for user in group_info.participants
                     if user not in ngroup_info.participants]
if len(users_to_add)>0:
    cli.addUsersToGroup(users_to_add, newcid)
time.sleep(0.25)

# Set the new chat's name
cli.changeThreadTitle(group_info.name, thread_id=newcid, thread_type=ThreadType.GROUP)
time.sleep(0.25)

# Set all the nicknames
old_nicks = group_info.nicknames
for uid in old_nicks:
    if uid in group_info.participants:
        cli.changeNickname(old_nicks[uid], int(uid), thread_id=newcid,
                           thread_type=ThreadType.GROUP)
        time.sleep(0.1)
time.sleep(0.5)

# Set chat emoji
cli.changeThreadEmoji(group_info.emoji, thread_id=newcid)
time.sleep(0.2)

# Set chat colors
cli.changeThreadColor(group_info.color, thread_id=newcid)
time.sleep(0.2)

# Upload the chat photo for someone to change manually
#cli.sendRemoteImage(group_info.photo, thread_id=newcid, thread_type=ThreadType.GROUP)
# doesn't work, let's just send the photo link
cli.send(Message(text=group_info.photo), thread_id=cid, thread_type=ThreadType.GROUP)
time.sleep(0.2)

# Tell the chat that process is done
cli.send(Message(text="Chat recreation has been completed"), thread_id=cid,
         thread_type=ThreadType.GROUP)
time.sleep(0.15)
cli.send(Message(text="Chat recreation has been completed"), thread_id=newcid,
         thread_type=ThreadType.GROUP)
time.sleep(1.0)

# Tell the old chat it's getting demolished
cli.send(Message(text="This chat will now be destroyed"), thread_id=cid,
         thread_type=ThreadType.GROUP)
time.sleep(2.0)

for user in group_info.participants:
    try:
        cli.removeUserFromGroup(int(user), thread_id=cid)
        sleep(0.2)
    except:
        pass

print("Chat recreation process completed")
