from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from stack.items import StackItem
from tkinter import *
from tkinter import ttk
from tkinter import Tk

class StackSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]
    def __init__(self, value='', *args, **kwargs):
        super(StackSpider, self).__init__(*args, **kwargs)
        self.search_value = value
        self.counter = 0
        self.start_urls = [f'http://stackoverflow.com/questions?pagesize=50&sort=newest']

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="s-post-summary--content"]//h3')

        if not questions:
            self.log("No questions found!")

        count = 0

        for question in questions:
            item = StackItem()
            title = question.xpath(
                'a[@class="s-link"]/text()').extract_first(default='').strip()
            url = question.xpath(
                'a[@class="s-link"]/@href').extract_first(default='').strip()


            if title and url:
                item['title'] = title
                item['url'] = response.urljoin(url)  # To form the full URL
                yield item

                if self.search_value.lower() in title.lower():
                    self.counter += 1
                    count += 1
                    yield {
                        'counter': self.counter,
                        'search_value': self.search_value,
                    }

            else:
                self.log(f"Missing title or url in question: {question.extract()}")

            print("Count:", count)   
