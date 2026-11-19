#Listing2.py
#Only GPS info

#pip install exifread

import exifread

f = open("C:\Users\Username\Desktop\Sample1.jpg") #Location of photograph 

tags = exifread.process_file(f)

for tag in tags.keys():
	#Look for GPS tags and print them
  	if "GPS" in tag:
  		print "Key: %s, value %s" % (tag, tags[tag])

