# test tokenizing and statistics! 
from utils.download import download
import statistics
import extractor as ex
from urllib.parse import urlparse
import re
import tldextract


test_url = "http://checkmate.ics.uci.edu"

parsed = urlparse(test_url)
print(parsed)

match = re.match(r"(?:http:\/\/)?((?:([^.]+)\.))?ics.uci\.edu", parsed.netloc)

print(match.group(2))


# Attaching relative links

# add to is_valid function? 


	


