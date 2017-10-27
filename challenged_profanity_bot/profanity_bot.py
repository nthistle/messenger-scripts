## PROFANITYBot v0.1
## @author Ankur Mishra

## Lazily coded so the bot is a little challenged
## Suggested Improvements
### Add Sentiment Analysis to check if term with aggressive tone
### Don't simply check if the word is in string ==> split string into set and then check if badword is in there
## too lazy to add these changes right now

from fbchat.models import *
from fbchat import log, Client
import time
import getpass

f = open('badword.txt', 'r')
l = f.read().split('\n')
filterchats = set(["1200858710014578","1752000458175873", "1329465697176406"]) # filter doesnt work

class ResponseBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        s = message_object.text.lower()

        for i in l:
            if len(i) > 0 and i in s and author_id != self.uid and thread_id not in filterchats:
                print(i)
                self.sendRemoteImage('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/MUTCD_R1-1.svg/2000px-MUTCD_R1-1.svg.png', message=Message(text='This is a Christian Minecraft Server! Absolutely NO PROFANITY!'), thread_id=thread_id, thread_type=thread_type)
                return

email = input("Please enter your FaceBook email.\n")
client = ResponseBot(email, getpass.getpass())
client.listen()
