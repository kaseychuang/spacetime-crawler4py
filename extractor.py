from bs4 import BeautifulSoup
import lxml

# BeautifulSoup(markup, "lxml")

# returns a list of links (later)
def collect_links(markup):
	# get html content
	soup = BeautifulSoup(markup, 'lxml')
	links = list()

	for link in soup.find_all('a'):
		if link.get('href') != "#": # get rid of fragments?
			links.append(link.get('href'))

	return links	
