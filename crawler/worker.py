from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time
import statistics
import extractor as ex


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.stats = statistics.Statistics("stats.txt")  # added this, check if it works
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            
            # USE RESP HERE TO ANALYZE DATA and store stats?
            # check if the link/download is good first!!!
            status_code = resp.status
            if status_code >= 200 and status_code < 300: # can switch this to check later
                self.stats.update_stats(tbd_url, resp)

            scraped_urls = scraper(tbd_url, resp)
            #print("VALID URLS")
           # print(scraped_urls)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)

            # can change delay here, if I want to check politeness based on website
            # ADD CODE ON ROBOTS.TXT HERE!
            time.sleep(self.config.time_delay)
