import re
from urllib.parse import urlparse
import extractor

# (url: str, rep: utils.response.Response): -> list
# returns a list of urls that are scraped from the response
# empty list for responses that are empty
def scraper(url, resp):
    # check if no content? 
    links = extract_next_links(url, resp)
    print(links)
    return [link for link in links if is_valid(link)]

# find links from the response here!
def extract_next_links(url, resp):
    # CHECK FOR BAD RESPONSES HERE!

    if resp.raw_response:
        return extractor.collect_links(resp.raw_response.content)
    else:
        print("NOTHING HERE AT URL: " + url)
        return list()

# used to filter urls
# add additional rules to this to filter urls
def is_valid(url):
    try:
        print("we are checking: " + url)
        parsed = urlparse(url)
      #  print("this is the domain: " + parsed.netloc)

        #if parsed.scheme not in set(["http", "https"]):
           # print ("scheme wrong")
           # return False

        if not re.match(r"^.*([(.ics)|(.cs)|(.informatics)].uci.edu)", parsed.netloc):
            return False

        if re.match(r"^.*(today.uci.edu)", parsed.netloc):
           # print("PATH: " + parsed.path)
            return re.match(r"^(\/department\/information_computer_sciences\/).*", parsed.path)

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