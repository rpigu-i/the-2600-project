### Code begins here

import requests
import re
import os
from bs4 import BeautifulSoup

class BleepTrack:
 def __init__(self, album, title, index):
   self.album = album
   self.title = title
   i = str(index)
   self.padded_index = "0" * (3-len(i)) + i # turn "5" into "005"

 @property
 def url(self):
   return self.album.url_prefix + self.padded_index + '.mp3'

 def download(self, dest_dir="."):
   r = requests.get(self.url, stream=True)
   dest_file = os.path.join(dest_dir, self.padded_index + " - " +
self.title) + ".mp3"
   with open(dest_file, 'wb') as f:
     for chunk in r.iter_content(chunk_size=1024):
       if chunk: # filter out keep-alive new chunks
         f.write(chunk)
         f.flush()

class BleepAlbum:

 def __init__(self, release_id):
   self.release_id = release_id
   album_url = "https://bleep.com/release/{}".format(self.release_id)
   r = requests.get(album_url)
   self.soup = BeautifulSoup(r.text)

 @property
 def artist(self):
   details = self.soup.find("div", "product-details")
   artist = details.find(itemprop="name")
   return artist.text

 @property
 def title(self):
   details = self.soup.find("div", "product-details")
   album_wrapper = details.find("dt", "release-title")
   title_elt = album_wrapper.find("a")
   return title_elt.text

 @property
 def tracks(self):
   tracks = []
   index = 1
   for span in self.soup.find_all("span", "track-name"):
     title = span.find("a").attrs['title']
     title = re.sub("^Play '(.*)'", r"\1", title)
     track = BleepTrack(self, title, index)
     tracks.append(track)
     index += 1
   return tracks

 @property
 def url_prefix(self):
   try:
     return self._url_prefix
   except:
     pass
   get_preview_url = '
https://bleep.com/player/resolve/{}-1-1'.format(self.release_id)
   r = requests.get(get_preview_url)
   preview_url = r.text
   match = re.search("(^http://.*?-01-)\d+.mp3", preview_url)
   self._url_prefix = match.group(1)
   return self._url_prefix

if __name__ == "__main__":
 album = BleepAlbum(55082)

 # This creates a directory like "Artist name/Album title", and saves the
tracks there.

 save_path = os.path.join(album.artist, album.title)
 try:
   os.makedirs(save_path)
 except FileExistsError:
   pass
 for track in album.tracks:
   print(track.title)
   track.download(save_path)

