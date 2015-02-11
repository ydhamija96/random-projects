#!/usr/bin/python


"""
This is a program that will delete everything in a folder,
get a reddit wallpaper,
download the image into the folder,
and set the it as the wallpaper on an Ubuntu system.

If not running an Ubuntu system, change the 
SET_AS_WALLPAPER global variable to False, 
and the program will not run the set wallpaper function.
It will merely delete the contents of the folder
and then download the image into the folder.
"""


SET_AS_WALLPAPER = True

# WARNING: Everything in this folder will be DELETED on running this program.
# Be VERY careful.
FOLDER_LOCATION = "XXXXXXXXXXXX"

TIME = "week"


import os
import sys
import random
import json
import urllib2
import urllib
import time
import datetime


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


def getRandomFromLists(number, list1, list2):
	"""
	This will return a random listing from a list, 
	and also return the corresponding listing from a 
	corresponding list of the same length.
	If the lists are not long enough, it will exit the 
	entire program and output an error.
	Parameters ->
		length of both lists [int]
		list 1 [list]
		list 2 [list]
	Returned ->
		random item from list 1 [unknown]
		correspoinding random item from list 2 [unknown]
	"""
	if number >= 1:
		randomNum = random.randrange(0, number)
		item1 = list1[randomNum]
		item2 = list2[randomNum]
		return item1, item2
	else:
		print("ERROR: Lists are empty.")
		sys.exit()

def filterfunc(data):
	"""
	Make sure data is an image URL.
	Parameters -> 
		image url [str]
	"""
	if data[-3:] == 'png' or data[-3:] == 'jpg' or \
	data[-4:] == 'jpeg' or data[-3:] == 'bmp' or \
	data[-3:] == 'gif':
		return True
	return False

def getInReddit():
	"""
	Returns ->
	    Reddit JSON [object]
	"""
	url = "http://www.reddit.com/r/wallpapers/top/.json?sort=top&t="+TIME
	data = json.load(urllib2.urlopen(url))
	return data

def assignRedditInfo(data):
	"""
	This function returns information extracted from
	a provided Reddit API object.
	If there's nothing on reddit, 
	it will exit the program and output an error.
	Parameters ->
		Reddit Json [object]
	Returns-> 
	    reddit wallpaper urls [list]
	    authors [list]
	    number of items in both lists [int]
	"""
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
		print "ERROR: Nothing on Reddit."
		sys.exit()

def confirmRedditUrl(url, urls, author, authors, number, iteration):
	"""
	Use redirect handler class to check if the Reddit URL 
	redirects. If it does, it chooses a different Reddit URL.
	This is a recursive function. 
	If it undergoes over 10 interations, then it will end the program
	and output an error.
	Parameters ->
		the url to check [str]
		all urls available [list]
		the reddit username of that url [str]
		all reddit usernames available [list]
		the number of all available urls and authors [int]
		iteration (this should always be set as 1) [int]
	Returns ->
	    the url [str]
	    the author [str]
	Dependencies ->
		getRandomFromLists()
	"""
	if iteration > 10:
		print 'Too many iterations.'
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
		return url, author

def downloadUrl(url, store):
    """
    This function will download the result of a URL
    to a specific filename and location.
    Parameters ->
        url to download [str]
        file path to save as [str]
    """
    urllib.urlretrieve(url, store)

def imgurNameGetter(url):
    """
    This function will, given an imgur URL,
    return the name of the image.
    Parameters ->
        the imgur url [str]
    Returns ->
        the name [str]
    """
    return url[(url.rfind('/')+1):]

def clearFolder(folder):
    """
    This function will delete all contents of the folder specified.
    Parameters ->
        folder path [str]
    """
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

def setWallpaper(fileName):
    """
    This function will set an image as the wallpaper on an Ubuntu system.
    Parameters ->
        image path [str]
    """
    os.system("gsettings set org.gnome.desktop.background picture-uri file://"+fileName)


def main():
    redditApi = getInReddit()
    allUrls, allAuthors, numberOfUrlsAndAuthors = assignRedditInfo(redditApi)
    url, author = getRandomFromLists(numberOfUrlsAndAuthors, allUrls, allAuthors)
    confirmedUrl, confirmedAuthor = confirmRedditUrl(url, allUrls, author, allAuthors, numberOfUrlsAndAuthors, 1)
    imageName = imgurNameGetter(confirmedUrl)
    clearFolder(FOLDER_LOCATION)
    fileName = FOLDER_LOCATION+imageName
    downloadUrl(confirmedUrl, fileName)
    if(SET_AS_WALLPAPER):
        setWallpaper(fileName)

    
main()
