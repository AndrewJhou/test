from selenium import webdriver
from selenium.webdriver.firefox.service import Service

import scrapy


class NikeSpider(scrapy.Spider):
    name = 'products'
    start_urls = ['https://www.nike.com.cn/w/']

    def __init__(self):
        geckodriver_path = '/Users/ray/Downloads/geckodriver'
        service = Service(executable_path=geckodriver_path)
        self.browser = webdriver.Firefox(service=service)
        self.browser.set_page_load_timeout(300)

    def parse(self, response):
        detail_page_links = response.css('div.product-card__body figure a.product-card__link-overlay')
        yield from response.follow_all(detail_page_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        size = response.xpath('//div[@data-testid="pdp-grid-selector-item"]/label/text()').getall()
        if size:
            size = [each.strip() for each in size]
        color = response.xpath('//li[@data-testid="product-description-color-description"]/text()').getall()
        color = color[2] if color else ''
        sku = response.url.split('/')[-1]
        if not sku[0].isdigit():
            yield {
                'title': extract_with_xpath('//div[@id="title-container"]/h1/text()'),
                'subtitle': extract_with_xpath('//div[@id="title-container"]/h2/text()'),
                'price': extract_with_xpath('//div[@id="price-container"]/span/text()'),
                'color': color,
                'size': size,
                # 'sku': extract_with_xpath('//li[@data-testid="product-description-style-color"]/text()').getall()[2],
                'sku': sku,
                'details': extract_with_xpath('//div[@id="product-description-container"]/p/text()'),
                'img_urls': extract_with_xpath('//div[@id="mobile-image-carousel"]/ul/li[1]/div/img/@src'),
            }
