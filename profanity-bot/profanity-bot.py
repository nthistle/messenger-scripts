## PROFANITYBot v0.1
## @author Ankur Mishra, Neil Thistlethwaite
## Possible major improvement: adding sentiment analysis to check if tone is aggressive
import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client
import time

profanity_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/MUTCD_R1-1.svg/2000px-MUTCD_R1-1.svg.png"
profanity_message = "This is a Christian Minecraft Server! Absolutely NO PROFANITY!"
alphabet = "abcdefghijklmnopqrstuvwxyz"

def format_word(word):
    return "".join(x for x in word.lower() if x in alphabet)

# assumes that word_list's contents have all been lowercased and stripped of punctuation
# returns True if there's a word in `message` that's in the word list, otherwise False
def check_message_against(message, word_list):
    stripped_message1 = "".join(x if x in alphabet else " " for x in message.lower())
    stripped_message2 = format_word(message)
    for word in stripped_message1.split():
        if word in word_list:
            return True
    for word in stripped_message2.split():
        if word in word_list:
            return True
    return False


# read the bad words from file into a set (dict with no values)
bad_words = {}
with open("badword.txt", "r") as bad_words_file:
    for word in bad_words_file:
        if len(word)<1:
            continue
        bad_words[format_word(word)] = None

        
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


    
class ProfanityBot(Client):
    
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # only do anything with it if it's in one of our allowed chats
        if author_id != self.uid and int(thread_id) in allowed_chats:
            self.markAsDelivered(author_id, thread_id)
            self.markAsRead(author_id)

            log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

            message_text = message_object.text.lower()
            if check_message_against(message_text, bad_words):
                self.respond_to_profanity(thread_id, thread_type)

    def respond_to_profanity(self, thread_id, thread_type):
        self.sendRemoteImage(profanity_image, message=Message(text=profanity_message), thread_id=thread_id, thread_type=thread_type)


# run our profanity bot
client = ProfanityBot(*get_login_creds())
client.listen()
