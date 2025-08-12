from selenium import webdriver

import scrapy


class NikeSpider(scrapy.Spider):
    name = 'products'

    start_urls = ['https://www.nike.com.cn/w/']

    def __init__(self):
        # self.browser = webdriver.Chrome('/Users/ray/Downloads/chromedriver-mac-arm64/chromedriver')
        # self.browser.set_page_load_timeout(300)
        pass

    def parse(self, response):
        detail_page_links = response.css('div.product-card__body figure a.product-card__link-overlay')
        yield from response.follow_all(detail_page_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_xpath(query):
            return response.xpath(query)

        yield {
            'title': extract_with_xpath('//div[@id="title-container"]/h1/text()').get(),
            'subtitle': extract_with_xpath('//div[@id="title-container"]/h2/text()').get(),
            'price': extract_with_xpath('//div[@id="price-container"]/span/text()').get(),
            'color': extract_with_xpath('//li[@data-testid="product-description-color-description"]/text()').getall()[2],
            
            # 'size': response.css('fieldset div div div input::value').getall(),
            
            'sku': extract_with_xpath('//li[@data-testid="product-description-style-color"]/text()').getall()[2],
            'details': extract_with_xpath('//div[@id="product-description-container"]/p/text()').get(),
            'img_urls': extract_with_xpath('//div[@id="mobile-image-carousel"]/ul/li[1]/div/img/@src').get()
        }
