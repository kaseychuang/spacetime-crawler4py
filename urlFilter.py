from threading import Thread

from urllib import robotparser
from urllib.parse import urlparse
import requests
import extractor as ex
import re

# DICTIONARY TO STORE THE ROBOTS.TXT FROM SUBDOMAINS
robots = dict()
# robot parser object
rparser = robotparser.RobotFileParser()

# list to store urls we've filtered
history = list()


# Checks if it is a good url
def is_good_url(url):

    # add url into the history list (hopefully is-good_url will always be called)
    history.append(url)

    # Source: https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression
    # check for repeating directories

    # WHY IS RE NOT MATCHING??

    if re.match(r".*?([^\/\&?]{4,})(?:[\/\&\?])(.*?\1){3,}.*", url):
        print("this is a repeating directory")
        return False

    # manually avoid this one
    if re.match(r"https://www.ics.uci.edu/.*/stayconnected/stayconnected", url):
        return False

    # check length of url, if there are more than 12 subdirectories or slashes, then ditch it
    if len(url) > 100:
        print("url too long")
        return False

    # check for extra directories
    if re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$", url):
        print("there are extra directories")
        return False

    # avoid calendars
    if re.match("^.*calendar.*$", url):
        print("avoiding bc this is a calendar")
        return False

    return True


# checks for content length and quality
def is_quality_content(url):
    # MAKE HEAD REQUEST AND CHECK IF WE WANT TO ACTUALLY DOWNLOAD THIS PAGE!
    h = requests.head(url)

    # CHECKING CONTENT LENGTH
    if ('Content-length' in h.headers.keys()):
        content_length = int(h.headers['Content-length'])
        #print("Content Length: ", content_length)
        if (content_length == 0):
            return False

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
        parsed = urlparse(url)
        base_url = parsed.scheme + "://" + parsed.netloc

        if base_url in robots.keys():  # if we already downloaded the robots.txt file
           rparser.parse(robots[base_url])
        else:
            # file = download(base_url + "/robots.txt", self.config)
            file = requests.get(base_url + "/robots.txt", timeout=5)
            status_code = file.status_code
            if status_code >= 200 and status_code < 300:
                # get robots.txt file content
                # file_content = file.raw_response.content.decode()
                file_content = file.text
                #print(file_content)

                file_lines = file_content.split('\n')
                robots[base_url] = file_lines
                #print(file_lines)

                # check robots.txt
                rparser.parse(file_lines)
            else:
                print("not a good link to fetch robots file")
                # exit out without considering robots.txt file?
                # CHECK THIS OUT LATER
                return True

        can_fetch = rparser.can_fetch("IR WR 26286982", url)

        # IMPLEMENT DELAY RETURN VALUE???!!
        delay = rparser.crawl_delay("IR WR 26286982")

        if not can_fetch:
            print("not allowed to crawl")
            return False

        return True

    # handle bad urls
    except requests.ConnectionError:
        #print("There was a connection error")
        return False
    except requests.Timeout:
        #print("There was timeout")
        return False
    except requests.RequestException:
        return False