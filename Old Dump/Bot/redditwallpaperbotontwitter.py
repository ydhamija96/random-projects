#!/usr/bin/python

#Importing modules
from __future__ import print_function
import sys
import random
import json
import urllib2
import urllib
import tweepy
import time
import datetime

REDDIT_URL = "http://www.reddit.com/r/wallpapers/top/.json?sort=top&t=hour"
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_KEY = ''
TWITTER_ACCESS_SECRET = ''
PHRASE_TO_SEARCH_ON_TWITTER = "@redditwalls"
PHRASES_TO_MATCH_ON_TWITTER = ["@redditwalls", "wallpaper"]
AGE_OF_TWEETS_TO_SEARCH = 3600

#New Redirect Handler
class NoRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		infourl = urllib.addinfourl(fp, headers, req.get_full_url())
		infourl.status = code
		infourl.code = code
		return infourl
	http_error_300 = http_error_302
	http_error_301 = http_error_302
	http_error_303 = http_error_302
	http_error_307 = http_error_302

def filterfunc(data):
	"""Make sure data is an image URL.
	Parameters -> 
		data (url) [str]"""
	if data[-3:] == 'png' or data[-3:] == 'jpg' or \
	data[-4:] == 'jpeg' or data[-3:] == 'bmp' or \
	data[-3:] == 'gif':
		return True
	return False

def getInReddit():
	"""This will return Reddit Json from a specified URL: REDDIT_URL"""
	url = REDDIT_URL
	data = json.load(urllib2.urlopen(url))
	return data
	
def confirmRedditUrl(url, urls, author, authors, number, iteration = 1):
	"""Use redirect handler class to check if the Reddit URL 
	redirects. If it does, it chooses a different Reddit URL.
	Parameters ->
		url (the url to check) [str]
		urls (all urls available) [list]
		author (the reddit username of that url) [str]
		authors (all reddit usernames available) [list]
		number (the number of elements in urls and authors) [int]
		iteration = 1 [int]
	If it undergoes over 10 interations, then it will end the program.
	Dependencies ->
		getRandomFromLists()"""
	if iteration > 10:
		print('Too many 404 links')
		sys.exit()
	opener = urllib2.build_opener(NoRedirectHandler())
	urllib2.install_opener(opener)
	response = urllib2.urlopen(url)
	if response.code in (300, 301, 302, 303, 307):
		url, author = getRandomFromLists(number, urls, authors)
		return confirmRedditUrl(url, \
								urls, \
								author, \
								authors, \
								number, \
								iteration+1)
	else:
		return [url, author, iteration]
	
def lengthfunc(final, urls, authors, number, name):
	"""This function will make sure the length of the 
	first parameter is less than 140 characters.
	If not, it will try to shorten it. If it can't, 
	it will re-assign the variable using other functions
	and try again.
	Parameters ->
		final (url and author) [list]
		urls (all urls) [list]
		authors (all authors) [list]
		number (number of urls and authors) [int]
		name (twitter username) [str]
	Other functions used ->
		confirmRedditUrl()
		getRandomFromLists()"""
	string = '@{}: Have a wallpaper: {} posted by user {} on Reddit' . \
											format(name, final[0], final[1])
	if len(string)>140:
		string = '@{}: Wallpaper: {} posted by user {} on Reddit' . \
											format(name, final[0], final[1])
		if len(string)>140:
			string = '@{}: {} posted by user {} on Reddit' . \
											format(name, final[0], final[1])
			if len(string)>140:
				string = '@{}: {} posted by {}' . \
										format(name, final[0], final[1])
				if len(string)>140:
					url, author = getRandomFromLists(number, \
													urls, authors)
					final = confirmRedditUrl(url, urls, author, \
											authors, number, final[2])
					return lengthfunc(final, urls, \
										authors, number, name)
	if name=='0':
		string = string[4:]
	return string	

