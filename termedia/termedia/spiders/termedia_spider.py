import scrapy


class TermediaSpiderSpider(scrapy.Spider):
    name = "termedia_spider"
    allowed_domains = ["termedia.pl"]
    start_urls = ["https://termedia.pl/Czasopisma"]

    def parse(self, response):
        pass
