from threading import Thread

from urllib import robotparser
from urllib.parse import urlparse
import requests
import extractor as ex
import re
from reppy.robots import Robots

# DICTIONARY TO STORE THE ROBOTS.TXT FROM SUBDOMAINS
robot_files = dict()
filepath = "robotlist.txt"
# robot parser object
rparser = robotparser.RobotFileParser()

# list to store urls we've filtered
# string url: set of tokens
history = dict()


# Checks if it is a good url
def is_good_url(url):


    # check if we can crawl
    if not (allows_crawl(url)):
        #print("not allowed to crawl!")
        return False


    # check length of url, if there are more than 12 subdirectories or slashes, then ditch it
    if len(url) > 150:
        #print("url too long")
        return False

    # Source: https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression

    # check for repeating directories
    if re.match(r".*?([^\/\&?]{4,})(?:[\/\&\?])(.*?\1){3,}.*", url):
        return False

    # also checks for repeating paths
    #parsed_url = history[url] # tokenizes using / to get path names
    parsed_url = ex.tokenize_url(url)
    s = set(parsed_url)

    if len(parsed_url) != len(s):
        #print("repeating directory")
        return False


    # # could use the above to check for similar urls to the ones in history
    # for old_url, tokens in history.items():
    #     # check if tokens same as parsed one
    #     if old_url != url and set(tokens) == s: # compare tokens to other urls
    #         return False

    # check for extra directories
    if re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$", url):
        #print("there are extra directories")
        return False

    # avoid calendars
    if re.match("^.*calendar.*$", url):
        #print("avoiding bc this is a calendar")
        return False

    # avoid json files
    if re.match("^.*-json", url):
        #print("avoiding bc it's a json")
        return False

    if re.match(
        r".*\.(css|js|bmp|gif|jpe?g|ico"
        + r"|png|tiff?|mid|mp2|mp3|mp4"
        + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
        + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
        + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
        + r"|epub|dll|cnf|tgz|sha1"
        + r"|thmx|mso|arff|rtf|jar|csv"
        + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", url):
        return False

    # manual avoids
    if re.match(r"https:\/\/archive\.ics\.uci\.edu\/ml", url):
        return False

    return True


def get_delay(url):
    parsed = urlparse(url)
    base_url = parsed.scheme + "://" + parsed.netloc

    if base_url in robot_files.keys():  # if we already downloaded the robots.txt file
        rparser = robot_files[base_url]
        delay = rparser.agent("*").delay
        #print("found delay: ", delay)
        return delay
    else:
        print("not there I guess")



# checks for content length and quality
def is_quality_content(url):
    try:
        h = requests.head(url)

        # CHECKING CONTENT LENGTH
        if ('Content-length' in h.headers.keys()):
            content_length = int(h.headers['Content-length'])
            #print("Content Length: ", content_length)
            if (content_length == 0):
                return False
    except:
        print("something broke")


    # CHECK CONTENT QUALITY
    # calculate proportion of tags versus
    # compare length of markup to length of text content
    # get proportion

    # use head request to get text? or lxml

    # CHECK FOR SIMILAR PAGES WITH NO INFORMATION
    # compare token list and frequencies of pages? # use checksum?? or simhash??

    return True

def allows_crawl(url):
    try:
        #url = "https://www.ics.uci.edu"
       # print("This is the passed url: ", url)
        url = str(url)
        parsed = urlparse(url)
        base_url = parsed.scheme + "://" + parsed.netloc


        # set up parser with robots.txt file!
        if base_url in robot_files.keys():  # if we already downloaded the robots.txt file
            #print("grabbing already foumd robots.txt")
            rparser = robot_files[base_url]
        else:
            try:

                robot_url = base_url + "/robots.txt"
                rparser = Robots.fetch(robot_url)


                # PUT ROBOTS.TXT FILE INTO HERE!
                robot_files[base_url] = rparser

            except IOError:
                print("IOERROR")
                return False
            except:
                print("some other error?")
                return False
        try:
            return rparser.allowed("*", url)
        except KeyError:
            return False
    except IOError:
        return False







