from bs4 import BeautifulSoup
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import lxml
from lxml import html
import re
from urllib.parse import urldefrag




# returns a list of links (later)
def collect_links(url, markup):

    try:
        string_doc = html.fromstring(markup)
        string_doc.make_links_absolute(url)
        links = list(string_doc.iterlinks())
        my_links = [urldefrag(l[2])[0] for l in links]
        return my_links
    except: # if we run into an Empty Document, return an empty list
        return list()


# get text
def get_text(markup):
	soup = BeautifulSoup(markup, 'lxml')
	for script in soup(["script", "style"]):
		script.decompose()
	text = soup.get_text()
	return text

# returns the number of tags in a html markup
def get_num_tags(markup):
    soup = BeautifulSoup(markup, 'lxml')
    tag_list = soup.find_all(True)
    if tag_list:
        return len(tag_list)


def tokenize(text):
    tokens = list()
    conjunc = ["s", "d", "ll", "t", "re", "ve", "l", "e", "f", "c", "b", "k", "p", "y", "g", "j", "m", "n",
               "o", "q", "r", "u", "v", "w", "x", "z", "h", "h"]
    words = re.split('[-~!@#$%^&*()_+= `[\'\".,<>/?{}:;]', text)
    for w in words:
        if word_is_alnum(w) and w != '':
            # get rid of excess conjunctions
            w = w.lower()
            if w not in conjunc and not w.isdigit():
           	    tokens.append(w)
    return tokens


def tokenize_url(url):
    # split by parentehsis
    pieces = re.split('/', url)
    while ('' in pieces):
        pieces.remove('')
    return pieces

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
    freq1 = updateWordFrequencies(one_tokens)
    freq2 = updateWordFrequencies(two_tokens)

    num_common = 0

    for k,v in freq1.items():
        if k in freq2.keys():
            # if it does, get min of frequencies
            num_common += 1
            # optionally print word
            print(k)

    return num_common
   

