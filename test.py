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

tbd_url = "https://www.stat.uci.edu/feed/"
robot_parser = robotparser.RobotFileParser(tbd_url)
print(robot_parser.crawl_delay("IR WR 26286982"))
print(robot_parser.can_fetch("IR WR 26286982", tbd_url))


