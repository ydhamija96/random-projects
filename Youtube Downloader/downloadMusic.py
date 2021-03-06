# This program scans youtube channels for their latest videos and downloads
# either the most recent 10, or the most recent since the last one it downloaded

YOUTUBE_CHANNELS = [
    "UCORIeT1hk6tYBuntEXsguLg",     # PostmodernJukebox
    "UCM9KEEuzacwVlkt9JfJad7g"      # Chill Nation
]
DOWNLOAD_PATH = "Downloads"
API_KEY = ""
RECORDS_PATH = "alreadyDone.txt"

import urllib, json, urllib2, os

def getVideo(channel, last = 1):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+channel+"&maxResults="+str(last)+"&order=date&key="+API_KEY
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    vidId = data['items'][last-1]['id']['videoId']
    return vidId

def inFile(string, path):
    handle = open(path, 'r')
    for line in handle:
        if(line.strip() == string):
            handle.close()
            return True
    handle.close()
    return False

def downloadVideo(vid, path, name):
    url = "http://youtubeinmp3.com/fetch/?video=http://www.youtube.com/watch?v="+vid
    outfile = urllib2.urlopen(url)
    output = open(path+name+".mp3", 'wb')
    output.write(outfile.read())
    output.close

def putInFile(string, path):
    handle = open(path, 'a')
    handle.write("\n"+string)
    handle.close()

def main():
    for channel in YOUTUBE_CHANNELS:
        print "Channel: "+channel
        latest = getVideo(channel)
        count = 1
        while((not inFile(latest, RECORDS_PATH)) and (count<=10)):
            print "Getting Video: "+latest
            try:
                attempt = 1
                size = 0
                while(attempt <= 10 and size < 50000):
                    downloadVideo(latest, DOWNLOAD_PATH, latest)
                    size = os.path.getsize(DOWNLOAD_PATH+latest+".mp3")
                if(size < 50000):
                    os.remove(DOWNLOAD_PATH+latest+".mp3")
                    raise ImportError("File download failed after 10 attempts.")
            except:
                print "ERROR: Could not download video."
            else:
                putInFile(latest, RECORDS_PATH)
            count += 1
            latest = getVideo(channel, count)

main()
