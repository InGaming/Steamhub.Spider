import scrapy
import json
from scrapy.http.request import Request
from orator import DatabaseManager


class GameInfosSpider(scrapy.Spider):
    name = "game_infos"
    start_urls = [
        'https://store.steampowered.com/search/?sort_by=Released_DESC&tags=-1&category1=998',
    ]

    def parse(self, response):
        db_config = self.settings.get('DB')
        config = {
            'mysql': {
                'driver': db_config['driver'],
                'host': db_config['host'],
                'port': db_config['port'],
                'database': db_config['database'],
                'user': db_config['user'],
                'password': db_config['password'],
                'prefix': db_config['prefix']
            }
        }

        db = DatabaseManager(config)

        for element in response.css('.search_result_row'):
            if element is not None:
                link = element.css('a::attr(href)').extract_first()
                appid = element.css('a::attr(data-ds-appid)').extract_first()

                yield Request(link, meta={'appid': appid, 'db': db},
                              callback=self.parse_info)

                yield Request('https://store.steampowered.com/api/appdetails?appids=' + appid, meta={'appid': appid, 'db': db},
                              callback=self.parse_info_api)

        for next in response.css('#search_result_container > div.search_pagination > div.search_pagination_right > a.pagebtn::attr(href)'):
            if next is not None:
                yield response.follow(next, callback=self.parse)

    def parse_info(self, response):
        yield {
            'db': response.meta['db'],
            'appid': response.meta['appid'],
            'review_title': response.css('.user_reviews_summary_bar .summary_section .game_review_summary::text').extract(),
            'review_people': response.css('.user_reviews_summary_bar .summary_section span:nth-child(3)::text').extract(),
            'tag': response.css('.glance_tags a::text').extract(),
        }

    def parse_info_api(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        yield {
            'db': response.meta['db'],
            'appid': response.meta['appid'],
            'jsonresponse': jsonresponse
        }
