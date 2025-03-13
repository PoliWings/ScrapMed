import scrapy
from urllib.parse import urlparse
from termedia.items import TermediaItem

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
                    scheme = urlparse(response.url).scheme
                    volume = scheme + "://" + base_url + volume
                item = TermediaItem()
                item["type"] = "whole_volume_in_pdf"
                item["file_urls"] = [volume]
                yield item
            else:
                yield response.follow(volume, self.parse_volume)

    def parse_volume(self, response):
        # TODO: corner case - no articles but url to new location 

        # button to download whole volume
        whole_volume_url = response.css("a.issuePdfButton::attr(href)").get()
        if whole_volume_url:
            item = TermediaItem()
            item["type"] = "whole_volume_in_pdf"
            item["file_urls"] = [whole_volume_url]
            yield item
        else:
            articles = response.css("div.magArticle")
            if len(articles) == 0:
                articles = response.css("div.magArticleNoBorder")
            # yield {"type": "list_of_articles", "url": response.url, "articles": len(articles)}
            for article in articles:
                title = article.css("h2::text").getall()
                url = article.css("a.magArticleTitle::attr(href)").get()

                if url is None:
                    url = article.css("div.magArticle a::attr(href)").get()
                elif url is None:
                    url = article.css("a.abstractFullText.dirLeft::attr(href)").get()

                yield response.follow(url, self.parse_article, meta={"title": title})

    def parse_article(self, response):
        title = response.meta.get("title")
        pdf_url = response.css("a.darkButton::attr(href)").get()

        if not pdf_url is None:
            if pdf_url.startswith("/"):
                base_url = urlparse(response.url).netloc
                scheme = urlparse(response.url).scheme
                pdf_url = scheme + "://" + base_url + pdf_url
                
                yield response.follow(pdf_url, self.parse_article, meta={"title": title})
        else:       
            pdf_url = response.css("div.articlePDF").css("a::attr(href)").get()

            if pdf_url is None:
                pdf_url = response.css("a.abstractFullText.dirLeft::attr(href)").get()

            # relative url
            if pdf_url.startswith("/"):
                base_url = urlparse(response.url).netloc
                scheme = urlparse(response.url).scheme
                pdf_url = scheme + "://" + base_url + pdf_url

            license = response.css("div.regulationsInfo::text").get()

            if license is None:
                license = response.css("div.em-09.pad-top-15::text").get()

            item = TermediaItem()
            item["type"] = "article_pdf"
            item["file_urls"] = [pdf_url]
            item["title"] = title
            item["license"] = license
            yield item