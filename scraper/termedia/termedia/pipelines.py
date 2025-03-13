# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class TermediaPipeline:
    def process_item(self, item, spider):
        pattern = r"\(([^)]+)\)"

        adapter = ItemAdapter(item)
        if adapter.get("title"):
            adapter["title"] = " ".join(adapter["title"]).strip()

        if adapter.get("license"):
            adapter["license"]= re.findall(pattern, adapter["license"])[0]

        return item
