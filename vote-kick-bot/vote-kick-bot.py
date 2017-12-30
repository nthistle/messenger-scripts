## VoteKickBot v1.0
## @author Jonathan Pollock, Neil Thistlethwaite
import sys
sys.path.append("..")
from utils.util import *
from fbchat.models import *
from fbchat import log, Client, ThreadType
import time



class VoteKickBot(Client):
	
	def __init__(self, email, password, vote_threshold=4):
		super().__init__(email, password)
		self.is_vote_active = {}
		self.active_chats = []
		self.current_votes = {}
		self.master_lookup = ({},{}) # name->id, id->name
		self.vote_threshold = vote_threshold

	def add_active_chat(self, new_chat_id):
		self.active_chats.append(new_chat_id)
		self.current_votes[new_chat_id] = {}
		self.is_vote_active[new_chat_id] = False
		
		chat_participants = [int(uid) for uid in self.fetchThreadInfo(new_chat_id)[str(new_chat_id)].participants]
		
		for participant_id in chat_participants:
			self.current_votes[new_chat_id][participant_id] = None
			
		new_master_ids = [pid for pid in chat_participants if pid not in self.master_lookup[1]]
		new_users_to_add = self.fetchUserInfo(*new_master_ids)
		for new_id in new_master_ids:
			self.master_lookup[0][new_users_to_add[str(new_id)].first_name.lower()] = new_id
			self.master_lookup[1][new_id] = new_users_to_add[str(new_id)].first_name.lower()
		
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		if int(thread_id) in self.active_chats:
			self.processActiveChatMessage(int(author_id), message_object, int(thread_id), thread_type)

	def processActiveChatMessage(self, author_id, message_object, thread_id, thread_type):
		if message_object.text.lower() == "!votekick":
			if self.is_vote_active[thread_id]:
				self.send(Message(text="There is already an Island Vote active"), thread_id=thread_id, thread_type=thread_type)
			else:
				self.send(Message(text="An Island vote has been called... Type someone's name to vote them off the island. Four votes means they will be leaving the island. Choose wisely"), thread_id=thread_id, thread_type=thread_type)
				self.is_vote_active[thread_id] = True
		elif self.is_vote_active[thread_id]:
			self.processVote(author_id, message_object, thread_id, thread_type)

	def capitalize_first(self, s):
		return s[0].upper() + s[1:].lower() if len(s)>0 else s

	def processVote(self, author_id, message_object, thread_id, thread_type):
		if message_object.text.lower() not in self.master_lookup[0]:
			return
		voted_for_id = self.master_lookup[0][message_object.text.lower()]
		if author_id not in self.master_lookup[1]:
			self.send(Message(text="User ID %d, you are not a registered voter."%int(author_id)), thread_id=thread_id, thread_type=thread_type)
		elif self.current_votes[thread_id][author_id] is None:
			# user hasn't voted yet
			self.current_votes[thread_id][author_id] = voted_for_id # votes for this id
			self.send(Message(text=("%s, you have voted for %s"%(self.capitalize_first(self.master_lookup[1][author_id]),
										     self.capitalize_first(message_object.text)))),
				  thread_id=thread_id, thread_type=thread_type)
			vote_count = 0
			for key in self.current_votes[thread_id]:
				if self.current_votes[thread_id][key] == voted_for_id:
					vote_count += 1
			self.send(Message(text=("%s now has %d votes"%(self.capitalize_first(message_object.text), vote_count))),
				  thread_id=thread_id, thread_type=thread_type)
			if vote_count >= self.vote_threshold:
				self.send(Message(text=("The Island has spoken. %s will be leaving. "%self.capitalize_first(message_object.text))),
					  thread_id=thread_id,thread_type=thread_type)
				self.removeUserFromGroup(voted_for_id, thread_id=thread_id)
		else:
			self.send(Message(text="%s, you have already voted. A vote is final."%self.capitalize_first(self.master_lookup[1][author_id])),
				  thread_id=thread_id, thread_type=thread_type)
			
			
vname = "VoteKickBot v1.1"
print("VotKickBot v1.1")
print("(C) 2017 Jonathan Pollock & Neil Thistlethwaite")
print("")
vkbot = VoteKickBot(*get_login_creds("Please Login"))
print()
print("What chat to run in?")
cid = int(input("Chat ID: "))
vkbot.add_active_chat(cid)
print("Chat has been added")
print()
vkbot.listen()
