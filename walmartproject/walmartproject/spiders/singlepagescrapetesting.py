import scrapy
from scrapy_splash import SplashRequest
import json

class WalmartMacbookPage21Spider(scrapy.Spider):
    name = 'walmart_macbook_page_21'
    allowed_domains = ['walmart.com']

    # Directly start from page 21 URL
    start_urls = [
        'https://www.walmart.com/browse/electronics/all-apple-macbook/3944_1089430_3951_8945805_4431341?povid=ETS_computing_facet_search&browse_macbooks&page=21'
    ]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Ch-Ua': '"Chromium";v="121", "Not A(Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
        }
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                endpoint='render.html',
                args={'wait': 5},
                headers=headers
            )

    def parse(self, response):
        # Extracting the JSON data from the script tag
        script_content = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        if script_content:
            data = json.loads(script_content)

            items = data['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']
            for item in items:
                yield {
                    'name': item.get('name'),
                    'price': item['priceInfo'].get('linePriceDisplay', item['priceInfo'].get('itemPrice')),
                    'url': f"https://www.walmart.com{item.get('canonicalUrl')}",
                    'page': 21  # Add the page number statically since it's always page 21
                }
