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
        print("Choose action: ")
        print("[C]onfirm targets")
        print("Add targets by [I]D")
        print("[S]earch for targets by group name")
        choice = input("> ")
        choice = choice[0].lower() if len(choice)>0 else None
        if choice == "c":
            return target_list
        elif choice == "i":
            print("Enter target IDs separated by commas: ")
            new_targets_raw = [int(t) for t in input("> ").split(",")]
            new_targets = [t for t in new_targets_raw if t not in target_list]
            target_list += new_targets
            print("%d new targets added to list" % len(new_targets))
            if len(new_targets)!=len(new_targets_raw):
                print("%d were not added because they were duplicates" % (len(new_targets_raw)-len(newtargets)))
        elif choice == "s":
            print("Enter search query: ")
            query = input("> ")
            results = client.searchForGroups(query, limit=30)
            for i in range(len(results)):
                print("{0: >2}: {}, '{}'".format(i+1,results[i].uid,results[i].name))
            print("Choose action: ")
            print("Add [A]ll")
            print("Add [N]one")
            print("Add [S]pecific")
            subchoice = input("> ")
            subchoice = subchoice[0].lower() if len(subchoice)>0 else None
            if subchoice == "a":
                new_targets = [int(t.uid) for t in results if int(t.uid) not in target_list]
                target_list += new_targets
                print("%d new targets added to list" % len(new_targets))
                if len(new_targets)!=len(results):
                    print("%d were not added because they were duplicates" % (len(results)-len(new_targets)))
            elif subchoice == "s":
                print("Sorry, not currently implemented")
            elif subchoice != "n":
                print("Error, action not understood")
            if subchoice != "a":
                print("No targets added to list")
        else:
            print("Error, action not understood")
            
        
