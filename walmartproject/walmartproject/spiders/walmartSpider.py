import scrapy
from scrapy_splash import SplashRequest
import json


class WalmartMacbooksSpider(scrapy.Spider):
    name = 'walmart_macbooks'
    allowed_domains = ['walmart.com']
    seen_urls = set()
    item_counter = 0

    def __init__(self, *args, **kwargs):
        super(WalmartMacbooksSpider, self).__init__(*args, **kwargs)
        self.item_counter = 0

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

        base_url = 'https://www.walmart.com/browse/electronics/all-apple-macbook/3944_1089430_3951_8945805_4431341?povid=ETS_computing_facet_search&browse_macbooks&page='
        for page in range(1, 26):  # For pages 1 to 25
            url = f"{base_url}{page}"
            yield SplashRequest(
                url,
                self.parse,
                endpoint='render.html',
                args={'wait': 5, 'viewport': '1024x2480', 'timeout': 90},
                headers=headers,
                meta={'page': page}
            )

    def parse(self, response):
        script_content = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        if script_content:
            data = json.loads(script_content)
            items = data['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']

            for item in items:
                product_url = f"https://www.walmart.com{item.get('canonicalUrl')}"
                if product_url == "https://www.walmart.comNone" or not item.get('name'):
                    continue

                if product_url not in self.seen_urls:
                    self.seen_urls.add(product_url)
                    product_name = item.get('name')
                    price_info = item.get('priceInfo', {})
                    product_price = price_info.get('linePriceDisplay', price_info.get('itemPrice', 'N/A'))

                    self.item_counter += 1
                    yield {
                        'number': self.item_counter,
                        'name': product_name,
                        'price': product_price,
                        'url': product_url,
                    }
