import scrapy
import json
from scrapy.http.request import Request
from orator import DatabaseManager


class NewsYysSpider(scrapy.Spider):
    name = "news_yys"
    start_urls = [
        'http://www.yystv.cn/boards/get_board_list_by_page?page=0&value=culture',
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
        json_response = json.loads(response.body_as_unicode())
        json_data = json_response['data']
        for item in json_data:
            yys_title = item['title']
            yys_link = 'http://www.yystv.cn/p/' + item['id']
            yys_image = item['cover']
            yys_author = item['author']
            yys_description = item['preface']

            yield Request(yys_link, meta={'id': item['id'], 'db': db, 'title': yys_title},
                          callback=self.parse_info)
            select_data = db.table('News').where({
                'Title': yys_title,
                'Link': yys_link
            }).first()

            if select_data:
                if yys_title == select_data['Title'] and yys_link == select_data['Link']:
                    pass
                else:
                    db.table('News').insert({
                        'Title': yys_title,
                        'NewsID': item['id'],
                        'Author': yys_author,
                        'Description': yys_description,
                        'Image': yys_image,
                        'Link': yys_link,
                        'Type': '文化',
                        'Site': '游研社'
                    })

            else:
                db.table('News').insert({
                    'Title': yys_title,
                    'NewsID': item['id'],
                    'Author': yys_author,
                    'Description': yys_description,
                    'Image': yys_image,
                    'Link': yys_link,
                    'Type': '文化',
                    'Site': '游研社'
                })

    def parse_info(self, response):
        meta_title = response.meta['title']
        meta_db = response.meta['db']
        meta_id = response.meta['id']
        select_data = meta_db.table('NewsArticles').where({
            'Title': meta_title
        }).first()
        if select_data:
            if select_data['Title'] == meta_title:
                pass
            else:
                meta_db.table('NewsArticles').insert({
                    'NewsID': meta_id,
                    'Title': meta_title,
                    'Body': response.css('body > div.wrapper > div.content-block.rel > div.doc-content.rel').extract()
                })

        else:
            meta_db.table('NewsArticles').insert({
                'NewsID': meta_id,
                'Title': meta_title,
                'Body': response.css('body > div.wrapper > div.content-block.rel > div.doc-content.rel').extract()
            })
