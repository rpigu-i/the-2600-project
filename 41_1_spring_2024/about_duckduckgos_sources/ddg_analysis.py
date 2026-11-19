#				*** ddg_analysis.py ***
#
#	This is a script that uses the ddg library to show the user detailed
#		information about their DuckDuckGo results.
#
import ddg

while True:
	# Fetch the search results for a user specified search term
	results = ddg.fetchAll(input("\n[???] Search term: "))

	print("")
	i = 1

	# Print out a list of data
	for result in results:
		title = result["t"][0:24]
		if len(title) < 24:
			title += (" " * (27 - len(title)))
		else:
			title += "..."
		try:
			source = result["s"]
		except:
			source = "Not Available"
		try:
			timestamp = result["e"]
		except:
			timestamp = "****** Not Available ******"
		print(" " + str(i) + ":" + (" " * (5 - len(str(i))))
			+ "'s': " + source + " "
			+ "Title: " + title + " "
			# Uncomment the following line to also print out the timestamp
			#+ "Timestamp: " + timestamp + " "
			+ "URL: " + result["u"])
		i += 1

