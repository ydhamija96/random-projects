from imgurpython import ImgurClient
import random
import subprocess
import sys
from difflib import SequenceMatcher

client_id = "e2d66c0fbd32315"
client_secret = "0ff533a2e1d7957666ff8ff5dd21a849b3dde3dc"

client = ImgurClient(client_id, client_secret)

if(len(sys.argv) <= 1):
    albums = []
    count = 0
    for album in client.get_account_albums("reactiongifsarchive"):
        album_title = album.title if album.title else 'Untitled'
        print('{1}: {0}'.format(album_title, count))
        albums.append(album.id)
        count = count+1
    print()
    choice = int(input("Please pick your choice: "))
    print()
    chosAlb = albums[choice]
else:
    chosAlb = -1
    for album in client.get_account_albums("reactiongifsarchive"):
        if(sys.argv[1].lower() in album.title.lower()):
            chosAlb = album.id
    if chosAlb == -1:
        print("404 Category Not Found")
        exit()

theChosen = random.choice(client.get_album_images(chosAlb))

cmd = 'echo '+theChosen.link.strip()+'|clip'
subprocess.check_call(cmd, shell=True)

print(theChosen.link + " has been copied to your clipboard :)")