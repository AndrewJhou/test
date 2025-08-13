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
        detail_page_links = response.xpath('//div[@class="product-card__body"]/figure/a[@class="product-card__link-overlay"]/@href').getall()
        url_count = 48 #48
        _links = []
        for each in detail_page_links:
            sku = each.split('/')[-1]
            if url_count > 0 and not sku[0].isdigit():
                url_count = url_count - 1
                _links.append(each)
        # _links = ['https://www.nike.com.cn/t/10-lego-collection-%E7%AF%AE%E7%90%83-plzdEw9O/IM2113-723']
        # _links = ['https://www.nike.com.cn/t/vomero-plus-%E8%80%90%E5%85%8B%E8%B6%85%E7%BA%A7%E8%BF%88%E6%9F%94%E5%A5%B3%E5%AD%90%E5%85%AC%E8%B7%AF%E8%B7%91%E6%AD%A5%E9%9E%8B-zn1pca1R/HV8154-001']
        yield from response.follow_all(_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        subtitle = extract_with_xpath('//div[@id="title-container"]/h2/text()')
        if subtitle == '篮球':
            size = response.xpath('//legend[@data-testid="pdp-grid-selector-legend"]/span/text()').getall()
        else:
            size = []
            _s = response.xpath('//div[@data-testid="pdp-grid-selector-item"]')
            for each in _s:
                _text = each.xpath('./label/text()').get(default='').strip()
                if each.xpath('./input[@aria-disabled="true"]'):
                    _text = r'{}（已售磬）'.format(_text)
                size.append(_text)
        
        color = response.xpath('//li[@data-testid="product-description-color-description"]/text()').getall()
        color = color[2] if color else ''
        yield {
            'title': extract_with_xpath('//div[@id="title-container"]/h1/text()'),
            'subtitle': subtitle,
            'price': extract_with_xpath('//div[@id="price-container"]/span/text()'),
            'color': color,
            'size': size,
            # 'sku': extract_with_xpath('//li[@data-testid="product-description-style-color"]/text()').getall()[2],
            'sku': response.url.split('/')[-1],
            'details': extract_with_xpath('//div[@id="product-description-container"]/p/text()'),
            'img_urls': extract_with_xpath('//div[@id="mobile-image-carousel"]/ul/li[1]/div/img/@src'),
        }
