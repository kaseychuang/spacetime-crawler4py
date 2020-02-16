# test tokenizing and statistics! 
from utils.download import download
import statistics
import extractor as ex
from urllib.parse import urlparse
import re
import tldextract
# from urllib import robotparser
# import urllib.robotparser
# rp = urllib.robotparser.RobotFileParser()
# rp.set_url("https://www.stat.uci.edu/robots.txt")
# rp.read()
# rp.can_fetch("*", "https://www.stat.uci.edu")
#
from reppy.robots import Robots

from urllib import robotparser
from urllib.parse import urlparse
import requests
import extractor as ex
import re

robots = dict()
filepath = "robotlist.txt"
# robot parser object
rparser = robotparser.RobotFileParser()

# list to store urls we've filtered
# string url: set of tokens
history = dict()
from reppy.robots import Robots



# # Get the rules for a specific agent
# agent = robots.agent('my-user-agent')
# print(agent.allowed('http://example.com/some/path/'))

url = "https://www.ics.uci.edu"
parsed = urlparse(url)
print("scheme: ", parsed.scheme)
print("netloc: ", parsed.netloc)
base_url = parsed.scheme + "://" + parsed.netloc
print("BASE URL: ", base_url)

# def allows_crawl(url):
#     try:
#         output_file = open(filepath, 'a+')
#
#         parsed = urlparse(url)
#         base_url = parsed.scheme + "://" + parsed.netloc
#
#         # set up parser with robots.txt file!
#         if base_url in robots.keys():  # if we already downloaded the robots.txt file
#             print("grabbing already foumd robots.txt")
#             rparser = robots[base_url]
#         else:
#             try:
#                 print("try")
#                 print(base_url + "/robots.txt")
#                 robot_url = base_url + "/robots.txt"
#                 rparser = Robots.fetch(robot_url)
#
#                 # PUT ROBOTS.TXT FILE INTO HERE!
#                 robots[base_url] = rparser
#
#                 #return rparser.allowed("*", url)
#             except IOError:
#                 print("IOERROR")
#                 return False
#
#
#         try:
#
#             output_file.write("URL: " + url + "\n")
#             output_file.close()
#             return rparser.allowed("*", url)
#         except KeyError:
#             return False
#     except IOError:
#         return False
#
# print(allows_crawl("https://www.ics.uci.edu/~lab/lab_schedule/spring_finals.php"))
# print(allows_crawl("https://www.ics.uci.edu/~lab/lab_schedule/"))
# print(allows_crawl("https://www.ics.uci.edu/ugrad/honors/index.php/computing/advising/sao/policies/degrees/resources/degrees/index.php"))
