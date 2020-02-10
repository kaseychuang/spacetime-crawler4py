import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
import extractor
import statistics
import lxml

# (url: str, rep: utils.response.Response): -> list
# returns a list of urls that are scraped from the response
# empty list for responses that are empty
def scraper(url, resp):
    # check for status codes here??
    status_code = resp.status
    if status_code >= 200 and status_code < 300:
    # get and process links!
        links = extract_next_links(url, resp)
        
        return [link for link in links if is_valid(link)]
    else:
        return list()


# find links from the response here!
def extract_next_links(url, resp):
    if resp.raw_response:
        links = extractor.collect_links(url, resp.raw_response.content)

        # de fragment them 
        for l in links:
            l = urldefrag(l)[0]

        return links
    else:
        return list()

# used to filter urls
# add additional rules to this to filter urls
def is_valid(url):
    try:
        parsed = urlparse(url)

        #if parsed.scheme not in set(["http", "https"]):
           # print ("scheme wrong")
           # return False

        if not re.match(r"^.*(\b(\.ics|\.cs|\.informatics|\.stat)\b)\.uci\.edu", parsed.netloc):
            return False

        if re.match(r"^.*(today.uci.edu)", parsed.netloc):
           # print("PATH: " + parsed.path)
           if not re.match(r"^(\/department\/information_computer_sciences\/).*", parsed.path):
                return False

        # NEED BETTER FILTER FOR WRONG FILE TIMES
            # filter out calendar??

         #check if file extension is in the middle of a path
        if re.match(r".*\/(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|json|mp2|mp3|mp4|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1r|thmx|mso|arff|rtf|jar|csvr|rm|smil|wmv|swf|wma|zip|rar|gz)\/", parsed.path.lower()):
            #print(parsed.path)
            #print("path contains invalid file type")
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise