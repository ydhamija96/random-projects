#!/usr/bin/python

#Importing modules
import sys
import random
import json
import urllib2
import urllib
import tweepy
import time
import datetime

#Log in to twitter
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Makes sure the word isn't from a twitter handle
def excludenamefunc(word, string):
	if '@' in string:
		if string.find('@')<string.find(word):
			if ' ' in string[string.find('@')+1:string.find(word)]:
				return True
	return False

#Find recent tweets
word = "color"
search = api.search(q=word)
for item in search:
	if word in item.text:
		if(excludenamefunc(word, item.text)):
			if item.text[0:2] != "RT":
				if (time.time() - (item.created_at - datetime.datetime(1970,1,1)).total_seconds())<600:
					name = item.user.screen_name
					reply = '@{}: '.format(name)
					reply = reply+"It's spelt 'colour'. Pssh Yankee English."
					print reply
					api.update_status(reply, item.id)
