#Listing1.py
#Pull all Exif Tags 

#pip install exifread

import exifread

f = open("C:\Users\Username\Desktop\Sample1.jpg") #Location of photograph 

tags = exifread.process_file(f)

for tag in tags.keys():
  if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
  	print "Key: %s, value %s" % (tag, tags[tag])

