# test tokenizing and statistics! 
from utils.download import download
import statistics
import extractor as ex
from urllib.parse import urlparse
import re
import tldextract
from urllib import robotparser

# Attaching relative links

# add to is_valid function?

print(re.match(r".*?([^\/\&?]{4,})(?:[\/\&\?])(.*?\1){3,}.*","https://www.ics.uci.edu/alumni/stayconnected/stayconnected/connected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/index.php"))
print(re.match(r".*?([^\/\&?]{4,})(?:[\/\&\?])(.*?\1){3,}.*","https://www.ics.uci.edu/community/alumni/index.php/stayconnected/hall_of_fame/hall_of_fame/hall_of_fame"))

