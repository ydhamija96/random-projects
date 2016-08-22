from imgurpython import ImgurClient
import random
import subprocess

client_id = "e2d66c0fbd32315"
client_secret = "0ff533a2e1d7957666ff8ff5dd21a849b3dde3dc"

client = ImgurClient(client_id, client_secret)

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

theChosen = random.choice(client.get_album_images(albums[choice]))

cmd = 'echo '+theChosen.link.strip()+'|clip'
subprocess.check_call(cmd, shell=True)

print(theChosen.link + " has been copied to your clipboard :)")
