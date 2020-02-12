from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
from urllib import robotparser
from urllib.parse import urlparse
from urllib import parse
import time
import statistics
import requests
import extractor as ex
import re

# DICTIONARY TO STORE THE ROBOTS.TXT FROM SUBDOMAINS
robots = dict()
rparser = robotparser.RobotFileParser()

def check_robots_txt(url):
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
                print(file_content)

                file_lines = file_content.split('\n')
                robots[base_url] = file_lines
                print(file_lines)

                # check robots.txt
                rparser.parse(file_lines)
            else:
                print("not a good link to fetch robots file")
                return False

        can_fetch = rparser.can_fetch("IR WR 26286982", url)
        delay = rparser.crawl_delay("IR WR 26286982")

        if not can_fetch:
            print("not allowed to crawl")
            return False

        return True

    # handle bad urls
    except requests.ConnectionError:
        print("There was a connection error")
        return False
    except requests.Timeout:
        print("There was timeout")
        return False
    except requests.RequestException:
        return False