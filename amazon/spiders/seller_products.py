import scrapy


class SellerProductsSpider(scrapy.Spider):
    name = 'seller_products'
    allowed_domains = ['amazon.com']
    start_urls = ['http://amazon.com/']

    def parse(self, response):
        pass
