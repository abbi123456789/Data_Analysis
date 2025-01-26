import scrapy
from fake_useragent import UserAgent
from scrapy.utils.project import get_project_settings

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.in"]
    start_urls = [
        "https://www.amazon.in/s?k=mushroom"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # 2-second delay between requests
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,  # Limit concurrent requests
        "USER_AGENT": UserAgent().random,  # Randomize User-Agent
        "FEEDS": {
            "output.csv": {"format": "csv"},  # Save output to CSV
        },
    }

    def parse(self, response):
        # Select product containers
        products = response.xpath("//div[@data-component-type='s-search-result']")
        for product in products:
            yield {
                "product_name": product.xpath(".//h2/a/span/text()").get(),
                "seller": product.xpath(".//span[contains(text(),'by')]/following-sibling::span/text()").get(),
                "price": product.xpath(".//span[@class='a-price-whole']/text()").get(),
                "ratings": product.xpath(".//span[@class='a-icon-alt']/text()").get(),
                "reviews": product.xpath(".//span[@aria-label]/following-sibling::span[@class='a-size-base']/text()").get(),
            }

        # Find and follow the next page link
        next_page = response.xpath("//a[contains(@class,'s-pagination-next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
