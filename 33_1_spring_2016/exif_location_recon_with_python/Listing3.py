#Listing3.py
#Custom/Important Tags

#pip install exifread

import exifread

f = open("C:\Users\Username\Desktop\Sample1.jpg") #Location of photograph 

tags = exifread.process_file(f)

#Only find/print desired tags

for tag in tags.keys():
	if 'EXIF DateTimeOriginal' in tag:
		print("Original Date & Time: %s" % (tags[tag]))

	else:
		if 'GPS GPSLatitudeRef' in tag:
		print("Latitude Reference: %s" % (tags[tag]))

		else:
			if 'GPS GPSLatitude' in tag:
			print("GPS Latitude: %s" % (tags[tag]))

			else:
				if 'GPS GPSLongitudeRef' in tag:
				print("Longitude Reference: %s" % (tags[tag]))

				else:
					if 'GPS GPSLongitude' in tag:
					print("GPS Longitude: %s" %(tags[tag]))

					else:
					  if 'Image Model' in tag:
					  print("Model: %s" %(tags[tag]))

					     else:
					       if 'Image Make' in tag
							     print("Make: %s" %(tags[tag]))

