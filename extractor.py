from bs4 import BeautifulSoup
import lxml
import re


# BeautifulSoup(markup, "lxml")

# returns a list of links (later)
def collect_links(markup):
	# get html content
	soup = BeautifulSoup(markup, 'lxml')
	links = list()

	for link in soup.find_all('a'):
		url = link.get('href')
		if type(url) == str:
			if not re.match(r"^#.*", url):
				links.append(url)
 

	return links	
