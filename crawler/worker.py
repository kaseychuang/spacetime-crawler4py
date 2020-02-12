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
import urlFilter as filter


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.stats = statistics.Statistics("stats.txt")
        super().__init__(daemon=True)

    # method to check if the url is worth downloading
        # filters in order to avoid wasting time with bad pages
    def is_good_url(self, url):

        # check robots.txt
        if not filter.allows_crawl(url):
            print("not allowed to crawl or could not fetch file")
            return False

        if not filter.is_quality_content(url):
            print("not quality content")
            return False

        if not filter.is_good_url(url):
            print("bad url")
            return False

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
                if status_code >= 200 and status_code < 300: # can switch this to check later
                    self.stats.update_stats(tbd_url, resp)
                    scraped_urls = scraper(tbd_url, resp)
                    for scraped_url in scraped_urls:
                        self.frontier.add_url(scraped_url)
                #else:
                   # print("bad status so don't do anything with it")
                self.frontier.mark_url_complete(tbd_url)

                # can change delay here, if I want to check politeness based on website
                time.sleep(self.config.time_delay)
