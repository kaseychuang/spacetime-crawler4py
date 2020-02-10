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


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.stats = statistics.Statistics("stats.txt")
        self.robots = dict()
        self.rparser = robotparser.RobotFileParser()
        super().__init__(daemon=True)

    def check_robots_txt(self, url):
        try:
            parsed = urlparse(url)
            base_url = parsed.scheme + "://" + parsed.netloc
            # print("base url", base_url)
            if base_url in self.robots.keys():
                # grab that one
                self.rparser.parse(self.robots[base_url])
            else:
                #file = download(base_url + "/robots.txt", self.config)
                file = requests.get(base_url + "/robots.txt", timeout=5)
                status_code = file.status_code
                if status_code >= 200 and status_code < 300:
                    # get robots.txt file content
                    #file_content = file.raw_response.content.decode()
                    file_content = file.text
                    print(file_content)

                    file_lines = file_content.split('\n')
                    self.robots[base_url] = file_lines
                    print(file_lines)

                    # check robots.txt
                    self.rparser.parse(file_lines)
                else:
                    print("not a good link to fetch robots file")
                    return False

            can_fetch = self.rparser.can_fetch("IR WR 26286982", url)
            delay = self.rparser.crawl_delay("IR WR 26286982")

            if not can_fetch:
                print("not allowed to crawl")
                return False

            return True
        except requests.ConnectionError:
            print("There was a connection error")
            return False
        except requests.Timeout:
            print("There was timeout")
            return False
        except requests.RequestException:
            return False

    # return bool
    def is_good_url(self, url):

        # CHECKING ROBOTS.TXT
        if not self.check_robots_txt(url):
            return False

        # MAKE HEAD REQUEST AND CHECK IF WE WANT TO ACTUALLY DOWNLOAD THIS PAGE!
        h = requests.head(url)

        # CHECKING CONTENT LENGTH
        if ('Content-length' in h.headers.keys()):
            content_length = int(h.headers['Content-length'])
            print("Content Length: ", content_length)
            if (content_length == 0):
                return False

        # CHECK CONTENT QUALITY
        # calculate proportion of tags versus


        # CHECK FOR SIMILAR PAGES WITH NO INFORMATION
            # check for repeating/extra directories



        # check if there are more tags than actual text content??

        return True


    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break

            print("URL: ", tbd_url)
            good_url = self.is_good_url(tbd_url)
            print("Is this a good url: ", good_url)

            if good_url:
                resp = download(tbd_url, self.config, self.logger)
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")

                status_code = resp.status
                #print("STATUS: ", status_code)
                if status_code >= 200 and status_code < 300: # can switch this to check later
                    self.stats.update_stats(tbd_url, resp)
                    scraped_urls = scraper(tbd_url, resp)
                    for scraped_url in scraped_urls:
                        self.frontier.add_url(scraped_url)
                self.frontier.mark_url_complete(tbd_url)

                # can change delay here, if I want to check politeness based on website
                time.sleep(self.config.time_delay)
