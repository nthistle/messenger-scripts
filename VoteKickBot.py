import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client, ThreadType
import time

vname = "VoteKickBot v1.0"
print("VotKickBot v1.0")
print("(C) 2017 Jonathan Pollock")
print("")
cli = get_user_client("Please Login")
cid = int(input("Chat ID: "))
group_info = cli.fetchGroupInfo(cid)[str(cid)]

ayy=0;
for user in group_info.participants:
	print(cli.fetchUserInfo(user)[str(user)].first_name)
	ayy=ayy+1

w, h = ayy, 3;
matrix = [[0 for x in range(w)] for y in range(h)] 
	
i=0;
for user in group_info.participants:
	name = cli.fetchUserInfo(user)[str(user)].first_name
	matrix[2][i] = name
	matrix[1][i] = user
	matrix[0][i] = 0
	i=i+1
	
	

class VoteKickBot(Client):	
	def __init__(self, email, password):
		super().__init__(email, password)
		self.check = False;
		
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		if message_object.text == '!VoteKick' and thread_type == ThreadType.GROUP:
			self.send(Message(text='An Island vote has been called... Type someones first name to vote them off the island. Four votes means they will be leaving the island. This is case sensitive btw.'), thread_id=thread_id, thread_type=thread_type)
			self.check = True
		if self.check:
			for user in group_info.participants:
				if message_object.text == str(cli.fetchUserInfo(user)[str(user)].first_name) and message_object.text != 'Jonathan':
					x=0;
					while(x<ayy):
						if matrix[2][x] == message_object.text:
							temp = int(matrix[0][x])
							temp=temp+1
							matrix[0][x] = temp
							self.send(Message(text='Sorry, '+message_object.text+' you have '+str(temp)+' vote(s)'), thread_id=thread_id, thread_type=thread_type)
							if(temp==4):
								self.send(Message(text='Sorry.. The Island has spoken.'), thread_id=thread_id, thread_type=thread_type)
								self.removeUserFromGroup(int(matrix[1][x]), thread_id=thread_id)
								self.check=False
						x=x+1;
			
			

client = VoteKickBot("Type Email", "Type Password")
client.listen()