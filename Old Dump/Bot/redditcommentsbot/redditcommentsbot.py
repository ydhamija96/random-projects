#Importing modules
from __future__ import print_function
import time
import praw

#Setting global stuff
REDDIT_USER_AGENT = "u/notWithThatSpirit comment reply bot v1.0 by Yogesh"
REDDIT_USERNAME = ""
REDDIT_PASSWORD = ""
SUBREDDIT = "funny"
NUM_POSTS = 50
DONE_FILE = "alreadyDone.txt"
ALREADY_DONE = []

def main():
	inst = 0;
	print("Reddit Bot")
	print()
	print()
	print()
	while True:
		inst = inst+1
		print("INSTANCE: ", end="")
		print(inst)
		try:
			oneCycle()
		except:
			print("     ERROR: Can't reply so often. (Probably. I'm not sure.)")
		print()
		print()
		print()
		print("Waiting 1 hour. PROGRESS:")
		print("------------------------------------------------------------|")
		for item in range(60):
			print("-", end="")
			time.sleep(60)
		print("|")
		print()
		print()

def oneCycle():
	"""This function will perform one cycle of the following tasks:
	log on to reddit
	cycle through the top ten posts
	in each post's comments, find ones that are replyable
	reply to those comments
	add the comment's id to ALREADY_DONE
	"""
	populateDone()
	doneThisCycle = []
	r = praw.Reddit(user_agent = REDDIT_USER_AGENT)
	r.login(REDDIT_USERNAME, REDDIT_PASSWORD)
	submissions = r.get_subreddit(SUBREDDIT).get_hot(limit=NUM_POSTS)
	for submission in submissions:
		print("TITLE::     %s" % (' '.join(submission.title.split())))
		if filter(submission):
			flat_comments = praw.helpers.flatten_tree(submission.comments)
			for comment in flat_comments:
				if isReplyable(comment):
					print("     COMMENT::     %s" % (' '.join(comment.body.split())))
					comment.reply("Not with that attitude!")
					comment.upvote()
					appendDone([""+comment.id])
					print("          STATUS::     Replied")
	ALREADY_DONE = []

def populateDone():
		"""This function will populate the ALREADY_DONE list
		with comment id's from the file DONE_FILE"""
		handle = open(DONE_FILE, 'r')
		for line in handle:
			ALREADY_DONE.append(line.strip())
		handle.close()

def appendDone(list):
		"""This function will append items in the provided list
		(theList) to the file DONE_FILE"""
		handle = open(DONE_FILE, 'a')
		for each in list:
			handle.write("\n"+each)
		handle.close()
		
def isReplyable(comment):
	"""This function, given a praw comment object (comment),
	will return True only if it passes all the following filters, 
	otherwise it returns False:
	the comment has not already been replied to by this program
	the comment fits with what we wanted to reply to"""
	if hasattr(comment, 'body'):
		if not textFits(comment.body):
			return False
		if comment.id in ALREADY_DONE:
			print("     COMMENT::     %s" % (' '.join(comment.body.split())))
			print("          STATUS::     Comment has already been replied to")
			return False
		return True
	else:
		return False
	
def textFits(text):
	"""This function will return True if the text either begins
	with "You can't " or contains ". You can't " (or any variations). Otherwise it 
	will return False."""
	text = text.lower()
	pronouns = ["you", "i", "we", "he", "she", "they"]
	triggers = ["can't", "cannot", "couldn't", "can not", "could not"]
	if len(text) < 100:
		for trigger in triggers:
			if ("s "+trigger in text):
				return True
		for pronoun in pronouns:
			for trigger in triggers:
				if ((". "+pronoun+" "+trigger) in text):
					return True
				length = len(pronoun)+len(trigger)+1
				if len(text)>=length:
					if((""+pronoun+" "+trigger) == text[:length]):
						return True
	return False
	
def filter(post):
	"""This function, given a praw submission object (post), will
	return True only if it passes all the following filters, otherwise
	it returns False:
	The post is not tagged as 'Serious'
	"""
	if isSerious(post):
		return False
	return True

def isSerious(post):
		"""This function will return True if the praw submission object
		(post) is tagged as 'Serious'."""
		if "[serious]" in post.title.lower():
			print("     STATUS::     Post is serious.")
			return True
		return False
	
	
main()
