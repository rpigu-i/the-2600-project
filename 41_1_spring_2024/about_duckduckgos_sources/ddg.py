#
#				*** ddg.py ***
#
#	This is a Python library for fetching search results from DuckDuckGo.
#	It gets search results directly from links.duckduckgo.com.
#
from urllib.request import urlopen, Request
import re, json

headers = {'User-Agent': 'ddg.py'}

def loadPage(url):
	#
	# WARNING: The following line of code is necessary to make this program
	# a user agent rather than a robot. The user decides when and if
	# they want to load more pages. You are strongly encouraged not
	# to remove or "comment out" the following line.
	#
	input("\n[???] ENTER to fetch web page, CTRL+C to cancel ")
	page = urlopen(Request(url, headers=headers)).read().decode("utf-8")
	return page

def getVQD(page):
	return (re.search(',vqd="[0-9]-[0-9]*"', page)[0].replace(',vqd="', "")
		.replace('"', ""))
def fetchAll(search):
	resultsList = []

	searchTerm = search.replace(" ", "+")
	print("[DDG] Search term is: " + searchTerm)

	# Get the VQD of this search from the first human readable page
	print("[DDG] Fetching first human readable page...")
	currentUrl = "https://duckduckgo.com/?q=" + searchTerm + "&ia=web"
	currentPage = loadPage(currentUrl)
	print("[DDG] Extracting VQD number...")
	VQD = getVQD(currentPage)
	print("[DDG] VQD number is: " + VQD)

	# Use the VQD to access the links subdomain
	print("[DDG] Getting JSON format SERP from links.duckduckgo.com...")
	currentUrl = ("https://links.duckduckgo.com/d.js?q=" + searchTerm
			+ "&s=0&vqd=" + VQD)

	resultsFromLastPage = ['']

	while True:
		currentPage = loadPage(currentUrl)

		# Extract the results in JSON format
		try:
			JSONresultsString = (re.search(r"load\(\'d\'\,.*}]\);", currentPage)
				[0].replace("load('d',", "")[0:-2])
		except:
			break
			# Add the current page of JSON results to the results list
			resultsFromCurrentPage = json.loads(JSONresultsString.replace("\t", ""))
			if resultsFromCurrentPage[0:-1] == resultsFromLastPage[0:-1]:
				print("[DDG] Current page identical to last, assuming end reached")
				break
			resultsFromLastPage = resultsFromCurrentPage
			resultsList += resultsFromCurrentPage[0:-1]
			print("[DDG] Got " + str(len(resultsFromCurrentPage[0:-1]))
+ " results from current page")

			# Move to next page
			print("[DDG] Moving to next page...")
			try:
				currentUrl = ("https://links.duckduckgo.com/"
					+ resultsFromCurrentPage[-1]['n'])
			except:
				print("[DDG] End of results")
				break

		return resultsList
	if __name__ == "__main__":
		# If running as main program, get search term from user and tell user how
		# to use the results object
		results = fetchAll(input("\n[???] Search term: "))
		print("""
	[***] To look at the results, browse the list called 'results' using the below
	[***] console. For example, try typing:
	results[0]['a']
[***] This will show you the description of the first result.""")

