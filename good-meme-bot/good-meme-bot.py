import sys
sys.path.append("..")
from utils.util import *
from fbchat import Client
from fbchat.models import *
import time, json
import string
import random

whitelist = input("Enter whitelist numbers, separated by commas: ").replace(" ", "").split(",")

response_message = ["ngl this is a pretty good meme","laughed aloud"]

class GoodMemeBot(Client):

    def __init__(self, uname, pwd):
        super().__init__(uname, pwd)
        self.salt = "".join(random.choice(string.ascii_letters) for i in range(5))
        
    def onMessage(self, mid, message, author_id, thread_id, ts, **kwargs):
        if thread_id not in whitelist:
            return
        print("MSG LEN: %d"%len(message.strip())) #status message
        if len(message.strip()) == 0: #lazy way of telling if it's an image
            for msg in response_message:
                self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
                time.sleep(0.1)
                
client = GoodMemeBot(*get_login_creds())
client.listen()

