## Chat Scraper v1.0
## @author Neil Thistlethwaite
import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client, ThreadType
import time
import requests
import os

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
        print("[L]ist current targets")
        choice = input("> ")
        choice = choice[0].lower() if len(choice)>0 else None
        print()
        if choice == "c":
            return target_list
        elif choice == "i":
            print("Enter target IDs separated by commas: ")
            input_targets = input("> ")
            if len(input_targets) > 0:
                new_targets_raw = [int(t) for t in input_targets.split(",")]
                new_targets = [t for t in new_targets_raw if t not in target_list]
                target_list += new_targets
                print("%d new targets added to list" % len(new_targets))
                if len(new_targets)!=len(new_targets_raw):
                    print("%d were not added because they were duplicates" % (len(new_targets_raw)-len(new_targets)))
        elif choice == "s":
            print("Enter search query: ")
            query = input("> ")
            results = client.searchForGroups(query, limit=30)
            for i in range(len(results)):
                print("{0: >2}: {1}, '{2}'".format(i+1,results[i].uid,results[i].name))
            print()
            print("Choose action: ")
            print("Add [A]ll")
            print("Add [N]one")
            print("Add [S]pecific")
            subchoice = input("> ")
            subchoice = subchoice[0].lower() if len(subchoice)>0 else None
            print()
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
        elif choice == "l":
            for i in range(len(target_list)):
                print("{0: >2}: {1}".format(i+1,target_list[i]))
            print()
            subchoice = input("Show detailed? [y/N] ")
            if len(subchoice)>0 and subchoice[0].lower()=="y":
                info = client.fetchThreadInfo(*target_list)
                for i in range(len(target_list)):
                    print("{0: >2}: {1}, '{2}' ({3} participants)".format(i+1,target_list[i],info[str(target_list[i])].name,
                                                                          len(info[str(target_list[i])].participants)))
        else:
            print("Error, action not understood")
        print()
            
        
# Authenticate
cli = get_user_client("Please Login")

targets = get_target_chats(cli)

print()
print("Base directory to save in?" )
basedir = input("> ")

if not os.path.exists(basedir):
    os.mkdir(basedir)

for i in range(len(targets)):
    target = targets[i]
    currentdir = os.path.join(basedir, str(target))
    os.mkdir(currentdir)
    print("Fetching messages from chat #%d... (%d)" % (i+1, target))
    messages = cli.fetchThreadMessages(thread_id=target, limit=100000) # max 100,000 messages
    print()
    print("Locating image URLs...")
    img_urls = []
    for j in range(len(messages)):
        message = messages[j]
        try: 
            if len(message.attachments) == 0:
                continue
            for k in range(len(message.attachments)):
                attachment = message.attachments[k]
                try:
                    img_urls.append((attachment.large_preview_url,j,k))
                except:
                    pass
        except:
            pass
    print("%d image URLs loaded"%len(img_urls))
    print()
    print("Downloading images...")
    failures = 0
    for j in range(len(img_urls)):
        print("\r{0:.2f}%\r".format(100*j/len(img_urls)), end="\r")
        url = img_urls[j]
        try:
            ext = ".png" if ".png" in url[0].lower() else ".jpg"
            file = open(os.path.join(currentdir, ("%06d_%02d"%url[1:])+ext),'wb')
            file.write(requests.get(url[0]).content)
            file.close()
        except:
            failures += 1
    print()
    if failures > 0:
        print("%d failures occcurred" % failures)
    print()
print("Done downloading the images from all targets")
