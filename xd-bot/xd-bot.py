## PROFANITYBot v0.1
## @author Ankur Mishra, Neil Thistlethwaite
## Possible major improvement: adding sentiment analysis to check if tone is aggressive
import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client
import time

      
# set up the allowed chats to send/listen to
allowed_chats = {}

toggle_whitelist = input("Read chats from whitelist? [Y/n] ")
toggle_whitelist = len(toggle_whitelist)<1 or toggle_whitelist[0].lower()!="n"

if toggle_whitelist:
    # ask for whitelist filename and read from there
    whitelist_name = input("Whitelist filename? ")
    whitelist_name = whitelist_name if len(whitelist_name)>0 else "whitelist.txt"
    with open(whitelist_name, "r") as whitelist_file:
        for whitelist_chat in whitelist_file:
            if len(whitelist_chat)<1:
                continue
            allowed_chats[int(whitelist_chat)] = None
else:
    # ask for chats separated by commas, command line (entering only one chat works)
    print("Enter allowed chats, comma delimited:")
    allowed_chats_text = input().split(",")
    for allowable in allowed_chats_text:
        if len(allowable)<1:
            continue
        allowed_chats[int(allowable)] = None


class XDBot(Client):
    
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # only do anything with it if it's in one of our allowed chats
        if author_id != self.uid and int(thread_id) in allowed_chats:
            self.markAsDelivered(author_id, thread_id)
            self.markAsRead(author_id)
            
            time.sleep(0.1)
            self.send(Message(text="xd"), thread_id=thread_id, thread_type=thread_type)

# run our profanity bot
client = XDBot(*get_login_creds())
client.listen()
