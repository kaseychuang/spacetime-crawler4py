from bs4 import BeautifulSoup
import lxml
from lxml import html
import re


# BeautifulSoup(markup, "lxml")

# returns a list of links (later)
def collect_links(url, markup):

	string_doc = html.fromstring(markup)	
	string_doc.make_links_absolute(url)
	links = list(string_doc.iterlinks())
	links = [l[2] for l in links]

	#for i in links:
	#	print(i)


	return links

# get text
def get_text(markup):
	soup = BeautifulSoup(markup, 'lxml')

	# https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
	# get rid of javascript and css
	for script in soup(["script", "style"]):
		script.decompose()

	text = soup.get_text()
	#print(tokenize(text))
	return text


def tokenize(text):
    # read text file
    tokens = list()
    words = re.split('[-~!@#$%^&*()_+= `[\'\".,<>/?{}:;]', text)
    for w in words:
        if word_is_alnum(w) and w != '':
        	# get rid of excess conjunctions
        	w = w.lower()
        	conjunc = ["s", "d", "ll", "t", "re", "ve", "l", "e", "f", "c"
        				"b"]
        	if w not in conjunc and not w.isdigit():
           		tokens.append(w)

    return tokens

# Helper method to check if all the characters in a word are alphanumeric
def word_is_alnum(word):
    for ch in word:
        if not ch.isalnum():
            return False
    return True


# updates given dictionary with word frequencies
def updateWordFrequencies(dictionary, tokenList):
    if tokenList is not None:
        for token in tokenList:
            if token in dictionary:
                dictionary[token] += 1
            else:
                dictionary[token] = 1

# returns an ordered list of the words that appear the most frequently
def get_ordered_freqs(frequencies):
    if frequencies is not None:
        # list comprehension, ordering by value
        ordered = [(k, v) for (k,v) in sorted(frequencies.items(), key = lambda x: (-x[1], x[0]))]
        return ordered

# USE THIS TO COMPARE IF WEBSITES ARE LARGELY THE SAME AND FILTER?? 
def get_intersection(markup1, markup2):
    # get tokens of both files
    one_tokens = tokenize(markup1)
    two_tokens = tokenize(markup2)
    freq1 = computeWordFrequencies(one_tokens)
    freq2 = computeWordFrequencies(two_tokens)

    num_common = 0

    for k,v in freq1.items():
        if k in freq2.keys():
            # if it does, get min of frequencies
            num_common += 1
            # optionally print word
            print(k)

    return num_common
   

