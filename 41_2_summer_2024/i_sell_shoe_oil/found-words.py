# Script for finding calculator compatible words.
# Requires the presence of SOWPODS.txt in the working directory.

with open("sowpods.txt", "r") as dictfile:
	dicti = dictfile.read()
dicti = dicti.split("\n")

calcletters = "lbhsgieo"
calcfriendlylist = []

for word in dicti:
	if len(word) > 2:
		good = True
		for letter in word.lower():
			if not letter in calcletters:
				good = False
				break
		if good:
			calcfriendlylist.append(word)

for word in calcfriendlylist:
	print(word)

print(len(calcfriendlylist))

