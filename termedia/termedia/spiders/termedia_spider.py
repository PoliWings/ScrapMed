import scrapy
from urllib.parse import urlparse

class TermediaSpiderSpider(scrapy.Spider):
    name = "termedia_spider"
    # allowed_domains = ["termedia.pl"]
    start_urls = ["https://termedia.pl/Czasopisma"]

    def parse(self, response):
        magazines = response.css("div.magazinesList").css("a::attr(href)").getall()
        for magazine in magazines:
            magazine = magazine.replace("/Czasopismo", "/Journal")
            if not magazine.endswith("/"):
                magazine = magazine + "/"
            magazine = magazine + "Archive"
            yield response.follow(magazine, self.parse_magazine)
    
    def parse_magazine(self, response):
        # one magazine had stupid redirect and removed the /Archive part
        if not response.url.endswith("Archive"):
            yield response.follow(response.url + "Archive", self.parse_magazine)

        # default select
        volumes = response.css("a.archiveVolume::attr(href)").getall()

        # select by covers
        if len(volumes) == 0:
            volumes = response.css("a.coversArchiveVolume::attr(href)").getall()

        # print all magazines with volume numbers
        # yield {"url": response.url, "volumes": len(volumes)}

        for volume in volumes:
            # whole volume is a pdf
            if volume.endswith(".pdf"):
                if volume.startswith("/"):
                    base_url = urlparse(response.url).netloc
                    volume = base_url + volume
                yield {"type": "whole_volume_in_pdf", "url": volume}
            else:
                yield response.follow(volume, self.parse_volume)

    def parse_volume(self, response):
        # TODO: corner case - no articles but url to new location 

        # button to download whole volume
        whole_volume_url = response.css("a.issuePdfButton::attr(href)").get()
        if whole_volume_url:
            yield {"type": "whole_volume_in_pdf", "url": whole_volume_url}
        else:
            articles = response.css("a.magFullT::attr(href)").getall()
            # yield {"type": "list_of_articles", "url": response.url, "articles": len(articles)}
            for article in articles:
                # list of pdf articles
                if article.endswith(".pdf"):
                    yield {"type": "article_pdf", "url": article}
                # list of article pages
                else:
                    yield response.follow(article, self.parse_article)
    
    def parse_article(self, response):
        pdf_url = response.css("div.articlePDF").css("a::attr(href)").get()
        yield {"type": "article_pdf", "url": pdf_url}
                
