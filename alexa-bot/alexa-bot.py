## AlexaBot v0.1
## @author Ankur Mishra, Neil Thistlethwaite
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


class AlexaBot(Client):
    
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # only do anything with it if it's in one of our allowed chats
        title = "ɴᴏᴡ ᴘʟᴀʏɪɴɢ:"

        end_title= """
        ───────────⚪────────────────────────────────

        ◄◄⠀▐▐ ⠀►►⠀⠀ ⠀ 1:17 / 4:20 ⠀ ───○ 🔊⠀ ᴴᴰ ⚙.
        """
        if  int(thread_id) in allowed_chats:
            self.markAsDelivered(author_id, thread_id)
            self.markAsRead(author_id)
            
            time.sleep(0.1)
            lower_mess = message_object.text.lower()
            if "alexa play despacito 2" == lower_mess:
                song = " Despacito 2 (ft. Lil Pump)"
                self.changeThreadTitle(title + song + end_title, thread_id=thread_id, thread_type=thread_type)
            elif "alexa play" == lower_mess:
                self.send(Message(text="Play what you bitch?"), thread_id=thread_id, thread_type=thread_type)
            elif "alexa play" in lower_mess:
                print("alexa")
                song = message_object.text[lower_mess.index("play")+4:]
                self.changeThreadTitle(title + song + end_title, thread_id=thread_id, thread_type=thread_type)
           
# run our alexa
client = AlexaBot(*get_login_creds())
client.listen()