def loginTwitter():
	"""This will log in to the Twitter API and then return the resulting object.
	It uses TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_KEY, and TWITTER_ACCESS_SECRET in order
	to log in."""
	auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
	auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
	api = tweepy.API(auth)
	return api

def assignRedditInfo(data):
	"""This code will return reddit wallpaper urls, authors, and the number of items in both lists.
	Parameters ->
		data (the Reddit Json)
	If there are no such links on reddit, it will exit the program and output an error."""
	if len(data['data']['children']) >= 1:
		urls = []
		authors = []
		number = 0
		for item in data['data']['children']:
			if filterfunc(item['data']['url']):
				urls.append(item['data']['url'])
				authors.append(item['data']['author'])
				number = number+1
		return urls, authors, number
	else:
		print("ERROR: Nothing on Reddit.")
		sys.exit()
	
def getRandomFromLists(number, list1, list2):
	"""This function, provided two lists of equal length, will pick a random index value
	and return the items that match that index value from both lists.
	Parameters ->
		number (length of lists)
		list1 (list 1)
		list2 (list 2)
	Returned ->
		item1 (item from list 1)
		item2 (item from list 2)
	If the lists are not long enough, it will exit the 
	program and output an error."""
	if number >= 1:
		randomNum = random.randrange(0, number)
		item1 = list1[randomNum]
		item2 = list2[randomNum]
		return item1, item2
	else:
		print("ERROR: No image URLs from Reddit.")
		sys.exit()

def replyToTweetsFromQueryWithRedditInfo( final, \
										api, \
										tosearch, \
										phrases, \
										timeframe, \
										urls, \
										authors):
	"""This will search the Twitter API for certain phrases, 
	and then reply to tweets that match those phrases with Reddit 
	data. 
	It will also output the responses.
	Parameters ->
		(the final reddit data) [list]
		(the twitter api object)
		(the string to search) [str]
		(the phrases to watch for) [list]
		(tweet found will not be older than this many seconds) [int]
		(the reddit urls list) [list]
		(the reddit authors list) [list]
	Other functions used ->
		lengthfunc()"""
	search = api.search(q=tosearch)
	for item in search:
		if (phrases[0] in item.text and phrases[1] in item.text):
			if (time.time() - (item.created_at - \
			datetime.datetime(1970,1,1)).total_seconds())<timeframe:
				name = item.user.screen_name
				reply = lengthfunc(final, urls, authors, number, name)
				print(reply)
				api.update_status(reply, item.id)

def tweetRedditData(api, final, urls, authors, number):
	"""This will tweet the reddit data. It will also output the tweet.
	Parameters ->
		(the twitter api object)
		(the final reddit data) [list]
		(the reddit urls) [list]
		(the reddit authors) [list]
		(the length of the lists) [int]
	Other functions used ->
		lengthfunc()"""
	tweet = lengthfunc(final, urls, authors, number, '0')
	print(tweet)
	api.update_status(tweet)

def doItOnce():
	data = getInReddit()
	urls, authors, number = assignRedditInfo(data)
	url, author = getRandomFromLists(number, urls, authors)
	final = confirmRedditUrl(url, urls, author, authors, number, 1)
	api = loginTwitter()
	tweetRedditData(api, final, urls, authors, number)
	replyToTweetsFromQueryWithRedditInfo(final, \
										api, \
										PHRASE_TO_SEARCH_ON_TWITTER, \
										PHRASES_TO_MATCH_ON_TWITTER, \
										AGE_OF_TWEETS_TO_SEARCH, \
										urls, \
										authors)

def main():
	inst = 0;
	print("Reddit Wallpaper Bot")
	print()
	print()
	print()
	while True:
		inst = inst+1
		print("INSTANCE: ", end="")
		print(inst)
		try:
			doItOnce()
		except:
			print("UNSUCCESSFUL")
		print()
		print()
		print()
		print("WAITING 1 HOUR. PROGRESS:")
		print("------------------------------|")
		for item in range(30):
			print("=", end="")
			time.sleep(120)
		print("|")
		print()
		print()
	
main()
