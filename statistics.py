# build class store data
import extractor as ex
from urllib.parse import urlparse
import re


class Statistics():

	stopwords = ["a", "about", "above", "after", "again", "against", "all",
							"am", "an", "and", "any", "are", "aren't", "as", "at",
							"be", "because", "been", "before", "being", "below", "between",
							"both", "but", "by", "can't", "cannot", "could", "couldn't", 
							"did", "didn't", "do", "does", "doesn't", "doing", "don't", 
							"down", "during", "each", "few", "for", "from", "further",
							"had", "hadn't", "has", "hasn't", "have", "haven't", "having",
							"he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", 
							"herself", "him", "himself", "his", "how", "i", "I'd", "if", "in",
							"i'll", "i've", "i'm", "into", "is", "isn't", "it", "it's", "its",
							"itself", "let's", "me", "more", "most", "mustn't", "my", "myself", 
							"no", "nor", "not", "of", "off", "on", "once", "only", "or", 
							"other", "ought", "our", "ours", "ourselves", "out", "over", "own",
							"same", "shan't", "she", "she'd", "she'll", "she's", "should", 
							"shouldn't", "so", "some", "such", "than", "that", "that's", "the", 
							"theirs", "their", "them", "themselves", "then", "there", 
							"there's", "these", "they", "they'd", "they'll", "they're", 
							"they've", "this", "those", "through", "to", "too", "under",
							"until", "up", "very", "was", "wasn't", "we", "we'd", "we'll",
							"we're", "we've", "were", "weren't", "what", "what's", 
							"when", "when's", "where", "where's", "which", "while", 
							"who", "who's", "whom", "why", "why's", "with", "won't", 
							"would", "wouldn't", "you", "you'd", "you'll", "you're", "your",
							"yours", "yourself", "yourselves"]

	def __init__(self, filepath): # additional paramters??
		# dictionary to store frequency of words
		self._freqs = dict()

		# tuple that stores the longest page (in terms of words)
			# (url, number of words)
		self._longest = ("", 0)

		# Subdomains! 
		# dictionary: (subdomain -> str, set<strs (paths))
		self._subdomains = {}

		# open file and store that object in variable to use in methods
		self._filepath = filepath

		self._num_urls_downloaded = 0

		self._unique_pages = set()




	#METHODS (DON'T FORGET TO INCLUDE SELF)
	# yeah don't just feed the individual text
	def update_stats(self, url, response):
		self._num_urls_downloaded += 1
		# get text
		text = ex.get_text(response.raw_response.content)
		tokens = ex.tokenize(text)

		# CHECK IF CONTENT WORTH CRAWLING?

		# high textual content? Maybe compare num of html tags versus text

		


		# update statistics
		self.update_longest(url, tokens)
		self.update_frequencies(tokens)
		self.update_subdomains(url)
		self.add_page(url)
		self.update_file()

	def add_page(self, url):
		# remove fragment
		new_url = url.split('#')[0]		

		# add to set
		self._unique_pages.add(new_url)

	# check if this new page is the longest in terms of words
	def update_longest(self, url, tokens):
		num_words = len(tokens)
		if (num_words > self._longest[1]):
			self._longest = (url, num_words)


	# add page's text to the frequency dictionary
	def update_frequencies(self, tokens):
		ex.updateWordFrequencies(self._freqs, tokens)

	# take note of page's subdomain and how many unique pages it has? 
		# use a set to keep track of unique pages?
		# dictionary with a set as a value? 
		# can use this same dictionary to get the number of unique pages as well 
			# should be the total of all lengths of the sets in the dictionary

	def update_subdomains(self, url):
		# CHECK IF N THE .ICS.UCI.EDU DOMAIN! 
		parsed = urlparse(url)

		# if in ics subdomain: 
		match = re.match(r"(?:http:\/\/)?((?:([^.]+)\.))?ics.uci\.edu", parsed.netloc)

		if match:
	 		# store the page, a set will keep it unique
	 		subdomain = match.group(2)
	 		if subdomain != "www":
	 			if not subdomain in self._subdomains.keys():
	 				self._subdomains[subdomain] = set()
	 			self._subdomains[subdomain].add(url)




	# write to file
	def update_file(self):
		file = open(self._filepath, 'w')


		# print number of unique pages (not including fragments)
			# use number of 


		# print longest page in terms of WORDS
		file.write("Longest page: " + self._longest[0] + "\n with " + str(self._longest[1]) + " words\n")


		# print the list of 50 most common words ordered by frequency
		# 	IGNORE ENGLISH STOP WORDS (reference the link on the assignment instructions)
		freq_list = ex.get_ordered_freqs(self._freqs)
		count = 1
		index = 0
		while (count <= 75 and index < len(freq_list)):
			# get next most frequent word tuple
			word, num = freq_list[index]
			# check for english stop words
			if (word not in Statistics.stopwords):
				file.write(str(count)+ ". " + freq_list[index][0] + " - " + str(freq_list[index][1]) + "\n")
				count += 1
			index +=1

		# print list of subdomains ordered alphabetically and the num
		# 	of unique pages detected in each subdomain
		# 	URL, number (http://vision.ics.uci.edu, 10)

		file.write("LIST OF SUBDOMAINS IN ICS.UCI.EDU\n")
		ordered_subdomains = [(s, pgs) for (s, pgs) in sorted(self._subdomains.items(), key = lambda x: x[0])]

		for sub, pages in ordered_subdomains:
			file.write(sub + ", " + str(len(pages)) +"\n")

		#print(self._subdomains)

		file.close()




