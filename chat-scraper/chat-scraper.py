## Chat Scraper v1.0
## @author Neil Thistlethwaite
import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client, ThreadType
import time

print("Chat Scraper v1.0")
print("(C) 2017 Neil Thistlethwaite")
print("")

def get_target_chats(client):
    target_list = []
    while True:
        print("Current list of target chats has %d chats" % len(target_list))
        print("Choose action")
        print("[C]onfirm targets")
        print("Add targets by [I]D")
        print("[S]earch for targets by name")
        choice = input("> ")
        
