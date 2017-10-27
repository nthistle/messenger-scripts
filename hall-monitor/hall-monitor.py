# -*- coding: utf-8 -*-
# This is a bot which activates when a user types "!suspend <suspension time>"
# and floods the chat with white images until the suspension is over.
# TODO: add cooldown
import sys
sys.path.append("..")
from utils.util import *
from fbchat import Client
from fbchat.models import *
import time, sys, json

whitelist = ["<enter enabled chat IDs here>"]
f = open("namesjson.txt", "r")
names = json.loads(f.read())
f.close()
class HallMonitor(Client):
    def onMessage(self, mid, message, author_id, thread_id, ts, **kwargs):
        words = message.split(" ")
        if words[0].lower() == "!suspend" and author_id != self.uid and thread_id in whitelist:
            try:
                suspension = int(words[1])
                t = time.clock()
                client.sendRemoteImage("https://cdn11.ahalife.com/uploads/onboarding/images/kzsc37uuTFuZRSJ8OIB7_gallery-1000x1000-white.jpg", message=Message("This chat is now on a "+words[1]+" second suspension."), thread_id=thread_id, thread_type=ThreadType.GROUP)
                while time.clock() - t < suspension:
                    time.sleep(0.5)
                    client.sendRemoteImage("https://cdn11.ahalife.com/uploads/onboarding/images/kzsc37uuTFuZRSJ8OIB7_gallery-1000x1000-white.jpg", thread_id=thread_id, thread_type=ThreadType.GROUP)
                client.send(Message(text="That suspension is invalid."), thread_id=thread_id, thread_type=ThreadType.GROUP)

client = HallMonitor(*get_login_creds())
client.listen()
